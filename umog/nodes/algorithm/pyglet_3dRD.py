from ..umog_node import *
from . import pyglet_3dRD_impl

import threading
import sys
import bpy
import copy
import numpy as np

class PyGLNode(UMOGNode):
    bl_idname = "umog_PyGLNode"
    bl_label = "3d Reaction Diffusion Node"
    
    def create(self):
        print("pyglet create")
        self.newInput("Texture3SocketType", "A").isPacked = True
        self.newInput("Texture3SocketType", "B").isPacked = True
        self.newInput("FloatSocketType", "Feed", value=0.055).isPacked = True
        self.newInput("FloatSocketType", "Kill", value=0.062).isPacked = True
        self.newInput("FloatSocketType", "A Rate", value=1.0).isPacked = True
        self.newInput("FloatSocketType", "B Rate", value=0.5).isPacked = True
        self.newInput("FloatSocketType", "Delta Time", value=0.2).isPacked = True
        self.newInput("IntegerSocketType", "Steps", value=500).isPacked = True
        
        self.newOutput("Texture3SocketType", "A'").isPacked = True
        self.newOutput("Texture3SocketType", "B'").isPacked = True

    def refresh(self):
        pass
        
    def update(self):
        pass

    def preExecute(self, refholder):
        pass
        

    def execute(self, refholder):
        if self.inputs[0].isLinked and self.inputs[1].isLinked:
            temps = {}
            temps["A"] = self.inputs[0].links[0].from_socket.getPixels()
            temps["B"] = self.inputs[1].links[0].from_socket.getPixels()
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
                
                self.outputs[0].setPixels(temps["Aout"])
                self.outputs[1].setPixels(temps["Bout"])
                self.inputs[0].links[0].from_socket.setPixels(temps["Aout"])
                self.inputs[1].links[0].from_socket.setPixels(temps["Bout"])
            except:
                print("thread start failed")
                print("Unexpected error:", sys.exc_info()[0])
        else:
            print("not enough inputs")
            
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
        

    
