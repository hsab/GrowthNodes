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
            (('0', 'Difference', ''),
            ('1', 'Similar', ''),
            ('2', 'Union', ''),
            ('3', 'Intersect', ''),
            ),
            name="Geometric Operations")
    threshold = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    
    def init(self, context):
        self.inputs.new("TextureSocketType", "A")
        self.inputs.new("TextureSocketType", "B")
        self.outputs.new("TextureSocketType", "A'")

    def draw_buttons(self, context, layout):
        layout.prop(self, "geo_op")
        layout.prop(self, "threshold", "Threshold")
        

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)
        types.assert_type(input_types[1], types.ARRAY)

        return engine.Operation(
            engine.SOLID_GEOMETRY_GPU,
            [input_types[0]],
            [types.Array(1,0,0,0,0,0)],
            [engine.Argument(engine.ArgumentType.SOCKET, 0),
             engine.Argument(engine.ArgumentType.SOCKET, 1),
             engine.Argument(engine.ArgumentType.BUFFER, 0)
             ],
            [int(self.geo_op)])

    def get_buffer_values(self):
        return [np.array([ self.threshold], dtype=np.float32, order="F").reshape((1,1,1,1,1))]
