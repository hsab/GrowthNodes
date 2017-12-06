from ..engine_node import *
from ...engine import types, engine
import numpy as np
import bpy

class NumberNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_NumberNode"
    bl_label = "Number Node"

    value = bpy.props.FloatProperty(default=0.0)

    def init(self, context):
        self.outputs.new("ScalarSocketType", "out")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="Value")

    def get_operation(self, input_types):
        return engine.Operation(
            engine.CONST,
            [types.Array(0,0,0,0,0,0)],
            [types.Array(0,0,0,0,0,0)],
            [])

    def get_default_value(self, index, argument_type):
        return np.array([self.value], dtype=np.float32, order="F").reshape((1,1,1,1,1))

    def update(self):
        pass
