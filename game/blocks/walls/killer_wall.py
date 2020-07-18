from game.blocks.walls.wall import Wall
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class KillerWall(Wall):
    def before_step(self, intruder: Moveable) -> MoveVerdict:
        intruder.set_dead()
        return MoveVerdict.NO_MOVE

    def after_step(self, intruder: Moveable) -> None:
        return
