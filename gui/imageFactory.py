import logging
import os
import tkinter

from PIL import Image, ImageTk

from gui.utils import BLOCK_SIZE


class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMeta, cls).__call__(*args,
                                                                    **kwargs)
        return cls._instance[cls]


class ImageFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._images = {}

    def get_image(self, image_file_name: str) -> tkinter.PhotoImage:
        photo = self._images.get(image_file_name)
        if photo is None:
            logging.info(f"Loading image: {image_file_name}")
            load = Image.open(
                os.path.join("resources", image_file_name)).resize(
                (BLOCK_SIZE, BLOCK_SIZE))
            photo = ImageTk.PhotoImage(load)
            self._images[image_file_name] = photo

        return photo
