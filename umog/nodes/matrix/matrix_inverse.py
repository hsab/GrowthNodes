from ..umog_node import *
from ...engine import types, engine
import bpy
import numpy as np
from numpy import linalg as la

class MatrixInverseNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_MatrixInverseNode"
    bl_label = "UMOG Matrix Inverse"
    bl_width_min = 200
    
    def init(self, context):
        self.outputs.new("ArraySocketType", "out")
        self.inputs.new("ArraySocketType", "a")
        super().init(context)
        
    def get_operation(self, input_types):    
        input_matrix = input_types[0]
        types.assert_type(input_matrix, types.ARRAY)
        
        if input_matrix.channels > 0 or input_matrix.z_size > 0:
            raise types.UMOGTypeError()
            
        if input_matrix.x_size != input_matrix.y_size:
            raise types.UMOGTypeError()
        
        output_types = [types.Array(input_matrix.channels, input_matrix.x_size, input_matrix.y_size, input_matrix.z_size, input_matrix.t_start, input_matrix.t_size)]
        
        return engine.Operation(
            engine.MATRIX_INVERSE,
            input_types,
            output_types,
            [])
        
    def update (self):
        pass

    # def execute(self, refholder):
    
        # input_matrix = refholder.matrices[self.inputs[0].links[0].from_socket.matrix_ref]
        # answer_matrix = np.zeros(16)
            
        # if la.det(input_matrix) == 0:
            # print("Matrix has no inverse")
        # else:
            # answer_matrix = la.inv(input_matrix)
    
        # self.outputs[0].matrix_ref = refholder.getRefForMatrix(answer_matrix) 