from ..engine_node import *
from ...engine import types, engine
import bpy

class OrNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_OrNode"
    bl_label = "Or Node"

    def init(self, context):
        self.inputs.new("BooleanSocketType", "a")
        self.inputs.new("BooleanSocketType", "b")
        self.outputs.new("BooleanSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        output_types = types.binary_scalar(input_types[0], input_types[1])

        return engine.Operation(
            engine.OR,
            input_types,
            output_types,
            [])

    def update(self):
        pass
