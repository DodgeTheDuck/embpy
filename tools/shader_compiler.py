

import re
from typing import Self

frag_shader: str
vert_shader: str


class Variable:
    def __init__(self: Self, type: str, name: str, n_items: int = 0) -> None:
        self.type = type
        self.name = name
        self.n_items = n_items


class Struct:
    def __init__(self: Self, name: str) -> None:
        self.name = name
        self.properties = list[Variable]()

    def add_property(self: Self, type: str, name: str) -> None:
        self.properties.append(Variable(type, name))


def create_header() -> bytes:
    return bytes(
        int(1).to_bytes(2, 'big')  # version
    )


def create_delimiter() -> bytes:
    return bytes(b'\0')


def parse_structs(text: str) -> list[Struct]:
    structs = list[Struct]()
    struct_matches = re.findall(r"struct +([^ ]+) +{((.|\n)*)};", text)
    for struct_match in struct_matches:
        struct_name = struct_match[0]
        property_string = struct_match[1]
        properties = re.findall(r" +(.+) (.+);", property_string)
        struct = Struct(struct_name)
        for property_match in properties:
            struct.add_property(property_match[0], property_match[1])
        structs.append(struct)

    return structs


def parse_uniforms(text: str) -> list[Variable]:
    matches = re.findall(r"(uniform) ([^ ]+) ([^;|^[]*)((\[(\d+)\])|;)", text)
    uniforms = list[Variable]()
    for match in matches:
        var_type: str = match[1]
        var_name: str = match[2]
        var_items: int = int(match[5] or 0)
        uniforms.append(Variable(var_type, var_name, var_items))
    return uniforms


def compile_uniforms(uniforms: list[Variable]) -> bytes:
    arr = bytearray()
    for uni in uniforms:
        arr.extend(str.encode(uni.name))
        arr.extend(b':')
        arr.extend(str.encode(uni.type))
        arr.extend(b':')
        arr.extend(uni.n_items.to_bytes())
        arr.extend(b':')
    arr.extend(b'\0')
    return bytes(arr)


def compile_structs(structs: list[Struct]) -> bytes:
    arr = bytearray()
    for struct in structs:
        arr.extend(str.encode(struct.name))
        arr.extend(b':')
        for property in struct.properties:
            arr.extend(str.encode(property.name))
            arr.extend(b",")
        arr.extend(b':')
    arr.extend(b'\0')
    return bytes(arr)


def compile_shader(text: str) -> bytes:

    structs: list[Struct] = parse_structs(text)
    uniforms: list[Variable] = parse_uniforms(text)

    struct_bytes = compile_structs(structs)
    uni_bytes = compile_uniforms(uniforms)

    # handle source code
    shader_bytes = str.encode(text)

    return b"".join([struct_bytes, uni_bytes, shader_bytes])


def compile(files: list[str], name: str) -> None:
    global frag_shader, vert_shader

    with open(files[0]) as f:
        frag_shader = f.read()

    with open(files[1]) as f:
        vert_shader = f.read()

    bin: bytearray = bytearray()
    bin.extend(create_header())
    bin.extend(compile_shader(frag_shader))
    bin.extend(create_delimiter())
    bin.extend(compile_shader(vert_shader))

    with open(name, 'wb') as f:
        f.write(bin)
