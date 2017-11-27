from ..umog_node import *
from ...engine import types, engine, mesh
import bpy

class SetMeshNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SetMeshNode"
    bl_label = "Set Mesh Node"

    mesh_name = bpy.props.StringProperty()

    def init(self, context):
        self.inputs.new("MeshSocketType", "mesh")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "mesh_name", bpy.data, "meshes", icon="MESH_CUBE", text="")

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.MESH)

        return engine.Operation(
            engine.OUT,
            input_types,
            [],
            [])

    def output_value(self, value):
        mesh.to_blender_mesh(value, bpy.data.meshes[self.mesh_name].as_pointer())
        bpy.data.meshes[self.mesh_name].update()

    def update(self):
        pass
