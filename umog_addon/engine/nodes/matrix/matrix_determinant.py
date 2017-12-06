from ..engine_node import *
from ...engine import types, engine
import bpy
import numpy as np
from numpy import linalg as la

class MatrixDeterminantNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_MatrixDeterminantNode"
    bl_label = "Matrix Determinant"
    
    def init(self, context):
        self.outputs.new("ScalarSocketType", "out")
        self.inputs.new("ArraySocketType", "a")
        super().init(context)

    def get_operation(self, input_types):
        input_matrix = input_types[0]
        types.assert_type(input_matrix, types.ARRAY)
        
        if input_matrix.channels > 0 or input_matrix.z_size > 0:
            raise types.EngineTypeError()
            
        output_types = [types.Array(0, 0, 0, 0, input_types[0].t_start, input_types[0].t_size)]
        
        return engine.Operation(
            engine.MATRIX_DETERMINANT,
            input_types,
            output_types,
            []) 
        
    def update (self):
        pass