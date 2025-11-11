import asyncio
import json
import logging

import ComfyUIController
import OllamaArtist
from src.ImageOrder import ImageOrder


async def create() -> str:
    order: ImageOrder = OllamaArtist.request_chat_image_order()
    if not order or order.Text == "":
        logging.error("No order received from Ollama")
        exit(1)

    image_path = await ComfyUIController.generate_image(order, True)

    return image_path


async def create_from_json(order_json: str) -> str:
    order: ImageOrder = ImageOrder(**json.loads(order_json))
    if not order or order.Text == "":
        logging.error("No order received from Ollama")
        exit(1)

    image_path = await ComfyUIController.generate_image(order, True)

    return image_path


async def get_order_json() -> str:
    return_json: str = OllamaArtist.request_chat_image_order_json()
    return return_json


if __name__ == "__main__":
    asyncio.run(create())
