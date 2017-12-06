from ..engine_node import *


import threading
import sys
import bpy
import copy
import numpy as np

class EngineTexture3SolidGeometryNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_Texture3SolidGeometryNode"
    bl_label = "Solid Geometry Node"
    
    geo_op = bpy.props.EnumProperty(items=
            (('0', 'Difference', ''),
            ('1', 'Similar', ''),
            ('2', 'Union', ''),
            ('3', 'Intersect', ''),
            ),
            name="Geometric Operations")
    threshold = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    
    def init(self, context):
        self.inputs.new("ArraySocketType", "A")
        self.inputs.new("ArraySocketType", "B")
        self.outputs.new("ArraySocketType", "A'")

    def draw_buttons(self, context, layout):
        layout.prop(self, "geo_op")
        layout.prop(self, "threshold", "Threshold")
        

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)
        types.assert_type(input_types[1], types.ARRAY)

        return engine.Operation(
            engine.SOLID_GEOMETRY_GPU,
            [input_types[0], input_types[1], types.Array(1,0,0,0,0,0)],
            [input_types[0]],
            [int(self.geo_op)])

    def get_default_value(self, index, argument_type):
        return np.array([ self.threshold], dtype=np.float32, order="F").reshape((1,1,1,1,1))
