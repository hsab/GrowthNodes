from ..umog_node import *
from ...engine import types, engine, mesh
import bpy

class ShowNumberNode(UMOGOutputNode):
    bl_idname = "umog_ShowNumberNode"
    bl_label = "Show Number Node"

    def value_changed(self, context):
        self.update()

    def get_value(self):
        return self.hidden_value

    hidden_value = bpy.props.FloatProperty(update=value_changed)
    value = bpy.props.FloatProperty(get=get_value)

    def init(self, context):
        self.inputs.new("FloatSocketType", "")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="value", emboss=False, slider=True)

    def get_operation(self, input_types):
        return engine.Operation(
            engine.OUT,
            [types.Scalar()],
            [],
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0)],
            [])

    def get_buffer_values(self):
        return []

    def output_value(self, value):
        self.hidden_value = value[0,0,0,0,0]

    def update(self):
        pass
