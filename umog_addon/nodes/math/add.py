from ..umog_node import UMOGNode
from ...engine import types, ops
import bpy

class AddNode(UMOGNode):
    bl_idname = "umog_AddNode"
    bl_label = "Add Node"

    def init(self, context):
        self.inputs.new("TextureSocketType", "a")
        self.inputs.new("TextureSocketType", "b")
        super().init(context)

    def input_types(self):
        return [types.Type.scalar(), types.Type.scalar()]

    def output_types(self):
        return [types.Type.scalar()]

    def operation(self):
        return ops.ADD

    def update(self):
        pass
