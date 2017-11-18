from ..umog_node import *
from ...engine import types, engine, mesh
import bpy

class PrintNode(UMOGOutputNode):
    bl_idname = "umog_PrintNode"
    bl_label = "Print Node"

    def init(self, context):
        self.inputs.new("FloatSocketType", "value")
        super().init(context)

    def draw_buttons(self, context, layout):
        pass

    def get_operation(self, input_types):
        return engine.Operation(
            engine.OUT,
            [],
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0)],
            [])

    def get_buffer_values(self):
        return []

    def output_value(self, value):
        print(value)

    def update(self):
        pass
