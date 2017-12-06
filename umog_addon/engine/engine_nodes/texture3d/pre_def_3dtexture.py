from ..engine_node import *


import threading
import sys
import bpy
import copy
import numpy as np

class EngineTexture3ShapeNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_Texture3ShapeNode"
    bl_label = "Voxel Creation Node"

    shapes = bpy.props.EnumProperty(items=
            (('0', 'Sphere', ''),
            ('1', 'Cylinder', ''),
            ),
            name="Shapes")
            
    height = bpy.props.FloatProperty(default=0.7, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    radius = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=0.5, step=1, precision=2)

    def init(self, context):
        self.outputs.new("ArraySocketType", "A'")

    def draw_buttons(self, context, layout):
        layout.prop(self, "shapes", "Shapes")
        layout.prop(self, "radius")
            
        if self.shapes == '1':
            layout.prop(self, "height")

    def get_operation(self, input_types):
        resolution = 256
        return engine.Operation(
            engine.SHAPE_GPU,
            [types.Array(2,0,0,0,0,0)],
            [types.Array(resolution, resolution, resolution, 0, 0, 0)],
            [resolution, int(self.shapes)])
    
    def get_default_value(self, index, argument_type):
        print("getting arguments " + str(index) + " h " + str(self.height) + " r " + str(self.radius))
        return np.array([self.height, self.radius], dtype=np.float32, order="F").reshape((2,1,1,1,1))

            
