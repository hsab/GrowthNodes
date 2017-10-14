import bpy
import sys
import types

from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.events import propUpdate
class ObjectSocket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Object socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'ObjectSocketType'
    # Label for nice name display
    bl_label = 'Object Socket'
    dataType = "Object"
    allowedInputTypes = ["Object"]

    useIsUsedProperty = False
    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0, 0.588235294, 0.533333333, 1)


    value = StringProperty(update = propUpdate)

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop_search(self, "value", bpy.data, "objects", icon="MESH_CUBE", text="")
        if self.value is not "":
           pass

    def getValue(self):
        pass

    def setProperty(self, data):
        self.value = data

    def getProperty(self):
        return self.value

    def refresh(self):
        self.name = self.value

    def getObject(self):
        return bpy.data.objects[self.value]