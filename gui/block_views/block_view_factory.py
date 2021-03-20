import logging

from game.blocks.block import AbstractBlock
from gui.block_views.block import BlockView
from gui.block_views.empty_block import EmptyBlockView
from gui.block_views.melting_ice import MeltingIceBlockView
from gui.block_views.player import PlayerBlockView
from gui.block_views.rock_block import RockBlockView

registered_block_views = [
    EmptyBlockView,
    RockBlockView,
    PlayerBlockView,
    MeltingIceBlockView,
]


def from_block(block: AbstractBlock, canvas) -> BlockView:
    for canditate_type in registered_block_views:
        candidate = canditate_type.from_block(canvas, block)
        if candidate is not None:
            return candidate
    logging.error(f"No registered block view is found for block of type: {type(block)}")
    raise RuntimeError("block view factory failed")
