
import array
import ctypes
import os
from typing import Self
import glm
import numpy
from pygame import Vector3
from gl.buffer_data import BufferData
from gl.texture import Sampler, Texture
from material import Material, TextureType
from mesh import Mesh
import pygltflib as gltf
from gl.attribute import Attribute
import OpenGL.GL as gl
from mesh_node import MeshNode
from node_graph import NodeGraph, Node
from transform import Transform


type_map = {
    "VEC4": 4,
    "VEC3": 3,
    "VEC2": 2,
    "SCALAR": 1,
}


class GltfLoader:
    def __init__(self: Self, filepath: str) -> None:
        self.filepath: str = filepath
        pass

    def load(self: Self) -> NodeGraph[MeshNode]:
        model: gltf.GLTF2 = gltf.GLTF2().load(self.filepath)
        mesh_tree: NodeGraph = NodeGraph[MeshNode]()

        buffers: list[bytes] = []
        for buffer in model.buffers:
            buffers.append(model.get_data_from_buffer_uri(buffer.uri))

        if len(model.scenes) != 1:
            raise Exception(f"unsupported number of scenes in {self.filepath}")

        for scene in model.scenes:
            self._traverse_node(model.nodes[scene.nodes[0]], buffers, model, mesh_tree, None)

        return mesh_tree

    def _parse_material(self: Self, model: gltf.GLTF2, gltf_material: gltf.Material) -> Material:

        material: Material = Material()
        albedo: Texture = None
        metallic_roughness: Texture = None

        if gltf_material.pbrMetallicRoughness:
            property = gltf_material.pbrMetallicRoughness
            if property.baseColorTexture:
                gltf_albedo: gltf.Texture = model.textures[property.baseColorTexture.index]
                gltf_sampler: gltf.Sampler = model.samplers[gltf_albedo.sampler]
                gltf_image: gltf.Image = model.images[gltf_albedo.source]

                sampler: Sampler = Sampler()
                sampler.tex_wrap_s = gltf_sampler.wrapS
                sampler.tex_wrap_t = gltf_sampler.wrapT
                sampler.tex_min_filter = gltf_sampler.minFilter
                sampler.tex_mag_filter = gltf_sampler.magFilter
                sampler.target = gl.GL_TEXTURE_2D

                albedo = Texture(os.path.join(os.path.dirname(self.filepath), gltf_image.uri), sampler)

            if property.metallicRoughnessTexture:
                gltf_roughness: gltf.Texture = model.textures[property.metallicRoughnessTexture.index]
                gltf_sampler: gltf.Sampler = model.samplers[gltf_roughness.sampler]
                gltf_image: gltf.Image = model.images[gltf_roughness.source]

                sampler: Sampler = Sampler()
                sampler.tex_wrap_s = gltf_sampler.wrapS
                sampler.tex_wrap_t = gltf_sampler.wrapT
                sampler.tex_min_filter = gltf_sampler.minFilter
                sampler.tex_mag_filter = gltf_sampler.magFilter
                sampler.target = gl.GL_TEXTURE_2D

                metallic_roughness = Texture(os.path.join(os.path.dirname(self.filepath), gltf_image.uri), sampler)

        if albedo:
            material.set_texture(TextureType.albedo, albedo)
        if metallic_roughness:
            material.set_texture(TextureType.metallic_roughness, metallic_roughness)

        return material

    def _parse_primitive(self: Self, model: gltf.GLTF2, node: gltf.Node, primitive: gltf.Primitive, buffers: list[bytes]) -> Mesh:

        att_accessors: dict[str, int] = dict()
        att_views: dict[str, int] = dict()
        attributes: list[Attribute] = []
        material: gltf.Material = model.materials[primitive.material]

        if primitive.attributes.POSITION is not None:
            att_accessors["POSITION"] = acc = model.accessors[primitive.attributes.POSITION]
            att_views["POSITION"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(0, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))
        if primitive.attributes.NORMAL is not None:
            att_accessors["NORMAL"] = acc = model.accessors[primitive.attributes.NORMAL]
            att_views["NORMAL"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(1, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))
        if primitive.attributes.TANGENT is not None:
            att_accessors["TANGENT"] = acc = model.accessors[primitive.attributes.TANGENT]
            att_views["TANGENT"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(2, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))
        if primitive.attributes.TEXCOORD_0 is not None:
            att_accessors["TEXCOORD_0"] = acc = model.accessors[primitive.attributes.TEXCOORD_0]
            att_views["TEXCOORD_0"] = view = model.bufferViews[acc.bufferView]
            attributes.append(Attribute(3, type_map[acc.type], acc.componentType, view.byteOffset + acc.byteOffset, view.byteStride))

        ind_acc = model.accessors[primitive.indices]
        ind_view = model.bufferViews[ind_acc.bufferView]

        # packed_data = buffers[packed_view.buffer][packed_view.byteOffset:packed_view.byteOffset + packed_view.byteLength]
        ind_data = buffers[ind_view.buffer][ind_view.byteOffset + ind_acc.byteOffset:ind_view.byteOffset + ind_view.byteLength]

        return Mesh([BufferData(ind_data, gl.GL_ELEMENT_ARRAY_BUFFER),
                    BufferData(buffers[0], gl.GL_ARRAY_BUFFER, attributes)],
                    ind_acc.count,
                    ind_acc.componentType,
                    self._parse_material(model, material))

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
            m = gltf_node.matrix
            mat = glm.mat4(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15])
            glm.decompose(mat, scale, rot_quat, pos, skew, persp)
            rot = glm.eulerAngles(rot_quat)
        else:
            if gltf_node.translation:
                pos = glm.vec3(gltf_node.translation[0], gltf_node.translation[1], gltf_node.translation[2])
            if gltf_node.rotation:
                rot = glm.vec3(gltf_node.rotation[0], gltf_node.rotation[1], gltf_node.rotation[2])
            if gltf_node.scale:
                scale = glm.vec3(gltf_node.scale[0], gltf_node.scale[1], gltf_node.scale[2])

        transform = Transform(pos, rot, scale)
        tree_node: Node[MeshNode] = mesh_tree.add_node(MeshNode(mesh_list, transform, gltf_node.name), parent_node)

        for child in gltf_node.children:
            self._traverse_node(model.nodes[child], buffers, model, mesh_tree, tree_node)
