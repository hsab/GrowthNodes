import bpy
import sys
from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.events import propUpdate


def getIntValue(self):
    return min(max(self.minValue, self.get("value", 0)), self.maxValue)


def setIntValue(self, value):
    self["value"] = min(max(self.minValue, value), self.maxValue)

class IntegerSocket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Integer socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'IntegerSocketType'
    # Label for nice name display
    bl_label = 'Integer Socket'
    dataType = "Integer"
    allowedInputTypes = ["Float", "Integer", "Boolean"]

    useIsUsedProperty = False
    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0.29, 0.68, 0.31, 1)

    value = IntProperty(default=0,
                        set=setIntValue, get=getIntValue,
                        update=propUpdate)

    minValue = FloatProperty(default=-1e10)
    maxValue = FloatProperty(default=sys.float_info.max)

    # integer_value = bpy.props.IntProperty()

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop(self, "value", text=text)

    def refresh(self):
        self.name = str(self.value)

    def getValue(self):
        return self.value

    def setProperty(self, data):
        if type(data) is bool:
            self.value = int(data)
        elif type(data) is float:
            self.value = int(data)
        else:
            self.value = data

    def getProperty(self):
        return self.value

    def setRange(self, min, max):
        self.minValue = min
        self.maxValue = max
