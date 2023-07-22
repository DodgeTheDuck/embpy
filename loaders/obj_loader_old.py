
import time
import pywavefront
from gl.texture import Texture
from material import Material, TextureType
from mesh import Mesh
import engine

# TODO:
# - roll my own .obj loader


def load_obj(filename: str) -> list[Mesh]:
    engine.console.write_line(f"loading model '{filename}'...")
    time_start = time.time_ns()
    scene = pywavefront.Wavefront(filename, collect_faces=True)
    time_after_load = time.time_ns()
    engine.console.write_line(f"loading finished in {(time_after_load - time_start) / 1e6}ms")
    engine.console.write_line(f"parsing model '{filename}'...")
    meshes = list[Mesh]()

    for mesh in scene.mesh_list:
        for material in mesh.materials:
            mesh_material: Material = Material()
            positions: list[float] = list[float]()
            normals: list[float] = list[float]()
            uvs: list[float] = list[float]()
            indices: list[int] = list[int]()
            if material.texture is not None:
                diffuse_path: str = material.texture.file_name
                location = filename.split("/")[0]
                mesh_material.set_texture(TextureType.albedo,
                                          Texture((location
                                                   + "/"
                                                   + diffuse_path)))

            indices.extend(range(0, len(material.vertices)))

            if material.has_normals and material.has_uvs:
                for i in range(0,
                               len(material.vertices),
                               material.vertex_size):
                    positions.append(material.vertices[i + 5])
                    positions.append(material.vertices[i + 6])
                    positions.append(material.vertices[i + 7])
                    normals.append(material.vertices[i + 2])
                    normals.append(material.vertices[i + 3])
                    normals.append(material.vertices[i + 4])
                    uvs.append(material.vertices[i])
                    uvs.append(material.vertices[i + 1])
                    mesh_material.col_albedo.append(material.diffuse[0])
                    mesh_material.col_albedo.append(material.diffuse[1])
                    mesh_material.col_albedo.append(material.diffuse[2])
            elif material.has_normals:
                for i in range(0,
                               len(material.vertices),
                               material.vertex_size):
                    positions.append(material.vertices[i + 3])
                    positions.append(material.vertices[i + 4])
                    positions.append(material.vertices[i + 5])
                    normals.append(material.vertices[i + 0])
                    normals.append(material.vertices[i + 1])
                    normals.append(material.vertices[i + 2])
                    mesh_material.col_albedo.append(material.diffuse[0])
                    mesh_material.col_albedo.append(material.diffuse[1])
                    mesh_material.col_albedo.append(material.diffuse[2])

            meshes.append(Mesh(positions,
                               normals,
                               uvs,
                               indices,
                               mesh_material))

    time_taken = time.time_ns() - time_after_load
    engine.console.write_line(f"parsing finished in {time_taken / 1e6}ms")

    return meshes
