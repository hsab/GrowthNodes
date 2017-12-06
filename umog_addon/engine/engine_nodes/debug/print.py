from ..engine_node import *
from ...engine import types, engine, mesh
import bpy

class PrintNode(bpy.types.Node, EngineOutputNode):
    bl_idname = "engine_PrintNode"
    bl_label = "Print Node"

    def init(self, context):
        self.inputs.new("ScalarSocketType", "value")
        super().init(context)

    def draw_buttons(self, context, layout):
        pass

    def get_operation(self, input_types):
        return engine.Operation(
            engine.OUT,
            input_types,
            [],
            [])

    def output_value(self, value):
        print(value)

    def update(self):
        pass
