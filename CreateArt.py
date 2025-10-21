import asyncio
from ImageOrder import ImageOrder
import OllamaArtist
import logging
import ComfyUIController


async def Create() -> str:
    order: ImageOrder = OllamaArtist.request_chat_imageOrder()
    if not order or order.Text == "":
        logging.error("No order received from Ollama")
        exit(1)

    image_path =  await ComfyUIController.generate_image(order, True)

    return image_path


if __name__ == "__main__":
    asyncio.run(Create())
