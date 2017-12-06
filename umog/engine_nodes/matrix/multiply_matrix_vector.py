from ..engine_node import *
from ...engine import types, engine
import bpy

class MultiplyMatrixVectorNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_MultiplyMatrixVectorNode"
    bl_label = "Matrix * Vector"

    def init(self, context):
        self.inputs.new("ArraySocketType", "a")
        self.inputs.new("ArraySocketType", "b")
        self.outputs.new("ArraySocketType", "out")
        super().init(context)

    def get_operation(self, input_types):
        matrix, vector = input_types
        types.assert_type(matrix, types.ARRAY)
        types.assert_type(vector, types.ARRAY)

        if matrix.channels > 0 or matrix.z_size > 0:
            raise types.EngineTypeError()

        if matrix.x_size != vector.channels:
            raise types.EngineTypeError()

        t_start, t_size = types.broadcast_time(matrix, vector)

        output_types = [types.Array(matrix.y_size, vector.x_size, vector.y_size, vector.z_size, t_start, t_size)]

        return engine.Operation(
            engine.MULTIPLY_MATRIX_MATRIX,
            input_types,
            output_types,
            [])

    def update(self):
        pass
