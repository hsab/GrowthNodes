from ..umog_node import *
from ...engine import types, engine
import bpy

class DivideNode(UMOGNode):
    bl_idname = "umog_DivideNode"
    bl_label = "Divide Node"

    def init(self, context):
        self.inputs.new("FloatSocketType", "a")
        self.inputs.new("FloatSocketType", "b")
        self.outputs.new("FloatSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        output_types = types.binary_scalar(input_types[0], input_types[1])

        return engine.Operation(
            engine.DIVIDE,
            output_types,
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0), engine.Argument(engine.ArgumentType.SOCKET, 1)],
            [])

    def update(self):
        pass
