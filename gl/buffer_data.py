
import array
from ast import Attribute
from typing import Self


class BufferData:
    def __init__(self: Self, data: array.array, target: int, attributes: list[Attribute] = None) -> None:
        self.data = data
        self.target = target
        self.attributes = attributes
        pass
