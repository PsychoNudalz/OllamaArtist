import datetime
import json
import urllib, urllib.parse, urllib.request
import uuid
import random
import asyncio
import traceback

from PIL import Image
import io

import websocket

from ImageOrder import ImageOrder

WORKFLOW_PATH = "ComfyUIWorkflow/"
OUTPUT_PATH = "ImageOut/"

SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())


def queue_prompt(prompt, client_id):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()


async def generate_image(order: ImageOrder, save_to_time=False) -> str:
    # Loads the default workflow
    ComfyUIWorkflow = WORKFLOW_PATH + "Default.json"
    with open(ComfyUIWorkflow, "r", encoding="utf-8") as f:
        json_str = f.read()
    prompt = json.loads(json_str)

    # Modify the text prompt for the positive CLIPTextEncode node
    prompt["6"]["inputs"]["text"] = "masterpiece best quality man"

    # Change the seed for different results
    prompt["3"]["inputs"]["seed"] = random.randint(0, 1000000)

    try:

        ws = websocket.WebSocket()
        ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")
    except ConnectionRefusedError as e:
        print(f"Error connecting to the server: {SERVER_ADDRESS}\nMake sure ComfyUI is running\n{e}")
        return ""

    try:
        # return ""

        # Get prompt_id for tracking the execution
        prompt_id = queue_prompt(prompt, CLIENT_ID)['prompt_id']

        # await asyncio.sleep(5)
        history = {}
        historyFailSafe:int = 0

        while len(history) == 0:
            try:
                # Get history for the executed prompt
                history = get_history(prompt_id)[prompt_id]
            except KeyError as e:
                if historyFailSafe < 100:
                    historyFailSafe += 1
                    print("Waiting for history")
                    await asyncio.sleep(1)
                else:
                    print(f"History not found: {e}")
                    ws.close()
                    return ""
        print(history)

        # Since a ComfyUI workflow may contain multiple SaveImage nodes,
        # and each SaveImage node might save multiple images,
        # we need to iterate through all outputs to collect all generated images
        output_images = {}
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

        # Process the generated images
        for node_id in output_images:
            for image_data in output_images[node_id]:
                # Convert bytes to PIL Image
                image = Image.open(io.BytesIO(image_data))
                # Process image as needed
                if not save_to_time:
                    image.save(f"{OUTPUT_PATH}output.png")
                else:
                    image.save(f"{OUTPUT_PATH}output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")


    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        print("Generation Complete")
        # Always close the WebSocket connection
        ws.close()

    return ""


if __name__ == "__main__":
    asyncio.run(generate_image(ImageOrder()))
