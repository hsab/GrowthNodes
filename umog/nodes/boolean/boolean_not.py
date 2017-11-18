from ..umog_node import *
from ...engine import types, engine
import bpy

class NotNode(UMOGNode):
    bl_idname = "umog_NotNode"
    bl_label = "Not Node"

    def init(self, context):
        self.inputs.new("FloatSocketType", "in")
        self.outputs.new("FloatSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.NOT,
            [input_types[0]],
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0,
            [])],
            [])

    def update(self):
        pass
