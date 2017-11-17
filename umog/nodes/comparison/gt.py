from ..umog_node import *
from ...engine import types, engine
import bpy

class GreaterThanNode(UMOGNode):
    bl_idname = "umog_GreaterThanNode"
    bl_label = "Greater Than Node"

    def init(self, context):
        self.inputs.new("FloatSocketType", "a")
        self.inputs.new("FloatSocketType", "b")
        self.outputs.new("FloatSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        return engine.Operation(
            engine.GT,
            [types.Scalar(), types.Scalar()],
            [types.Scalar()],
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0), engine.Argument(engine.ArgumentType.SOCKET, 1)])

    def update(self):
        pass
