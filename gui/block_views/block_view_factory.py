import logging
from typing import Type

from game.blocks.block import AbstractBlock
from game.blocks.impl.empty_block import EmptyBlock
from game.blocks.impl.melting_ice import MeltingIceBlock
from game.blocks.impl.player import Player
from game.blocks.impl.rock import RockBlock
from gui.block_views.block import BlockView
from gui.block_views.empty_block import EmptyBlockView
from gui.block_views.melting_ice import MeltingIceBlockView
from gui.block_views.player import PlayerBlockView
from gui.block_views.rock_block import RockBlockView

registered_block_views = {
    EmptyBlockView : EmptyBlock,
    RockBlockView: RockBlock,
    PlayerBlockView: Player,
    MeltingIceBlockView: MeltingIceBlock,
}


def to_block(block_view_type: Type[BlockView]) -> AbstractBlock:
    return registered_block_views[block_view_type]()


def from_block(block: AbstractBlock, canvas) -> BlockView:
    for view_type, block_type in registered_block_views.items():
        if block_type != type(block):
            continue
        candidate = view_type.from_block(canvas, block)
        if candidate is None:
            raise ValueError("Factory failed. Block view does not support block.")
        return candidate
    logging.error(f"No registered block view is found for block of type: {type(block)}")
    raise ValueError("block view factory failed")
