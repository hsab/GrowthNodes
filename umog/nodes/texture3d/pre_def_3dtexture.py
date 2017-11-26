from ..umog_node import *


import threading
import sys
import bpy
import copy
import numpy as np

class UMOGTexture3ShapeNode(UMOGNode):
    bl_idname = "umog_Texture3ShapeNode"
    bl_label = "Voxel Creation Node"

    shapes = bpy.props.EnumProperty(items=
            (('0', 'Sphere', ''),
            ('1', 'Cylinder', ''),
            ),
            name="Shapes")
            
    height = bpy.props.FloatProperty(default=0.7, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    radius = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=0.5, step=1, precision=2)

    def init(self, context):
        self.outputs.new("TextureSocketType", "A'")

    def draw_buttons(self, context, layout):
        layout.prop(self, "shapes", "Shapes")
        layout.prop(self, "radius")
            
        if self.shapes == '1':
            layout.prop(self, "height")

    def get_operation(self, input_types):
        resolution = 256
        return engine.Operation(
            engine.SHAPE_GPU,
            [types.Array(resolution, resolution, resolution, 0, 0, 0)],
            [types.Array(2,0,0,0,0,0)],
            [engine.Argument(engine.ArgumentType.BUFFER, 0)],
            [resolution, int(self.shapes)])

    def get_buffer_values(self):
        return [np.array([self.height, self.radius], dtype=np.float32, order="F").reshape((2,1,1,1,1))]


            
