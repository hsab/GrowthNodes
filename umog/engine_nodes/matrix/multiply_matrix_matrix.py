from ..engine_node import *
from ...engine import types, engine
import bpy

class MultiplyMatrixMatrixNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_MultiplyMatrixMatrixNode"
    bl_label = "Matrix * Matrix"

    def init(self, context):
        self.inputs.new("ArraySocketType", "a")
        self.inputs.new("ArraySocketType", "b")
        self.outputs.new("ArraySocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        a, b = input_types
        types.assert_type(a, types.ARRAY)
        types.assert_type(b, types.ARRAY)

        if a.channels > 0 or b.channels > 0 or a.z_size > 0 or b.z_size > 0:
            raise types.EngineTypeError()

        if a.x_size == 0 or a.y_size == 0 or b.x_size == 0 or b.y_size == 0:
            raise types.EngineTypeError()

        if a.x_size != b.y_size:
            raise types.EngineTypeError()

        t_start, t_size = types.broadcast_time(a, b)

        output_types = [types.Array(0, b.x_size, a.y_size, 0, t_start, t_size)]

        return engine.Operation(
            engine.MULTIPLY_MATRIX_MATRIX,
            input_types,
            output_types,
            [])

    def update(self):
        pass
