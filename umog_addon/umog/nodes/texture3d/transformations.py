from ... base_types import UMOGNode
from . import pyglet_tr_impl
from ....packages import transformations

import threading
import sys
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()

class UMOGTexture3TransformNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_SolidTextureTransformationmNode"
    bl_label = "Solid Texture Transformation"
    
    tr_op = bpy.props.EnumProperty(items=
            (('translation', 'Translation', ''),
            ('rotation', 'Rotation', ''),
            ('scale', 'Scale', ''),
            #('intersect', 'Intersect', ''),
            ),
            name="Transformations")
    
    direction = bpy.props.FloatVectorProperty()
    angle = bpy.props.FloatProperty()
    factor = bpy.props.FloatProperty()
    origin = bpy.props.FloatVectorProperty(default=(0.5,0.5,0.5))
    point = bpy.props.FloatVectorProperty(default=(0.5,0.5,0.5))
    
    def create(self):
        self.newInput("Texture3", "A").isPacked = True
        self.newOutput("Texture3", "Texture").isPacked = True

    def draw(self, layout):
        layout.prop(self, "tr_op")
        if self.tr_op == "translation":
            layout.prop(self, "direction", "Direction")
        elif self.tr_op == "rotation":
            layout.prop(self, "angle")
            layout.prop(self, "direction")
            layout.prop(self, "point")
        elif self.tr_op == "scale":
            layout.prop(self, "factor")
            layout.prop(self, "origin")
            #layout.prop(self, "direction")
        

    def execute(self, refholder):
        if self.inputs[0].isLinked:
            temps = {}
            temps["A"] = self.inputs[0].getFromSocket.getPixels()
            #set transform with the correct mat4
            if self.tr_op == "translation":
                temps["transform"] = transformations.translation_matrix(self.direction)
            elif self.tr_op == "rotation":
                temps["transform"] = transformations.rotation_matrix(self.angle, self.direction, self.point)
            elif self.tr_op == "scale":
                temps["transform"] = transformations.scale_matrix(self.factor, self.origin)
            else:
                print("no operation selected")
            print(temps["transform"])
            #pydevd.settrace()
            try:
                #start a new thread to avoid poluting blender's opengl context
                t = threading.Thread(target=pyglet_tr_impl.OffScreenRender, 
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
            #pydevd.settrace()
                
        else:
            print("not enought inputs")

    def preExecute(self, refholder):
        pass
