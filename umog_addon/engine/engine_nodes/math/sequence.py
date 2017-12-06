from ..engine_node import *
from ...engine import types, engine
import bpy

class TimeSequenceNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_TimeSequenceNode"
    bl_label = "Time Sequence Node"

    start = bpy.props.FloatProperty(default=0.0)
    end = bpy.props.FloatProperty(default=10.0)

    def init(self, context):
        self.outputs.new("ScalarSocketType", "out")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "start", text="Value")
        layout.prop(self, "end", text="Value")

    def get_operation(self, input_types):
        return engine.Operation(
            engine.CONST,
            [types.Array(1,1,1,1,int(self.start),int(self.end-self.start))],
            [types.Array(1,1,1,1,int(self.start),int(self.end-self.start))],
            [])

    def get_buffer_values(self, buffer_types):
        return [engine.sequence(self.start, self.end)]

    def update(self):
        pass
