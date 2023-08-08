

import re

frag_shader: str
vert_shader: str


def create_header() -> bytes:
    return bytes(
        int(1).to_bytes(2, 'big')  # version
    )


def create_delimiter() -> bytes:
    return bytes(b'\0')


def get_uniforms(text: str) -> list[str]:
    matches = re.findall(r"(uniform .+ )([^;]*)", text)
    return [match[1] for match in matches]


def compile_uniforms(uniforms: list[str]) -> bytes:
    arr = bytearray()
    for uni in uniforms:
        arr.extend(str.encode(uni))
        arr.extend(b':')
    arr.extend(b'\0')
    return bytes(arr)


def compile_shader(text: str) -> bytes:

    # handle uniforms
    uniforms = get_uniforms(text)
    uni_bytes = compile_uniforms(uniforms)

    # handle source code
    shader_bytes = str.encode(text)

    return b"".join([uni_bytes, shader_bytes])


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
