from ..umog_node import *
import bpy
import numpy as np

class GaussNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_GaussNode"
    bl_label = "Gaussian Blur"
    
    radius = bpy.props.IntProperty(default = 3)
    sigma = bpy.props.FloatProperty(default = 1.0)
    
    def init(self, context):
        self.outputs.new("ArraySocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "radius", text="Radius")
        layout.prop(self, "sigma", text="Sigma")

    def get_operation(self, input_types):
        size = self.radius
        return engine.Operation(
            engine.CONST,
            [types.Array(0,size,size,0,0,0)],
            [types.Array(0,size,size,0,0,0)],
            [])
            
    def get_default_value(self, index, argument_type):
    
        # generate matrix
        size = self.radius
        gauss_matrix = np.zeros((size, size), dtype=np.float)
        total = 0
        for i in range (-(size - 1)//2, (size - 1)//2 + 1):
            for j in range (-(size - 1)//2, (size - 1)//2 + 1):
                x0 = size//2
                y0 = size//2
                x = x0 + i
                y = y0 + j
                value = np.exp(-((x-x0)**2 + (y-y0)**2)/(2 * self.sigma**2))   
                gauss_matrix[x][y] =  value
                total += value
                
        # normalize matrix
        for i in range(0,size):
            for j in range(0,size):
                gauss_matrix[i][j] = gauss_matrix[i][j]/total
                
        return gauss_matrix.reshape((1,size,size,1,1))
  