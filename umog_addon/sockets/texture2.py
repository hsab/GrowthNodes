import bpy
import sys
import types
import numpy as np 

from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.events import propUpdate

class UMOGTextureProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_TextureProperties"


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


    value = StringProperty(update=propUpdate)

    _pixels = []

    def _setPixels(self, newPixels=None):
        self._pixels = newPixels

    def _getPixels(self):
        return self._pixels

    x = property(_getPixels, _setPixels, "I'm the 'x' property.")


    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop_search(self, "value", bpy.data,
                           "textures", icon="TEXTURE_DATA", text="")
        if self.value is not "":
            pass

    def pack(self):
        resolution = self.nodeTree.properties.TextureResolution
        if self.isOutput:
            D = bpy.data
            textureName = self.nodeTree.name + " - " + self.node.name + " - " + str(self.index)
            if textureName not in D.textures:
                texture = D.textures.new(textureName, "IMAGE")
            else:
                texture = D.textures[textureName]

            if textureName in D.images:
                D.images.remove(D.images[textureName])

            image = D.images.new(textureName, resolution,
                         resolution, alpha=False, float_buffer=True)

            texture.image = image
            self.value = texture.name

        else:
            rows = resolution
            columns = resolution
            # TODO: Fix harcoded channel attr
            pixels = np.empty( (rows, columns, 4), dtype="float" )

            fromTexture = self.getTexture()
            if fromTexture.type is not "IMAGE":
                for i in range(rows):
                    for j in range(columns):
                        # Mapping from -1 to 1 for evaluate
                        x = (i/rows)*2 -1
                        y = (j/columns)*2 -1
                        w = fromTexture.evaluate((y,x,0)).w
                        pixels[i,j][0]= w
                        pixels[i,j][1]= w
                        pixels[i,j][2]= w
                        pixels[i,j][3]= 1.0
            else:
                fromImage = texture.image
                fromRows = fromImage.size[1]
                fromColumns = fromImage.size[0]
                fromPixels = np.asarray( fromImage.pixels, dtype="float" )
                fromPixels = fromPixels.reshape(fromRows, fromColumns, fromImage.channels)

                for i in range(rows):
                    for j in range(columns):
                        # Scale image to resolution*resolution
                        x = i*(fromRows/rows)
                        y = j*(fromColumns/columns)
                        pixels[i,j][0]= fromPixels[x,y][0]
                        pixels[i,j][1]= fromPixels[x,y][1]
                        pixels[i,j][2]= fromPixels[x,y][2]
                        pixels[i,j][3]= fromPixels[x,y][3]
            
            self._setPixels(pixels)

    def setPackedImageFromPixels(self, newPixels):
        if self.isOutput and self.isPacked:
            texture = self.getTexture()
            image = texture.image
            image.pixels = newPixels.flatten()

    @classmethod
    def setPixels(self, newPixels):
        self.pixels = newPixels

    def getPixels(self):
        return self.pixels

    def getValue(self):
        return self.value

    def setProperty(self, data):
        self.value = data

    def getProperty(self):
        return self.value

    def refresh(self):
        self.name = self.value

    def getTexture(self):
        return bpy.data.textures[self.value]

    def destroy(self):
        self.pixels = None