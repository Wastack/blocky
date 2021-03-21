import logging
import os
import tkinter

from PIL import Image, ImageTk

from game.utils.direction import Direction
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

    def get_image(self, image_file_name: str, rotate: Direction = Direction.RIGHT) -> tkinter.PhotoImage:
        load = self._images.get(image_file_name)
        if load is None:
            logging.info(f"Loading image: {image_file_name}")
            load = Image.open(
                os.path.join("resources", image_file_name)).resize(
                (BLOCK_SIZE, BLOCK_SIZE))
            self._images[image_file_name] = load
        load = rotate_image_to_direction(load, rotate)

        photo = ImageTk.PhotoImage(load)
        return photo


def rotate_image_to_direction(image: Image, direction: Direction) -> Image:
    if direction == Direction.RIGHT:
        return image
    elif direction == Direction.UP:
        return image.rotate(90)
    elif direction == Direction.LEFT:
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == Direction.DOWN:
        return image.rotate(90*3)

    raise ValueError("Invalid direction")
