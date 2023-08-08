
from io import BufferedReader
from typing import Self
from gfx.shader import Shader, ShaderType

from gfx.shader_program import ShaderProgram


class ShaderLoader:
    def __init__(self: Self, filepath: str) -> None:
        self.filepath = filepath
        self.version = 0

    def load(self: Self) -> ShaderProgram:
        program: ShaderProgram = None
        with open(self.filepath, "rb") as f:
            frag: Shader = None
            vert: Shader = None
            frag_src = ""
            vert_src = ""
            frag_uniforms = list[str]()
            vert_uniforms = list[str]()
            stage = 0

            while f.read(1):
                f.seek(-1, 1)
                match stage:
                    case 0:
                        self.parse_header(f)
                        stage += 1
                    case 1:
                        frag_uniforms = self.parse_uniforms(f)
                        stage += 1
                    case 2:
                        frag_src = self.parse_src(f)
                        stage += 1
                    case 3:
                        vert_uniforms = self.parse_uniforms(f)
                        stage += 1
                    case 4:
                        vert_src = self.parse_src(f)
                        stage += 1

            frag = Shader(ShaderType.fragment, frag_src, frag_uniforms)
            vert = Shader(ShaderType.vertex, vert_src, vert_uniforms)
            frag.compile()
            vert.compile()
            program = ShaderProgram([frag, vert])
            program.compile()

        return program

    def parse_header(self: Self, f: BufferedReader) -> None:
        self.version: int = int.from_bytes(f.read(2), "big")

    def parse_uniforms(self: Self, f: BufferedReader) -> list[str]:
        uniforms = list[str]()
        temp = ""
        while (b := f.read(1)):
            c = b.decode()
            if c == '\0':
                break
            if c == ':':
                uniforms.append(temp)
                temp = ""
                continue
            temp += c
        return uniforms

    def parse_src(self: Self, f: BufferedReader) -> str:
        src = ""
        while (b := f.read(1)):
            c = b.decode()
            if c == '\0':
                break
            src += c
        return src
