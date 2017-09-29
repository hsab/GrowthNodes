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
    defaultDrawType = "TEXT_PROPERTY"

    drawColor = (1, 0, 1, 0.5)

    comparable = True
    storable = True

    value = FloatProperty(default = 0.0, update = propUpdate)

    minValue = FloatProperty(default = -1e10)
    maxValue = FloatProperty(default = sys.float_info.max)

    def drawProperty(self, context, layout, text, node):
        layout.prop(self, "value", text = text)

    def getValue(self):
        return self.value

    def setProperty(self, data):
        self.value = data

    def getProperty(self):
        return self.value

    def refresh(self):
        print("refresh from socket", self.name, self.node)