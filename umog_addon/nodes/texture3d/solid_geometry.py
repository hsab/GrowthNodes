from ... base_types import UMOGNode
from . import pyglet_sg_impl

import threading
import sys
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()


class UMOGTexture3SolidGeometryNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_Texture3SolidGeometryNode"
    bl_label = "Solid Geometry Node"
    
    geo_op = bpy.props.EnumProperty(items=
            (('difference', 'Difference', ''),
            ('similar', 'Similar', ''),
            ('union', 'Union', ''),
            ('intersect', 'Intersect', ''),
            ),
            name="Geometric Operations")
    threshold = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    
    def create(self):
        socket = self.newOutput(
            "Texture3", "Texture", drawOutput=False, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket.isPacked = True
        
        self.newInput("Texture3", "A").isPacked = True
        self.newInput("Texture3", "B").isPacked = True
        

    def draw(self, layout):
        layout.prop(self, "geo_op")
        layout.prop(self, "threshold", "Threshold")
        

    def execute(self, refholder):
        # print("get texture node execution, texture: " + self.texture)
        # print("texture handle: " + str(self.outputs[0].texture_index))
        # print(refholder.np2dtextures[self.outputs[0].texture_index])
        pass

    def preExecute(self, refholder):
        temps = {}
        temps["A"] = self.inputs[0].getPixels()
        temps["B"] = self.inputs[0].getPixels()
        temps["operation"] = self.geo_op
        temps["threshold"] = self.threshold
        
        try:
            #start a new thread to avoid poluting blender's opengl context
            t = threading.Thread(target=pyglet_sg_impl.OffScreenRender, 
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
