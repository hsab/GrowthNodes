import bpy
import sys
import types
import numpy as np

from bpy.props import *
from ..base_types import UMOGSocket
from ..utils.events import propUpdate


class UMOGTextureData(dict):
    bl_idname = "umog_TextureData"

    def __init__(self):
        pass


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

    data = UMOGTextureData()

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop_search(self, "value", bpy.data, "textures", icon = "TEXTURE_DATA",
                           text = "")
        if self.value is not "":
            pass

    def pack(self):
        resolution = self.nodeTree.properties.TextureResolution
        if self.isOutput:
            self.initOutputData(resolution)
        else:
            self.packInputData(resolution)

    def initOutputData(self, resolution):
        D = bpy.data
        textureName = self.nodeTree.name + " - " + self.node.name + " - " + str(
            self.index)
        if textureName not in D.textures:
            texture = D.textures.new(textureName, "IMAGE")
        else:
            texture = D.textures[textureName]

        if textureName in D.images:
            D.images.remove(D.images[textureName])

        image = D.images.new(textureName, resolution, resolution, alpha = False,
                             float_buffer = True)

        texture.image = image
        self.value = texture.name

    def packInputData(self, resolution):
        rows = resolution
        columns = resolution
        # TODO: Fix harcoded channel attr
        pixels = np.empty((rows, columns, 4), dtype = "float")
        fromTexture = self.getTexture()

        if fromTexture.type != "IMAGE":
            self.proceduralToNumpy(fromTexture, pixels, rows, columns)
        else:
            self.imageToNumpy(fromTexture, pixels, rows, columns)

        self.data[self.identifier] = pixels

    def proceduralToNumpy(self, fromTexture, pixels, rows, columns):
        for i in range(rows):
            for j in range(columns):
                # Mapping from -1 to 1 for evaluate
                x = (i / rows) * 2 - 1
                y = (j / columns) * 2 - 1
                w = fromTexture.evaluate((y, x, 0)).w
                pixels[i, j][0] = w
                pixels[i, j][1] = w
                pixels[i, j][2] = w
                pixels[i, j][3] = 1.0

        return pixels

    def imageToNumpy(self, fromTexture, pixels, rows, columns):
        fromImage = fromTexture.image
        fromRows = fromImage.size[1]
        fromColumns = fromImage.size[0]
        fromPixels = np.asarray(fromImage.pixels, dtype = "float")
        fromPixels = fromPixels.reshape(fromRows, fromColumns, fromImage.channels)

        for i in range(rows):
            for j in range(columns):
                # Scale image to resolution*resolution
                x = int(i * (fromRows / rows))
                y = int(j * (fromColumns / columns))
                pixels[i, j][0] = fromPixels[x, y][0]
                pixels[i, j][1] = fromPixels[x, y][1]
                pixels[i, j][2] = fromPixels[x, y][2]
                pixels[i, j][3] = fromPixels[x, y][3]

        return pixels

    def setPackedImageFromPixels(self, newPixels, flatten=True):
        if self.isOutput and self.isPacked:
            texture = self.getTexture()
            image = texture.image
            if flatten:
                image.pixels = newPixels.flatten()
            else:
                image.pixels = newPixels
            image.update()

        else:
            assert(False)

    def setPackedImageFromChannels(self, newPixels, channel, flatten=True):
        if self.isOutput and self.isPacked:
            texture = self.getTexture()
            image = texture.image
            npImage = np.asarray(image.pixels, dtype = "float")
            npImage = npImage.reshape(image.size[0], image.size[0], image.channels)
            npImage[:,:,channel] = newPixels
            if flatten:
                image.pixels = npImage.flatten()
            else:
                image.pixels = npImage
            image.update()

        elif self.isInput and self.isPacked:
            self.data[self.identifier][:,:,channel] = newPixels
            

    def setPixels(self, newPixels):
        self.data[self.identifier] = newPixels

    def getPixels(self):
        return self.data[self.identifier]

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
        if self.isPacked and self.identifier in self.data:
            del self.data[self.identifier]
