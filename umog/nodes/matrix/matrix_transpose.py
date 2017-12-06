from ..umog_node import *
from ...engine import types, engine
import bpy
import numpy as np

class MatrixTransposeNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_MatrixTransposeNode"
    bl_label = "UMOG Matrix Transpose"
    
    def init(self, context):
        self.inputs.new("ArraySocketType", "a")
        self.outputs.new("ArraySocketType", "out")        
        super().init(context)

    def get_operation(self, input_types):    
        input_matrix = input_types[0]
        types.assert_type(input_matrix, types.ARRAY)
        
        if input_matrix.channels > 0 or input_matrix.z_size > 0:
            raise types.UMOGTypeError()
        
        output_types = [types.Array(input_matrix.channels, input_matrix.y_size, input_matrix.x_size, input_matrix.z_size, input_matrix.t_start, input_matrix.t_size)]
        
        return engine.Operation(
            engine.MATRIX_TRANSPOSE,
            input_types,
            output_types,
            [])
        
        #answer_matrix = np.transpose(input_matrix)

    def update (self):
        pass