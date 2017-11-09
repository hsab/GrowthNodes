import bpy
import sys
import types
import numpy as np

from bpy.props import *
from ..base_types import UMOGSocket
from ..utils.events import propUpdate


class UMOGTexture3Data(dict):
    bl_idname = "umog_Texture3Data"

    def __init__(self):
        pass


class Texture3Socket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Float socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Texture3SocketType'
    # Label for nice name display
    bl_label = 'Texture3 Socket'
    dataType = "Texture3"
    allowedInputTypes = ["Texture3"]

    useIsUsedProperty = False
    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0.61372549, 0.117647059, 0.388235294, 1)


    data = UMOGTexture3Data()

    def drawProperty(self, context, layout, layoutParent, text, node):
        pass

    def pack(self):
        resolution = self.nodeTree.properties.TextureResolution
        if self.isOutput:
            pass
        else:
            self.data[self.identifier] = np.zeros((resolution, resolution, resolution), dtype = "float")

            

    def setPixels(self, newPixels):
        self.data[self.identifier] = newPixels

    def getPixels(self):
        return self.data[self.identifier]

    def refresh(self):
        self.name = self.identifier

    def destroy(self):
        if self.isPacked and self.identifier in self.data:
            del self.data[self.identifier]
