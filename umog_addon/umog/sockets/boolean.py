import bpy
import sys
from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.events import propUpdate


class BooleanSocket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Boolean socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'BooleanSocketType'
    # Label for nice name display
    bl_label = 'Boolean Socket'
    dataType = "Boolean"
    allowedInputTypes = ["Float", "Integer", "Boolean"]

    useIsUsedProperty = False

    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0.247058824, 0.317647059, 0.705882353, 1)

    value = BoolProperty(default=True, update=propUpdate)

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop(self, "value", text=text)
        pass

    def refresh(self):
        self.name = str(self.value)

    def getValue(self):
        return self.value

    def setProperty(self, data):
        if type(data) is bool:
            self.value = data
        else:
            self.value = data > 0 

    def getProperty(self):
        return self.value
