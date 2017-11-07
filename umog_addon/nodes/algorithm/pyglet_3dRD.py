'''
Based on code from
Author: leovt (Leonhard Vogt)
License: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007
Example code for using glsl and vertex buffer objects with pyglet
'''
from ... base_types import UMOGOutputNode
from . import pyglet_3dRD_impl

import threading
import sys
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()


class PyGLNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "PyGLNode"
    bl_label = "3d Reaction Diffusion Node"
    
    assignedType = "Texture2"
    
    texture = bpy.props.StringProperty()

    def init(self, context):
        self.newInput(self.assignedType, "A").isPacked = True
        self.newInput(self.assignedType, "B").isPacked = True
        self.newInput("Float", "Feed", value=0.055).isPacked = True
        self.newInput("Float", "Kill", value=0.062).isPacked = True
        self.newInput("Float", "A Rate", value=1.0).isPacked = True
        self.newInput("Float", "B Rate", value=0.5).isPacked = True
        self.newInput("Float", "Delta Time", value=1.0).isPacked = True
        self.newInput("Integer", "Steps", value=500).isPacked = True
        
        self.newOutput(self.assignedType, "A'").isPacked = True
        self.newOutput(self.assignedType, "B'").isPacked = True

    def draw(self, layout):
        pass
    
    def refresh(self):
        pass
        
    def update(self):
        pass

    def preExecute(self, refholder):
        refholder.execution_scratch[self.name] = {}
        refholder.execution_scratch[self.name]["buffer"] = 0
        

    def execute(self, refholder):
        temps = {}
        temps["A"] = self.inputs[0].getPixels()
        temps["B"] = self.inputs[1].getPixels()
        temps["feed"] = self.inputs[2].getValue()
        temps["kill"] = self.inputs[3].getValue()
        temps["dA"] = self.inputs[4].getValue()
        temps["dB"] = self.inputs[5].getValue()
        temps["dt"] = self.inputs[6].getValue()
        
        steps = self.inputs[-1].getValue()
        try:
            #start a new thread to avoid poluting blender's opengl context
            t = threading.Thread(target=pyglet_3dRD_impl.OffScreenRender, 
                                args=(steps, temps,))
            
            t.start()
            t.join()
            print("OpenglRender done")
            #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
            #print(temps["Aout"])
            
            self.outputs[0].setPackedImageFromPixels(temps["Aout"])
            self.outputs[1].setPackedImageFromPixels(temps["Bout"])
            self.inputs[0].setPixels(temps["Aout"])
            self.inputs[1].setPixels(temps["Bout"])
        except:
            print("thread start failed")
            print("Unexpected error:", sys.exc_info()[0])
        

    
