# ... existing code ...
import logging
import ollama
import datetime
import time
import asyncio
import threading
import json

from pyexpat.errors import messages

from ImageOrder import ImageOrder

MODEL = "gpt-oss:20b"
running = True
logging.basicConfig(level=logging.INFO)



async def progress_printer():
    while running:
        print(f"generating response {datetime.datetime.now().isoformat()}")
        await asyncio.sleep(1)


def start_async_progress_printer():
    asyncio.run(progress_printer())


def process_chat(question: str):
    global running
    printer_thread = threading.Thread(target=start_async_progress_printer, daemon=True)
    printer_thread.start()

    try:
        result = ollama.generate(model=MODEL, prompt=question)
        print(result.get("response", "[No response returned]"))
    finally:
        running = False
        printer_thread.join()


def request_chat_image_order() -> ImageOrder:
    global running
    printer_thread = threading.Thread(target=start_async_progress_printer, daemon=True)
    printer_thread.start()
    order: ImageOrder = ImageOrder(Text="", Style="", Age=0)
    # messages = [
    #     {"role": "system", "content": "You will be decide on an order for an image to be generated."
    #                                   "Rules:"
    #                                   "- The order output should follow the following json format: "
    #                                   "{'Text': <text of what to generate in string>, 'Style': <style of the art>, 'Age': <what age the image will mimic>}"
    #                                   "- Age MUST BE an integer value."
    #      },{"role": "user", "content": f"fill in this json {order.to_json()}, pick any idea you want" }
    # ]

    prompt: str = ("You will be decide on an order for an image to be generated."
                   "Rules:"
                   "- The order output should follow the following json format: "
                   f"{ImageOrder.to_string_prompt_format()}"
                   f"'Text': <text of what to generate in string> "
                   f"'Style': <style of the art>, "
                   f"'Age': <what age the image will mimic>"
                   f"'Seed': Random integer (200-20000) seed for the generation"
                   f"'Width': Width of the image (500-1000)"
                   f"'Height': Width of the image (500-1000)"
                   "- Age, Seed, Width, Height MUST BE an integer value."
                   "-No Quotation marks at the end of the json."
                   "-You will only return the order in json format.")
    try:
        # result = ollama.chat(model=MODEL, messages=messages)
        result = ollama.generate(model=MODEL, prompt=prompt)
        responseString = result.get("response", "[No response returned]")
        result = ollama.generate(model=MODEL, prompt=f"Fix {responseString} to make sure it is json valid"
                                                     f"only reply with the json"
                                                     f"-No Quotation marks at the end of the json.")
        responseString = result.get("response", "[Fix failed]")

    except Exception as e:
        print(e)
        return order
    finally:
        running = False
        printer_thread.join()

    # Remove the second-to-last character
    if len(responseString) >= 2:
        responseString = responseString[:-2] + responseString[-1]
        logging.info(f"Removed second-to-last character: {responseString}")


    logging.info(responseString)

    try:
        order = ImageOrder.model_validate_json(responseString)
    except Exception as e:
        print(f"image parse error: {responseString}")
    print(order.to_json())

    return order


def request_chat_image_order_json() -> str:
    order = request_chat_image_order()
    return order.to_json()

def ping() -> bool:
    try:
        ollama.list()  # This will call the local Ollama daemon
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # question = input("Ask me:\n")
    # process_chat(question)
    request_chat_image_order()
