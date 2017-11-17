from ..umog_node import *
from ...engine import types, engine
import bpy

class BooleanNode(UMOGNode):
    bl_idname = "umog_BooleanNode"
    bl_label = "Boolean Node"

    value = bpy.props.BoolProperty(default=False)

    def init(self, context):
        self.outputs.new("FloatSocketType", "out")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="Value")

    def get_operation(self, input_types):
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
