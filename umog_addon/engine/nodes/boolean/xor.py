from ..engine_node import *
from ...engine import types, engine
import bpy

class XorNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_XorNode"
    bl_label = "Xor Node"

    def init(self, context):
        self.inputs.new("BooleanSocketType", "a")
        self.inputs.new("BooleanSocketType", "b")
        self.outputs.new("BooleanSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        output_types = types.binary_scalar(input_types[0], input_types[1])

        return engine.Operation(
            engine.XOR,
            input_types,
            output_types,
            [])

    def update(self):
        pass
