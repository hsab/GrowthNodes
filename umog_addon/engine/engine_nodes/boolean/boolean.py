from ..engine_node import *
from ...engine import types, engine
import bpy

class BooleanNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_BooleanNode"
    bl_label = "Boolean Node"

    value = bpy.props.BoolProperty(default=False)

    def init(self, context):
        self.outputs.new("BooleanSocketType", "out")
        super().init(context)

    def draw_buttons(self, context, layout):
        if self.value:
            text = "true"
        else:
            text = "false"
        layout.prop(self, "value", text=text)

    def get_operation(self, input_types):
        return engine.Operation(
            engine.CONST,
            [types.Array(0,0,0,0,0,0)],
            [types.Array(0,0,0,0,0,0)],
            [])

    def get_default_value(self, index, argument_type):
        return np.array([float(self.value)], dtype=np.float32, order="F").reshape((1,1,1,1,1))

    def update(self):
        pass
