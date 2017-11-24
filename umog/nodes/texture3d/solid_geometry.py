from ..umog_node import *


import threading
import sys
import bpy
import copy
import numpy as np

class UMOGTexture3SolidGeometryNode(UMOGNode):
    bl_idname = "umog_Texture3SolidGeometryNode"
    bl_label = "Solid Geometry Node"
    
    geo_op = bpy.props.EnumProperty(items=
            (('difference', 'Difference', ''),
            ('similar', 'Similar', ''),
            ('union', 'Union', ''),
            ('intersect', 'Intersect', ''),
            ),
            name="Geometric Operations")
    threshold = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    
    def init(self, context):
        self.newInput("Texture3SocketType", "A").isPacked = True
        self.newInput("Texture3SocketType", "B").isPacked = True
        self.newOutput("Texture3SocketType", "Texture").isPacked = True

    def draw_buttons(self, context, layout):
        layout.prop(self, "geo_op")
        layout.prop(self, "threshold", "Threshold")
        

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.REACTION_DIFFUSION_GPU_STEP,
            [input_types[0]],
            [types.Array(2,0,0,0,0,0)],
            [engine.Argument(engine.ArgumentType.SOCKET, 0),
             engine.Argument(engine.ArgumentType.SOCKET, 1),
             engine.Argument(engine.ArgumentType.BUFFER, 0)
             ],
            [1])

    def get_buffer_values(self):
        return [np.array([self.geo_op, self.threshold], dtype=np.float32, order="F").reshape((2,1,1,1,1))]
