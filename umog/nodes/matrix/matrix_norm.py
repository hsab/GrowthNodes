from ..umog_node import *
from ...engine import types, engine
import bpy
import numpy as np
from numpy import linalg as la

class MatrixNormNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_MatrixNormNode"
    bl_label = "UMOG Matrix Norm"
                                         
    norms = bpy.props.EnumProperty(items=
                                            (('0', 'Frobenius Norm', 'F-norm'),
                                            ('1', '1-Norm', '1-norm'),
                                            ('2', '2-Norm', '2-norm'),
                                            ('3', 'Inf-Norm', 'inf-norm'),
                                            ),
                                            name="Norm Type")
    def init(self, context):
        self.outputs.new("ScalarSocketType", "out")
        self.inputs.new("ArraySocketType", "a")
        super().init(context)
        
    def get_operation(self, input_types):
        input_matrix = input_types[0]
        types.assert_type(input_matrix, types.ARRAY)
        
        if input_matrix.channels > 0 or input_matrix.z_size > 0:
            raise types.UMOGTypeError()
            
        output_types = [types.Array(0, 0, 0, 0, input_types[0].t_start, input_types[0].t_size)]
        
        if self.norms == 0:
            return engine.Operation(
                engine.MATRIX_NORM_FRO,
                input_types,
                output_types,
                [])
                
        elif self.norms == 1:
            return engine.Operation(
                engine.MATRIX_NORM_1,
                input_types,
                output_types,
                []) 
                
        elif self.norms == 2:
            return engine.Operation(
                engine.MATRIX_NORM_2,
                input_types,
                output_types,
                [])
                
        elif self.norms == 3:
            return engine.Operation(
                engine.MATRIX_NORM_INF,
                input_types,
                output_types,
                [])
            
    def draw_buttons(self, context, layout):
        layout.prop(self, "norms", 'Norm Type')
        
    def update (self):
        pass