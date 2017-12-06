import bpy
import sys
import types
from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.events import propUpdate


class TemplateSocket(bpy.types.NodeSocket, UMOGSocket):
    '''Custom Float socket type'''

    bl_idname = 'TemplateSocketType'
    bl_label = 'Template Socket'
    dataType = "Template"
    allowedInputTypes = ["All"]

    isRefreshable = True
    isPacked = False
    useIsUsedProperty = False

    defaultDrawType = "TEXT_PROPERTY"
    drawOutput = False
    drawColor = (0, 0, 0, 0.5)

    texture = StringProperty(update=propUpdate)

    def addTextureToContext(self, context):
        context.texture = self.texture

    def drawProperty(self, context, layout, layoutParent, text, node):
        pass

    def setProperty(self, data):
        pass

    def getProperty(self):
        pass

    def refresh(self):
        pass
