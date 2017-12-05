from ... base_types import UMOGNode
from . import pyglet_cr_sphere_impl

import threading
import sys
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()


class UMOGTexture3ShapeNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_SolidTextureNode"
    bl_label = "Shape Texture"

    shapes = bpy.props.EnumProperty(items=
            (('0', 'Sphere', ''),
            ('1', 'Cylinder', ''),
            ),
            name="Shapes")
            
    height = bpy.props.FloatProperty(default=0.7, soft_min=0.0, soft_max=1.0, step=1, precision=2)
    radius = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=0.5, step=1, precision=2)

    def create(self):
        socket = self.newOutput(
            "Texture3", "Texture", drawOutput=False, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def draw(self, layout):
        layout.prop(self, "shapes", "Shapes")
        layout.prop(self, "radius")
            
        if self.shapes == '1':
            layout.prop(self, "height")

    def execute(self, refholder):
        # print("get texture node execution, texture: " + self.texture)
        # print("texture handle: " + str(self.outputs[0].texture_index))
        # print(refholder.np2dtextures[self.outputs[0].texture_index])
        pass

    def preExecute(self, refholder):
        temps = {}
        if self.shapes == '0':
            temps["shape"] = "sphere"
        elif self.shapes == '1':
            temps["shape"] = "cylinder"
        temps["center"] = (0.5,0.5,0.5)

        temps["height"] = self.height
        temps["radius"] = self.radius
        temps["resolution"] = self.nodeTree.properties.TextureResolution
        try:
            #start a new thread to avoid poluting blender's opengl context
            t = threading.Thread(target=pyglet_cr_sphere_impl.OffScreenRender, 
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
            
