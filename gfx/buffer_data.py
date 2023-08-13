
import array

from typing import Self

from gfx.attribute import Attribute


class BufferData:
    def __init__(self: Self, data: array.array, target: int, attributes: list[Attribute] = None) -> None:
        self.data = data
        self.target = target
        self.attributes = attributes
        pass
