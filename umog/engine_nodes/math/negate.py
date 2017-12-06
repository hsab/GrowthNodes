from ..engine_node import *
from ...engine import types, engine
import bpy

class NegateNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_NegateNode"
    bl_label = "Negate Node"

    def init(self, context):
        self.inputs.new("ScalarSocketType", "in")
        self.outputs.new("ScalarSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.NEGATE,
            input_types,
            [input_types[0]],
            [])

    def update(self):
        pass
