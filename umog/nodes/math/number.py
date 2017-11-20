from ..umog_node import *
from ...engine import types, engine
import numpy as np
import bpy

class NumberNode(UMOGNode):
    bl_idname = "umog_NumberNode"
    bl_label = "Number Node"

    value = bpy.props.FloatProperty(default=0.0)

    def init(self, context):
        self.outputs.new("FloatSocketType", "out")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="Value")

    def get_operation(self, input_types):
        return engine.Operation(
            engine.CONST,
            [types.Array(0,0,0,0,0,0)],
            [types.Array(0,0,0,0,0,0)],
            [engine.Argument(engine.ArgumentType.BUFFER, 0)],
            [])

    def get_buffer_values(self):
        return [np.array([self.value], dtype=np.float32, order="F").reshape((1,1,1,1,1))]

    def update(self):
        pass
