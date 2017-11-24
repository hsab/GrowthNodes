from ..umog_node import *

import threading
import sys
import bpy
import copy
import numpy as np

class UMOGTexture3TransformNode(UMOGNode):
    bl_idname = "umog_Texture3TransformNode"
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
        self.newInput("Texture3SocketType", "A").isPacked = True
        self.newOutput("Texture3SocketType", "Texture").isPacked = True

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
        engine.REACTION_DIFFUSION_GPU_STEP,
        [input_types[0]],
        [types.Array(6,0,0,0,0,0)],
        [engine.Argument(engine.ArgumentType.SOCKET, 0),
            engine.Argument(engine.ArgumentType.SOCKET, 1),
            engine.Argument(engine.ArgumentType.BUFFER, 0)
            ],
        [1])

def get_buffer_values(self):
    return [np.array([self.feed, self.kill, self.Da, self.Db, self.dt, self.iterations], dtype=np.float32, order="F").reshape((6,1,1,1,1))]
