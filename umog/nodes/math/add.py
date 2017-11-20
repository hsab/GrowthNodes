from ..umog_node import *
from ...engine import types, engine
import bpy

class AddNode(UMOGNode):
    bl_idname = "umog_AddNode"
    bl_label = "Add Node"

    default_a = bpy.props.FloatProperty(default = 0.0)

    def init(self, context):
        a = self.inputs.new("FloatSocketType", "a")
        a.value_path = "default_a"
        self.inputs.new("FloatSocketType", "b")
        self.outputs.new("FloatSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        output_types = types.binary_scalar(input_types[0], input_types[1])

        return engine.Operation(
            engine.ADD,
            output_types,
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0), engine.Argument(engine.ArgumentType.SOCKET, 1)],
            [])

    def update(self):
        pass
