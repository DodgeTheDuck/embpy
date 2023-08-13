

from gfx.texture import Texture
from gfx.material_properties import MaterialProperties, TextureType
from gfx.mesh import Mesh


def load_obj(file_path: str) -> Mesh:
    meshes = []
    vertices = []
    normals = []
    uvs = []
    indices = []
    material = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(x) for x in line[2:].split()]
                vertices.extend(vertex)
            elif line.startswith('vn '):
                normal = [float(x) for x in line[3:].split()]
                normals.extend(normal)
            elif line.startswith('vt '):
                uv = [float(x) for x in line[3:].split()]
                uvs.extend(uv)
            elif line.startswith('f '):
                face = [int(x.split('/')[0]) - 1 for x in line[2:].split()]
                indices.extend(face)
            elif line.startswith('mtllib '):
                material_file = line[7:].strip()
                material = parse_material(file_path.split("/")[-2] + "/" + material_file)

        if material is not None:
            meshes.append(Mesh(vertices, normals, uvs, indices, material))

    return meshes


def parse_material(material_file: str) -> MaterialProperties:
    material = MaterialProperties()
    current_texture_type = None

    with open(material_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('newmtl '):
                current_texture_type = None
            elif line.startswith('map_Ka '):
                texture_file = line[7:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.albedo] = texture
                current_texture_type = TextureType.albedo
            elif line.startswith('map_Kd '):
                texture_file = line[7:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.diffuse] = texture
                current_texture_type = TextureType.diffuse
            elif line.startswith('map_Ks '):
                texture_file = line[7:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.specular] = texture
                current_texture_type = TextureType.specular
            elif line.startswith('map_Ke '):
                texture_file = line[7:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.emissive] = texture
                current_texture_type = TextureType.emissive
            elif line.startswith('map_bump ') or line.startswith('bump '):
                texture_file = line[9:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.bump] = texture
                current_texture_type = TextureType.bump
            elif line.startswith('map_d '):
                texture_file = line[6:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.alpha] = texture
                current_texture_type = TextureType.alpha
            elif line.startswith('map_disp '):
                texture_file = line[9:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.displacement] = texture
                current_texture_type = TextureType.displacement
            elif line.startswith('map_Ns '):
                texture_file = line[7:].strip()
                texture = Texture(texture_file)
                material.textures[TextureType.normal] = texture
                current_texture_type = TextureType.normal
            elif line.startswith('map_ '):
                # Custom texture type
                texture_file = line[5:].strip()
                texture = Texture(texture_file)
                material.textures[current_texture_type] = texture

    return material
