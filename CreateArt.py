import asyncio
from ImageOrder import ImageOrder
import OllamaArtist
import logging
import ComfyUIController


def Create():
    order: ImageOrder = OllamaArtist.request_chat_imageOrder()
    if not order or order.Text == "":
        logging.error("No order received from Ollama")
        exit(1)

    asyncio.run(ComfyUIController.generate_image(order, True))


if __name__ == "__main__":
    Create()
