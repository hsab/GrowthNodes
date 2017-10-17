from ..umog_node import *
from ...engine import types, engine, mesh
import bpy

class GetMeshNode(UMOGNode):
    bl_idname = "umog_GetMeshNode"
    bl_label = "Get Mesh Node"

    mesh_name = bpy.props.StringProperty()

    def init(self, context):
        self.outputs.new("MeshSocketType", "out")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "mesh_name", bpy.data, "meshes", icon="MESH_CUBE", text="")

    def get_operation(self):
        return engine.Operation(
            engine.CONST,
            [],
            [types.Mesh()],
            [types.Mesh()],
            [])

    def get_buffer_values(self):
        return [mesh.from_blender_mesh(bpy.data.meshes[self.mesh_name])]

    def update(self):
        pass
