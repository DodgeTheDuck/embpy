
from typing import Self

from mesh import Mesh
from transform import Transform


class MeshNode:
    def __init__(self: Self, meshes: list[Mesh], transform: Transform, name: str) -> None:
        self.name = name
        self.meshes = meshes
        self.transform = transform
