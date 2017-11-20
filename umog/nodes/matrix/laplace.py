from ..umog_node import *
from ...engine import types, engine
import bpy
import numpy as np

class LaplaceNode(UMOGNode):
    bl_idname = "umog_LaplaceNode"
    bl_label = "Laplace Kernel"

    bl_width_default = 150

    def init(self, context):
        self.outputs.new("ArraySocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        pass

    def get_operation(self, input_types):
        return engine.Operation(
            engine.CONST,
            [types.Array(0,3,3,0,0,0)],
            [types.Array(0,3,3,0,0,0)],
            [engine.Argument(engine.ArgumentType.BUFFER, 0)],
            [])

    def get_buffer_values(self):
        return [np.array([[0.25, 0.5, 0.25], [0.5, -3, 0.5], [0.25, 0.5, 0.25]], dtype=np.float32, order="F").reshape((1,3,3,1,1))]
