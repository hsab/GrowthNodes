from ... base_types import UMOGNode
from . import pyglet_lathe_impl

import threading
import sys
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()


class UMOGTexture3LatheNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_LatheNode"
    bl_label = "2D Texture to Solid Texture (Lathe)"
    
    def create(self):
        socket = self.newOutput(
            "Texture3", "Texture", drawOutput=False, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket.isPacked = True
        self.newInput("Texture2", "A").isPacked = True
        

    def draw(self, layout):
        pass

    def execute(self, refholder):
        # print("get texture node execution, texture: " + self.texture)
        # print("texture handle: " + str(self.outputs[0].texture_index))
        # print(refholder.np2dtextures[self.outputs[0].texture_index])
        pass

    def preExecute(self, refholder):
        temps = {}
        temps["A"] = self.inputs[0].getPixels()
        temps["outResolution"] = self.nodeTree.properties.TextureResolution
        
        try:
            #start a new thread to avoid poluting blender's opengl context
            t = threading.Thread(target=pyglet_lathe_impl.OffScreenRender, 
                                args=(temps,))
            
            t.start()
            t.join()
            print("OpenglRender done")
            #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
            #print(temps["Aout"])
            
            self.outputs[0].setPixels(temps["Aout"])

        except:
            print("thread start failed")
            print("Unexpected error:", sys.exc_info()[0])
