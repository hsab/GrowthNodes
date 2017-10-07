from ..output_node import UMOGOutputNode
from ... events import bgl_helper

import pyglet

import bpy
import copy
import numpy as np
import pyximport
pyximport.install()
from ...events import events



class PyGLNode(UMOGOutputNode):
    bl_idname = "PyGLNode"
    bl_label = "Reaction Diffusion Node"

    def init(self, context):
        super().init(context)

    def draw_buttons(self, context, layout):
        pass
        
    def update(self):
        pass

    def execute(self, refholder):
        tr = bpy.context.scene.TextureResolution
        print("begining execution " + str(tr))

        
        
def postBake(self, refholder):
        #TODO clean up the shader stuff
        pass
    
