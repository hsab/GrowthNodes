from ..umog_node import *
from ...engine import types, engine, mesh
import bpy

class SetMeshNode(UMOGOutputNode):
    bl_idname = "umog_SetMeshNode"
    bl_label = "Set Mesh Node"

    mesh_name = bpy.props.StringProperty()

    def init(self, context):
        self.inputs.new("MeshSocketType", "mesh")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "mesh_name", bpy.data, "meshes", icon="MESH_CUBE", text="")

    def get_operation(self):
        return engine.Operation(
            engine.OUT,
            [types.Mesh()],
            [],
            [],
            [])

    def get_buffer_values(self):
        return []

    def output_value(self, value):
        blender_mesh = bpy.data.meshes.new(self.mesh_name)
        vertices, edges, faces = mesh.to_pydata(value)
        blender_mesh.from_pydata(vertices, edges, faces)
        bpy.data.meshes[self.mesh_name].user_remap(blender_mesh)

    def update(self):
        pass
