from ..umog_node import *


import threading
import sys
import bpy
import copy
import numpy as np

class UMOGTexture3ShapeNode(UMOGNode):
    bl_idname = "umog_Texture3ShapeNode"
    bl_label = "Texture Node"

    shapes = bpy.props.EnumProperty(items=
            (('0', 'Sphere', ''),
            ('1', 'Cylinder', ''),
            ),
            name="Shapes")
            
    height = bpy.props.FloatProperty(default=0.7, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    radius = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=0.5, step=1, precision=2)

    def init(self, context):
        socket = self.newOutput(
            "Texture3", "Texture", drawOutput=False, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "shapes", "Shapes")
        layout.prop(self, "radius")
            
        if self.shapes == '1':
            layout.prop(self, "height")

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.REACTION_DIFFUSION_GPU_STEP,
            [input_types[0], input_types[0]],
            [types.Array(6,0,0,0,0,0)],
            [engine.Argument(engine.ArgumentType.SOCKET, 0),
             engine.Argument(engine.ArgumentType.SOCKET, 1),
             engine.Argument(engine.ArgumentType.BUFFER, 0)
             ],
            [1])

    def get_buffer_values(self):
        return [np.array([self.height, self.radius, self.shapes], dtype=np.float32, order="F").reshape((4,1,1,1,1))]


            
