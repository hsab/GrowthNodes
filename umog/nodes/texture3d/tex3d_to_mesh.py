from ..umog_node import *


import threading
import sys
import bpy
import copy
import numpy as np

class UMOGTexture3MeshNode(UMOGNode):
    bl_idname = "umog_Texture3MeshNode"
    bl_label = "Mesh 3d Texture Node"
    
    mesh_name = bpy.props.StringProperty()
    
    iso_level = bpy.props.FloatProperty(default=0, soft_min=0.0, step=1, precision=2)
    
    def init(self, context):
        self.inputs.new("TextureSocketType", "A")

    def draw_buttons(self, context, layout):
        layout.prop(self, "mesh_name")
        layout.prop(self, "iso_level", "Iso Level")
        

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.REACTION_DIFFUSION_GPU_STEP,
            [input_types[0], input_types[0]],
            [types.Array(2,0,0,0,0,0)],
            [engine.Argument(engine.ArgumentType.SOCKET, 0),
            engine.Argument(engine.ArgumentType.SOCKET, 1),
            engine.Argument(engine.ArgumentType.BUFFER, 0)
            ],
            [1])

    def get_buffer_values(self):
        return [np.array([self.iso_level, self.mesh_name], dtype=np.float32, order="F").reshape((2,1,1,1,1))]

