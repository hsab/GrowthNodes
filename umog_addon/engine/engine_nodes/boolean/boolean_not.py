from ..engine_node import *
from ...engine import types, engine
import bpy

class NotNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_NotNode"
    bl_label = "Not Node"

    def init(self, context):
        self.inputs.new("BooleanSocketType", "in")
        self.outputs.new("BooleanSocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.NOT,
            input_types,
            [input_types[0]],
            [])

    def update(self):
        pass
