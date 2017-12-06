from ..engine_node import *
from ...engine import types, engine, mesh
import bpy

class ShowNumberNode(bpy.types.Node, EngineOutputNode):
    bl_idname = "engine_ShowNumberNode"
    bl_label = "Show Number Node"

    def value_changed(self, context):
        self.update()

    def get_value(self):
        return self.hidden_value

    hidden_value = bpy.props.FloatProperty(update=value_changed)
    value = bpy.props.FloatProperty(get=get_value)

    def init(self, context):
        self.inputs.new("ScalarSocketType", "")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="value", emboss=False, slider=True)

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.OUT,
            input_types,
            [],
            [])

    def output_value(self, value):
        self.hidden_value = value.array[0,0,0,0,0]

    def update(self):
        pass
