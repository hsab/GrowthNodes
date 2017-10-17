from ..umog_node import *
from ...engine import types, engine
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

    def get_operation(self):
        return engine.Operation(
            engine.CONST,
            [],
            [types.Scalar()],
            [types.Scalar()],
            [engine.Argument(engine.ArgumentType.BUFFER, 0)])

    def get_buffer_values(self):
        return [self.value]

    def update(self):
        pass
