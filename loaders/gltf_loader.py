import os
import time
from typing import Self
import glm
from gfx.buffer_data import BufferData
from gfx.material import ColorType, TextureType
from gfx.material_properties import MaterialProperties, ScalarType
from gfx.texture_2d import Sampler, Texture2D
from gfx.mesh import Mesh
import pygltflib as gltf
from gfx.attribute import Attribute, AttributeType
import OpenGL.GL as gl
from gfx.mesh_node import MeshNode
from core.node_graph import NodeGraph, Node
from gfx.transform import Transform
import core.engine as engine


type_map = {
    "VEC4": 4,
    "VEC3": 3,
    "VEC2": 2,
    "SCALAR": 1,
}


class GltfLoader:
    def __init__(self: Self, filepath: str) -> None:
        self.filepath: str = filepath

    def load(self: Self) -> NodeGraph[MeshNode]:

        engine.console.write_line(f"loading GLTF: {self.filepath}")
        start_time = time.time()

        model: gltf.GLTF2 = gltf.GLTF2().load(self.filepath)
        mesh_tree: NodeGraph = NodeGraph[MeshNode]()

        buffers: list[bytes] = []
        for buffer in model.buffers:
            buffers.append(model.get_data_from_buffer_uri(buffer.uri))

        if len(model.scenes) != 1:
            raise Exception(f"unsupported number of scenes in {self.filepath}")

        for scene in model.scenes:
            for node in scene.nodes:
                self._traverse_node(model.nodes[node], buffers, model, mesh_tree, mesh_tree.root)

        engine.console.write_line(f"finished loading GLTF in {time.time() - start_time}")

        return mesh_tree

    def _parse_texture(self: Self, model: gltf.GLTF2, texture: gltf.Texture, buffers: list[bytes]) -> Texture2D:

        gltf_image: gltf.Image = model.images[texture.source]
        sampler: Sampler = Sampler()
        if texture.sampler is not None:
            gltf_sampler: gltf.Sampler = model.samplers[texture.sampler]
            sampler.tex_wrap_s = gltf_sampler.wrapS
            sampler.tex_wrap_t = gltf_sampler.wrapT
            sampler.tex_min_filter = gltf_sampler.minFilter
            sampler.tex_mag_filter = gltf_sampler.magFilter
            sampler.target = gl.GL_TEXTURE_2D
        else:
            sampler.tex_wrap_s = gl.GL_CLAMP
            sampler.tex_wrap_t = gl.GL_CLAMP
            sampler.tex_min_filter = gl.GL_NEAREST
            sampler.tex_mag_filter = gl.GL_NEAREST
            sampler.target = gl.GL_TEXTURE_2D

        if gltf_image.uri:
            return Texture2D(os.path.join(os.path.dirname(self.filepath), gltf_image.uri), sampler)
        elif gltf_image.bufferView:
            buffer_view = model.bufferViews[gltf_image.bufferView]
            img_data = buffers[buffer_view.buffer][buffer_view.byteOffset:buffer_view.byteOffset + buffer_view.byteLength]
            with open("tex.png", "wb") as binary_file:
                binary_file.write(img_data)
            return Texture2D(img_data, sampler)

    def _parse_material_properties(self: Self, model: gltf.GLTF2, gltf_material: gltf.Material, buffers: list[bytes]) -> MaterialProperties:

        if gltf_material is None:
            return MaterialProperties.make_default()

        engine.console.write_line(f"loading material: {gltf_material.name}")

        material_properties = MaterialProperties()
        albedo: Texture2D = None
        albedo_color: glm.vec3 = glm.vec3(1, 1, 1)
        metallic_roughness: Texture2D = None
        normal: Texture2D = None

        metallic_factor: float = 0.0
        roughness_factor: float = 0.0

        if gltf_material.normalTexture:
            property = gltf_material.normalTexture
            gltf_normal: gltf.Texture = model.textures[property.index]
            normal = self._parse_texture(model, gltf_normal, buffers)

        if gltf_material.pbrMetallicRoughness:
            property = gltf_material.pbrMetallicRoughness

            metallic_factor = property.metallicFactor or 0.0
            roughness_factor = property.metallicFactor or 0.0

            if property.baseColorTexture:
                gltf_albedo: gltf.Texture = model.textures[property.baseColorTexture.index]
                albedo = self._parse_texture(model, gltf_albedo, buffers)

            if property.baseColorFactor:
                albedo_color.x = property.baseColorFactor[0]
                albedo_color.y = property.baseColorFactor[1]
                albedo_color.z = property.baseColorFactor[2]

            if property.metallicRoughnessTexture:
                gltf_roughness: gltf.Texture = model.textures[property.metallicRoughnessTexture.index]
                metallic_roughness = self._parse_texture(model, gltf_roughness, buffers)

        if albedo:
            material_properties.set_texture(TextureType.albedo, albedo)
        if normal:
            material_properties.set_texture(TextureType.normal, normal)
        if metallic_roughness:
            material_properties.set_texture(TextureType.metallic_roughness, metallic_roughness)

        material_properties.set_scalar(ScalarType.metallic, metallic_factor)
        material_properties.set_scalar(ScalarType.roughness, roughness_factor)

        material_properties.add_color_property("albedo_col", ColorType.albedo, albedo_color)

        return material_properties

    def _parse_primitive(self: Self, model: gltf.GLTF2, node: gltf.Node, primitive: gltf.Primitive, buffers: list[bytes]) -> Mesh:

        att_accessors: dict[str, int] = dict()
        att_views: dict[str, int] = dict()
        attributes: list[Attribute] = []
        material: gltf.Material = None

        if primitive.attributes.POSITION is not None:
            att_accessors["POSITION"] = acc = model.accessors[primitive.attributes.POSITION]
            att_views["POSITION"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(AttributeType.POSITION, 0, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))
        if primitive.attributes.NORMAL is not None:
            att_accessors["NORMAL"] = acc = model.accessors[primitive.attributes.NORMAL]
            att_views["NORMAL"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(AttributeType.NORMAL, 1, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))
        if primitive.attributes.TANGENT is not None:
            att_accessors["TANGENT"] = acc = model.accessors[primitive.attributes.TANGENT]
            att_views["TANGENT"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(AttributeType.TANGENT, 2, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))
        if primitive.attributes.TEXCOORD_0 is not None:
            att_accessors["TEXCOORD_0"] = acc = model.accessors[primitive.attributes.TEXCOORD_0]
            att_views["TEXCOORD_0"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(AttributeType.TEX_COORD, 3, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))

        ind_acc = model.accessors[primitive.indices]
        ind_view = model.bufferViews[ind_acc.bufferView]

        # packed_data = buffers[packed_view.buffer][packed_view.byteOffset:packed_view.byteOffset + packed_view.byteLength]
        ind_data = buffers[ind_view.buffer][ind_view.byteOffset + ind_acc.byteOffset:ind_view.byteOffset + ind_view.byteLength]

        if primitive.material is not None:
            material = model.materials[primitive.material]

        return Mesh([BufferData(ind_data, gl.GL_ELEMENT_ARRAY_BUFFER),
                    BufferData(buffers[0], gl.GL_ARRAY_BUFFER, attributes)],
                    ind_acc.count,
                    ind_acc.componentType,
                    self._parse_material_properties(model, material, buffers))

    def _traverse_node(self: Self, gltf_node: gltf.Node, buffers: list[bytes], model: gltf.GLTF2, mesh_tree: NodeGraph, parent_node: Node[MeshNode]) -> None:

        mesh_list = list[Mesh]()

        if gltf_node.mesh is not None:
            mesh = model.meshes[gltf_node.mesh]
            for primitive in mesh.primitives:
                mesh_list.append(self._parse_primitive(model, gltf_node, primitive, buffers))

        pos = glm.vec3(0)
        rot = glm.vec3(0)
        scale = glm.vec3(1)

        if gltf_node.matrix:
            skew = glm.vec3(1)
            persp = glm.vec4(1)
            rot_quat = glm.quat()
            mat = glm.mat4(*gltf_node.matrix)
            glm.decompose(mat, scale, rot_quat, pos, skew, persp)
            rot = glm.eulerAngles(rot_quat)
        else:
            if gltf_node.translation:
                pos = glm.vec3(gltf_node.translation[0], gltf_node.translation[1], gltf_node.translation[2])
            if gltf_node.rotation:
                if len(gltf_node.rotation) == 4:
                    rot = glm.eulerAngles(glm.quat(gltf_node.rotation[0], gltf_node.rotation[1], gltf_node.rotation[2], gltf_node.rotation[3]))
                elif len(gltf_node.rotation) == 3:
                    rot = glm.vec3(gltf_node.rotation[0], gltf_node.rotation[1], gltf_node.rotation[2])
                else:
                    raise Exception("unsupported gltf rotation components")
            if gltf_node.scale:
                scale = glm.vec3(gltf_node.scale[0], gltf_node.scale[1], gltf_node.scale[2])

        transform = Transform(pos, rot, scale)
        tree_node: Node[MeshNode] = mesh_tree.add_node(MeshNode(mesh_list, transform, gltf_node.name), parent_node)

        for child in gltf_node.children:
            self._traverse_node(model.nodes[child], buffers, model, mesh_tree, tree_node)
