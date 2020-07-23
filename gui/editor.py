import tkinter

from game.utils.position import Position
from gui.block import BlockView

_WINDOW_WIDTH = 1024
_WINDOW_HEIGHT = 768


def _create_window() -> tkinter.Tk:
    window = tkinter.Tk()
    window.title("Blocky")
    #window.attributes('-fullscreen', True)
    window.geometry(f"{_WINDOW_WIDTH}x{_WINDOW_HEIGHT}")
    return window


def _create_canvas(window) -> tkinter.Canvas:
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)
    return canvas


def _initialize_editor(canvas: tkinter.Canvas) -> None:
    rect = BlockView(canvas, Position(4, 5)).draw()
    #Block(canvas, Position(6, 5))


def main():
    window = _create_window()
    canvas = _create_canvas(window)
    _initialize_editor(canvas)
    window.mainloop()


if __name__ == "__main__":
    main()