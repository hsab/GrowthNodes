from ..umog_node import *
from . import pyglet_sg_impl

import threading
import sys
import bpy
import copy
import numpy as np

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
    
    def init(self, context):
        self.inputs.new("Texture3SocketType", "A")
        self.inputs.new("Texture3SocketType", "B")
        self.outputs.new("Texture3SocketType", "Texture")

    def draw_buttons(self, context, layout):
        layout.prop(self, "geo_op")
        layout.prop(self, "threshold", "Threshold")
        

    def execute(self, refholder):
        if self.inputs[0].isLinked and self.inputs[1].isLinked:
            temps = {}
            temps["A"] = self.inputs[0].links[0].from_socket.getPixels()
            temps["B"] = self.inputs[1].links[0].from_socket.getPixels()
            temps["operation"] = self.geo_op
            temps["threshold"] = self.threshold
            #pydevd.settrace()
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
                
        else:
            print("not enought inputs")

    def preExecute(self, refholder):
        pass
