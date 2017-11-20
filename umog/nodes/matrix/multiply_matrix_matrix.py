from ..umog_node import *
from ...engine import types, engine
import bpy

class MultiplyMatrixMatrixNode(UMOGNode):
    bl_idname = "umog_MultiplyMatrixMatrixNode"
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
            raise types.UMOGTypeError()

        if a.x_size == 0 or a.y_size == 0 or b.x_size == 0 or b.y_size == 0:
            raise types.UMOGTypeError()

        if a.x_size != b.y_size:
            raise types.UMOGTypeError()

        if a.t_start == b.t_start and a.t_size == b.t_size:
            t_start = a.t_start
            t_size = a.t_size
        elif a.t_size == 0:
            t_start = b.t_start
            t_size = b.t_size
        elif b.t_size == 0:
            t_start = a.t_start
            t_size = a.t_size
        else:
            raise UMOGTypeError()

        output_types = [types.Array(0, b.x_size, a.y_size, 0, t_start, t_size)]

        return engine.Operation(
            engine.MULTIPLY_MATRIX_MATRIX,
            output_types,
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0), engine.Argument(engine.ArgumentType.SOCKET, 1)],
            [])

    def update(self):
        pass
