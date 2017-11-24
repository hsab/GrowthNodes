from ..umog_node import *

import threading
import sys
import bpy
import copy
import numpy as np
#import pyximport
#pyximport.install()


class UMOGTexture3LatheNode(UMOGNode):
    bl_idname = "umog_Texture3LatheNode"
    bl_label = "Lathe Node"
    
    def init(self, context):
        self.inputs.new("TextureSocketType", "A")
        self.outputs.new("TextureSocketType", "A'")
        

    def draw_buttons(self, context, layout):
        pass

            
    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)
        print(input_types[0])
        return engine.Operation(
            engine.REACTION_DIFFUSION_GPU_STEP,
            [input_types[0]],
            [],
            [engine.Argument(engine.ArgumentType.SOCKET, 0),
             engine.Argument(engine.ArgumentType.SOCKET, 1),
             engine.Argument(engine.ArgumentType.BUFFER, 0)
             ],
            [1])

    def get_buffer_values(self):
        return []
