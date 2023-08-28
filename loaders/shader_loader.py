
from io import BufferedReader
from typing import Self
from gfx.shader import Shader, ShaderType
from gfx.shader_program import ShaderProgram


class Variable:
    def __init__(self: Self, type: str, name: str, n_items: int = -1) -> None:
        self.type = type
        self.name = name
        self.n_items = n_items


class Struct:
    def __init__(self: Self, name: str, properties: list[str]) -> None:
        self.name = name
        self.properties = properties


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
            frag_structs = list[Struct]()
            frag_uniforms = list[Variable]()

            vert_structs = list[Struct]()
            vert_uniforms = list[Variable]()

            stage = 0

            while f.read(1):
                f.seek(-1, 1)
                match stage:
                    case 0:
                        self.__parse_header(f)
                        stage += 1
                    case 1:
                        frag_structs = self.__parse_structs(f)
                        stage += 1
                    case 2:
                        frag_uniforms = self.__parse_uniforms(f)
                        stage += 1
                    case 3:
                        frag_src = self.__parse_src(f)
                        stage += 1
                    case 4:
                        vert_structs = self.__parse_structs(f)
                        stage += 1
                    case 5:
                        vert_uniforms = self.__parse_uniforms(f)
                        stage += 1
                    case 6:
                        vert_src = self.__parse_src(f)
                        stage += 1
                        break

            frag_var_names = self.__create_variable_names(frag_uniforms, frag_structs)
            vert_var_names = self.__create_variable_names(vert_uniforms, vert_structs)

            frag = Shader(ShaderType.fragment, frag_src, frag_var_names)
            vert = Shader(ShaderType.vertex, vert_src, vert_var_names)
            frag.compile()
            vert.compile()
            program = ShaderProgram([frag, vert])
            program.compile()

        return program

    def __parse_header(self: Self, f: BufferedReader) -> None:
        self.version: int = int.from_bytes(f.read(2), "big")

    def __parse_uniforms(self: Self, f: BufferedReader) -> list[Variable]:
        uniforms = list[Variable]()
        stage = 0
        name = ""
        var_type = ""
        n_items = 0

        while (b := f.read(1)):
            match stage:
                case 0:
                    c = b.decode()
                    if c == ':':
                        stage = 1
                        continue
                    if c == '\0':
                        break
                    name += c
                case 1:
                    c = b.decode()
                    if c == ':':
                        stage = 2
                        continue
                    var_type += c
                case 2:
                    n_items = int.from_bytes(b)
                    stage = 3
                    continue
                case 3:
                    uniforms.append(Variable(var_type, name, n_items))
                    stage = 0
                    name = ""
                    n_items = 0
                    var_type = ""

        return uniforms

    def __parse_structs(self: Self, f: BufferedReader) -> list[Struct]:
        structs = list[Struct]()
        stage = 0
        properties = list[str]()
        name = ""
        property_name = ""

        while (b := f.read(1)):
            if name == "" and b.decode() == '\0':
                break
            match stage:
                case 0:
                    c = b.decode()
                    if c == ':':
                        stage = 1
                        continue
                    if c == '\0':
                        break
                    name += c
                case 1:
                    c = b.decode()
                    if c == ':':
                        stage = 2
                        continue
                    if c == ',':
                        properties.append(property_name)
                        property_name = ""
                        continue
                    property_name += c
                case 2:
                    structs.append(Struct(name, properties))
                    if b.decode() == '\0': break
                    name = ""
                    property_name = ""
                    stage = 0

        return structs

    def __parse_src(self: Self, f: BufferedReader) -> str:
        src = ""
        while (b := f.read(1)):
            c = b.decode()
            if c == '\0':
                break
            src += c
        return src

    def __create_variable_names(self: Self, variables: list[Variable], structs: list[Struct]) -> list[str]:
        result = list[str]()
        for var in variables:
            done = False
            for struct in structs:
                if var.type == struct.name:
                    for property in struct.properties:
                        if var.n_items > 0:
                            for i in range(0, var.n_items):
                                result.append(f"{var.name}[{i}].{property}")
                                done = True
                        else:
                            result.append(f"{var.name}.{property}")
                            done = True

            if not done:
                result.append(var.name)
        return result
