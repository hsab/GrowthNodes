import bpy
import sys
import types

from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.events import propUpdate
class Texture2Socket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Float socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Texture2SocketType'
    # Label for nice name display
    bl_label = 'Texture2 Socket'
    dataType = "Texture2"
    allowedInputTypes = ["Texture2"]

    useIsUsedProperty = False
    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0.91372549, 0.117647059, 0.388235294, 1)


    value = StringProperty(update = propUpdate)

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop_search(self, "value", bpy.data, "textures", icon="TEXTURE_DATA", text="")
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

    def getTexture(self):
        return bpy.data.textures[self.value]