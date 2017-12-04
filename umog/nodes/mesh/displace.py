from ..umog_node import *
from ...engine import types, engine
import bpy

class DisplaceNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_DisplaceNode"
    bl_label = "Displace Node"

    def init(self, context):
        self.inputs.new("MeshSocketType", "mesh")
        self.inputs.new("ArraySocketType", "texture")
        self.outputs.new("MeshSocketType", "out")
        super().init(context)

    def draw_buttons(self, context, layout):
        pass

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.MESH)
        types.assert_type(input_types[1], types.ARRAY)

        if input_types[0].t_size > 0:
            opcode = engine.DISPLACE_SEQUENCE
        else:
            opcode = engine.DISPLACE

        return engine.Operation(
            engine.DISPLACE,
            input_types,
            [input_types[0]],
            [])

    def update(self):
        pass
