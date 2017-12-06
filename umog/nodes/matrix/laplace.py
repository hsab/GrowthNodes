from ..umog_node import *
from ...engine import types, engine
import bpy
import numpy as np

class LaplaceNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_LaplaceNode"
    bl_label = "Laplace Kernel"

    bl_width_default = 150
    radius = bpy.props.IntProperty(default = 3, step = 2, min = 3)
    dimension = bpy.props.EnumProperty(items=
                                            (('0', '1D', '1D'),
                                            ('1', '2D', '2D'),
                                            ('2', '3D', '3D'),
                                            ),
                                            name="Dimensions")

    def init(self, context):
        self.outputs.new("ArraySocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "radius", text="Radius")

    def get_operation(self, input_types):
        size = self.radius
        
        if self.dimension == '0':
            return engine.Operation(
                engine.CONST,
                [types.Array(0,size,0,0,0,0)],
                [types.Array(0,size,0,0,0,0)],
                [])
        elif self.dimension == '1':
            return engine.Operation(
                engine.CONST,
                [types.Array(0,size,size,0,0,0)],
                [types.Array(0,size,size,0,0,0)],
                [])
        elif self.dimension == '2':
            return engine.Operation(
                engine.CONST,
                [types.Array(0,size,size,size,0,0)],
                [types.Array(0,size,size,size,0,0)],
                [])

    def get_default_value(self, index, argument_type):
    
        size = self.radius
        laplace_matrix = np.ones((size, size), dtype=np.float32, order="F")
        
        center = size // 2
        laplace_matrix[center][center] = 1 - (size * size)
        
        return laplace_matrix.reshape((1,size,size,1,1))
