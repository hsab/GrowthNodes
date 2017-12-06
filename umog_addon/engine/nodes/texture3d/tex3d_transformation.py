from ..engine_node import *

import threading
import sys
import bpy
import copy
import numpy as np
from ....packages import transformations

class EngineTexture3TransformNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_Texture3TransformNode"
    bl_label = "Transform Node"
    
    tr_op = bpy.props.EnumProperty(items=
            (('translation', 'Translation', ''),
            ('rotation', 'Rotation', ''),
            ('scale', 'Scale', ''),
            #('intersect', 'Intersect', ''),
            ),
            name="Transformations")
    
    direction = bpy.props.FloatVectorProperty()
    angle = bpy.props.FloatProperty()
    factor = bpy.props.FloatProperty()
    origin = bpy.props.FloatVectorProperty(default=(0.5,0.5,0.5))
    point = bpy.props.FloatVectorProperty(default=(0.5,0.5,0.5))
    
    def init(self, context):
        self.inputs.new("ArraySocketType", "A")
        self.outputs.new("ArraySocketType", "A'")

    def draw_buttons(self, context, layout):
        layout.prop(self, "tr_op")
        if self.tr_op == "translation":
            layout.prop(self, "direction", "Direction")
        elif self.tr_op == "rotation":
            layout.prop(self, "angle")
            layout.prop(self, "direction")
            layout.prop(self, "point")
        elif self.tr_op == "scale":
            layout.prop(self, "factor")
            layout.prop(self, "origin")
            #layout.prop(self, "direction")
        

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.TRANSFORM_GPU,
            [input_types[0], types.Array(4,4,0,0,0,0)],
            input_types,
            [])

    def get_default_value(self, index, argument_type):
        if self.tr_op == "translation":
            transform = transformations.translation_matrix(self.direction)
        elif self.tr_op == "rotation":
            transform = transformations.rotation_matrix(self.angle, self.direction, self.point)
        elif self.tr_op == "scale":
            transform = transformations.scale_matrix(self.factor, self.origin)
        else:
            print("no operation selected")
        
        return np.array(transform, dtype=np.float32, order="F").reshape((4,4,1,1,1))
