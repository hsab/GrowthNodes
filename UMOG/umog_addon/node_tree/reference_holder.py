import bpy
import numpy as np

class UMOGReferenceHolder:
    def __init__(self):
        self.references = {}
        # maps texture names to integers
        self.ntindex = 0
        self.tdict = {}
        self.np2dtextures = {}
        self.matrices = {}
        #maps the node name to a dict of node defined objects
        #store temporary objects here
        self.execution_scratch = {}
        
    def getRefForMatrix(self, matrix):
        matrix_name = np.array2string(matrix)
        if matrix_name in self.tdict:
            return self.tdict[matrix_name]
        oldidx = self.ntindex
        self.ntindex += 1
        # setup the empty texture array
        self.matrices[oldidx] = matrix
        self.tdict[matrix_name] = oldidx
        # now fill in the values
        return oldidx

    def getRefForTexture2d(self, name):
        if name in self.tdict:
            return self.tdict[name]
        oldidx = self.ntindex
        self.ntindex += 1
        # setup the empty texture array
        tr = bpy.context.scene.TextureResolution
        self.np2dtextures[oldidx] = np.zeros((tr, tr, 4))
        self.tdict[name] = oldidx
        # now fill in the values
        self.fillTexture(oldidx, name)
        return oldidx

    # returns the index of an initialized
    def createRefForTexture2d(self):
        oldidx = self.ntindex
        self.ntindex += 1
        # setup the empty texture array
        tr = bpy.context.scene.TextureResolution
        self.np2dtextures[oldidx] = np.zeros((tr, tr, 4))
        return oldidx

    def handleToImage(self, handle, image):
        # print("shape of texture " + str(self.np2dtextures[handle].shape))
        pixels = self.np2dtextures[handle].flatten().tolist()
        # print(str(pixels[0:64]))
        image.pixels = pixels

        # write image use to debug textures
        # image.filepath_raw = "/bulk/Pictures/Blender_Generated/temp.png"
        # image.file_format = 'PNG'
        # image.save()

    #writes the pixels of the image to the numpy array of the handle
    def imageToHandle(self, image, handle):
        self.np2dtextures[handle] = np.reshape(np.array(image.pixels[:]), 
            (bpy.context.scene.TextureResolution, bpy.context.scene.TextureResolution, 4))

    def fillTexture(self, index, name):
        tr = bpy.context.scene.TextureResolution
        trh = tr / 2
        # handle 1d textures by copying data to all channels
        if bpy.data.textures[name].type in ['CLOUDS', 'DISTORTED_NOISE', 'MARBLE', 'MUSGRAVE',
                                            'NOISE', 'STUCCI', 'VORONOI', 'WOOD']:
            for i in range(0, tr):
                for j in range(0, tr):
                    x, y = (i - trh) / trh, (j - trh) / trh
                    temp = bpy.data.textures[name].evaluate((x, y, 0.0))
                    self.np2dtextures[index][i, j] = [temp[3], temp[3], temp[3], 1.0]
        else:
            for i in range(0, tr):
                for j in range(0, tr):
                    x, y = (i - trh) / trh, (j - trh) / trh
                    self.np2dtextures[index][i, j] = bpy.data.textures[name].evaluate((x, y, 0.0))

    # used to generate intermediate or output references
    def getNewRef(self):
        oldidx = self.ntindex
        self.ntindex += 1
        return oldidx
