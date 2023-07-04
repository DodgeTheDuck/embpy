
import pywavefront
from gl.texture import Texture
from mesh import Mesh

# TODO:
# - probably roll my own obj loader


def load_obj(filename: str) -> Mesh:

    scene = pywavefront.Wavefront(filename, collect_faces=True)
    positions: list[float] = list[float]()
    normals: list[float] = list[float]()
    uvs: list[float] = list[float]()
    indices: list[int] = list[int]()
    texture: Texture = None

    for mesh in scene.mesh_list:
        for material in mesh.materials:
            location = filename.split("/")[0]
            texture = Texture(location + "/" + material.texture.file_name)
            for i in range(0, len(material.vertices), material.vertex_size):
                indices.extend(range(i, i+material.vertex_size))
                positions.append(material.vertices[i+5])
                positions.append(material.vertices[i+6])
                positions.append(material.vertices[i+7])
                normals.append(material.vertices[i+2])
                normals.append(material.vertices[i+3])
                normals.append(material.vertices[i+4])
                uvs.append(material.vertices[i])
                uvs.append(material.vertices[i+1])

    return Mesh(positions, normals, uvs, indices, texture)
