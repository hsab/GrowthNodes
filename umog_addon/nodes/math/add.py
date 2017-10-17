from ..umog_node import *
from ...engine import types, engine
import bpy

class AddNode(UMOGNode):
    bl_idname = "umog_AddNode"
    bl_label = "Add Node"

    def init(self, context):
        self.inputs.new("FloatSocketType", "a")
        self.inputs.new("FloatSocketType", "b")
        self.outputs.new("FloatSocketType", "out")
        super().init(context)

    def get_operation(self):
        return Operation(
            engine.ADD,
            [types.Scalar(), types.Scalar()],
            [types.Scalar()],
            [],
            [Argument(ArgumentType.SOCKET, 0), Argument(ArgumentType.SOCKET, 0)])

    def update(self):
        pass
