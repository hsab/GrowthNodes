'''
Based on code from
Author: leovt (Leonhard Vogt)
License: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007
Example code for using glsl and vertex buffer objects with pyglet
'''
from ... base_types import UMOGOutputNode
from . import pyglet_test_impl

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
    
    #feed = bpy.props.FloatProperty(default=0.014, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    #kill = bpy.props.FloatProperty(default=0.046, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    #Da = bpy.props.FloatProperty(default=0.2, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    #Db = bpy.props.FloatProperty(default=0.09, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    #dt = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    #steps = bpy.props.IntProperty(default=2, min=1, step=500)
    channels = bpy.props.EnumProperty(items=
        (('0', 'R', 'Just do the reaction on one channel'),
         ('1', 'RGB', 'Do the reaction on all color channels'),
        ),
        name="channels")

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
            t = threading.Thread(target=pyglet_test_impl.OffScreenRender, 
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
            
    #def execute(self, refholder):
        #try:
            ##start a new thread to avoid poluting blender's opengl context
            #p = Process(target=OffScreenRender, args=(self.steps,refholder.execution_scratch[self.name]["buffer"],refholder.execution_scratch[self.name]["buffer"]))
            
            ##p = Process(target=Dummy, args=(self.steps,refholder.execution_scratch[self.name]["buffer"], refholder.execution_scratch[self.name]["buffer"]))
            
            #p.start()
            #p.join()
            #print("OpenglRender done")
            #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
            #print(buf)
        #except:
            #print("process failed")
        

    
