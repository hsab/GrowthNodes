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
    defaultDrawType = "TEXT_PROPERTY"

    drawColor = (1, 0, 0, 0.5)

    comparable = False
    storable = True

    texture = StringProperty(update = propUpdate)

    def addTextureToContext(self, context):
        context.texture = self.texture

    def drawProperty(self, context, layout, text, node):
        layout.prop_search(self, "texture", bpy.data, "textures", icon="TEXTURE_DATA", text="")
        if self.texture is not "":
           pass

    def getValue(self):
        pass

    def setProperty(self, data):
        self.texture = data

    def getProperty(self):
        return self.texture


    def refresh(self):
        pass