'''
Based on code from
Author: leovt (Leonhard Vogt)
License: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007
Example code for using glsl and vertex buffer objects with pyglet
'''
from ..output_node import UMOGOutputNode
from ... events import pyglet_helper
from . import pygl_test_impl

import threading
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()


class PyGLNode(UMOGOutputNode):
    bl_idname = "PyGLNode"
    bl_label = "3d Reaction Diffusion Node"

    feed = bpy.props.FloatProperty(default=0.014, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    kill = bpy.props.FloatProperty(default=0.046, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    Da = bpy.props.FloatProperty(default=0.2, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    Db = bpy.props.FloatProperty(default=0.09, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    dt = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    steps = bpy.props.IntProperty(default=2, min=1, step=500)
    channels = bpy.props.EnumProperty(items=
        (('0', 'R', 'Just do the reaction on one channel'),
         ('1', 'RGB', 'Do the reaction on all color channels'),
        ),
        name="channels")

    def init(self, context):
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "feed", "Feed")
        layout.prop(self, "kill", "Kill")
        layout.prop(self, "Da", "Da")
        layout.prop(self, "Db", "Db")
        layout.prop(self, "dt", "dt")
        layout.prop(self, "steps", "steps")
        layout.prop(self, "channels", "channels")
        
    def update(self):
        pass

    def preExecute(self, refholder):
        refholder.execution_scratch[self.name] = {}
        refholder.execution_scratch[self.name]["buffer"] = 0
        

    def execute(self, refholder):
        try:
            #start a new thread to avoid poluting blender's opengl context
            t = threading.Thread(target=pygl_test_impl.OffScreenRender, args=(self.steps,refholder.execution_scratch[self.name]["buffer"],
                refholder.execution_scratch[self.name]))
            t.start()
            t.join()
            print("OpenglRender done")
            #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
            print(refholder.execution_scratch[self.name]["buffer"])
        except:
            print("thread start failed")
            
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
        

    
