import asyncio
from ImageOrder import ImageOrder
import OllamaArtist
import logging
import ComfyUIController


if __name__ == "__main__":
    order:ImageOrder = OllamaArtist.request_chat_imageOrder()
    if not order or order.Text=="":
        logging.error("No order received from Ollama")
        exit(1)


    asyncio.run(ComfyUIController.generate_image(order,True))
    # generate_image(order_cat_test))