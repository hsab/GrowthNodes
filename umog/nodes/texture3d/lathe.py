from ..umog_node import *

import threading
import sys
import bpy
import copy
import numpy as np
#import pyximport
#pyximport.install()


class UMOGTexture3LatheNode(UMOGOutputNode):
    bl_idname = "umog_Texture3LatheNode"
    bl_label = "Lathe Node"
    
    def init(self, context):
        self.inputs.new("TextureSocketType", "A")
        self.outputs.new("TextureSocketType", "A'")
        

    def draw_buttons(self, context, layout):
        pass

            
    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)
        print("input types")
        print(input_types[0])
        return engine.Operation(
            engine.LATHE_GPU,
            [input_types[0]],
            [types.Array(1,0,0,0,0,0)],
            [engine.Argument(engine.ArgumentType.SOCKET, 0)
             ],
            [1])

    def get_buffer_values(self):
        return [np.array([256], dtype=np.float32, order="F").reshape((1,1,1,1,1))]
