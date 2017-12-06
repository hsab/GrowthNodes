import bpy
import sys
from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.events import propUpdate


def getFloatValue(self):
    return min(max(self.minValue, self.get("value", 0)), self.maxValue)


def setFloatValue(self, value):
    self["value"] = min(max(self.minValue, value), self.maxValue)


class FloatSocket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Float socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'FloatSocketType'
    # Label for nice name display
    bl_label = 'Float Socket'
    dataType = "Float"
    allowedInputTypes = ["Float", "Integer", "Boolean"]

    useIsUsedProperty = False
    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0.99, 0.59, 0, 1)

    value = FloatProperty(default=0.0,
                          set=setFloatValue, get=getFloatValue,
                          precision=6, update=propUpdate)

    minValue = FloatProperty(default=-1e10)
    maxValue = FloatProperty(default=sys.float_info.max)

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop(self, "value", text=text)

    def refresh(self):
        self.name = "{:.3f}".format(self.value)

    def getValue(self):
        return self.value

    def setProperty(self, data):
        if type(data) is bool:
            self.value = int(data)
        else:
            self.value = data

    def getProperty(self):
        return self.value

    def setRange(self, min, max):
        self.minValue = min
        self.maxValue = max
