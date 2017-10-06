import numpy as np
cimport numpy as np

import bpy
from bpy import types

import cython
cimport cython
from cpython.ref cimport PyObject

from libc.math cimport fmod

cdef class Mesh:
    cdef float[:,:] vertices
    cdef float[:,:] normals
    cdef int[:] polygon_vertices
    cdef int[:,:] polygons

    @cython.boundscheck(False)
    def __init__(self, object mesh):
        print(repr(mesh))
        cdef PyObject *ptr = <PyObject *>mesh

        self.vertices = np.ndarray(shape=(len(mesh.vertices),3), dtype=np.float32)
        self.normals = np.ndarray(shape=(len(mesh.vertices),3), dtype=np.float32)
        self.polygon_vertices = np.ndarray(shape=(len(mesh.loops)), dtype=np.int32)
        self.polygons = np.ndarray(shape=(len(mesh.polygons),2), dtype=np.int32)

        cdef int i
        for i in range(len(mesh.vertices)):
            vector = mesh.vertices[i].co
            self.vertices[i,0] = vector.x
            self.vertices[i,1] = vector.y
            self.vertices[i,2] = vector.z

            normal = mesh.vertices[i].normal
            self.normals[i,0] = normal.x
            self.normals[i,1] = normal.y
            self.normals[i,2] = normal.z

        for i in range(len(mesh.loops)):
            self.polygon_vertices[i] = mesh.loops[i].vertex_index

        for i in range(len(mesh.polygons)):
            self.polygons[i,0] = mesh.polygons[i].loop_start
            self.polygons[i,1] = mesh.polygons[i].loop_total

    def to_pydata(self):
        cdef list vertices = []
        cdef list faces = []

        cdef int i, j

        for i in range(self.vertices.shape[0]):
            vertices.append((self.vertices[i,0], self.vertices[i,1], self.vertices[i,2]))

        cdef list polygon
        for i in range(self.polygons.shape[0]):
            polygon = []
            for j in range(self.polygons[i,0], self.polygons[i,0] + self.polygons[i,1]):
                polygon.append(self.polygon_vertices[j])
            faces.append(tuple(polygon))

        return vertices, [], faces

    cdef displace(self, Texture2D texture):
        cdef int i
        cdef float[:] value
        cdef float c
        for i in range(self.vertices.shape[0]):
            value = texture.sample(1000.0 * self.vertices[i,0], 1000.0 * self.vertices[i,1])
            c = 0.1 * ((value[0] + value[1] + value[2] + value[3]) / 4.0 - 0.5)
            self.vertices[i,0] += c * self.normals[i,0]
            self.vertices[i,1] += c * self.normals[i,1]
            self.vertices[i,2] += c * self.normals[i,2]

cdef class Texture2D:
    cdef float[:,:,:] data

    def __init__(self, int width, int height, channels):
        self.data = np.ndarray(shape=(width,height,channels), dtype=np.float32)

    @staticmethod
    def from_texture(object blender_texture, int width, int height):
        texture = Texture2D(width, height, 4)

        cdef int x, y, i
        cdef object pixel
        for x in range(width):
            for y in range(height):
                pixel = blender_texture.evaluate([x, y, 0.0])
                texture.data[x,y,0] = pixel[0]
                texture.data[x,y,1] = pixel[1]
                texture.data[x,y,2] = pixel[2]
                texture.data[x,y,3] = pixel[3]

        return texture

    cdef float[:] sample(self, float x, float y):
        cdef int x1 = <int>x % self.data.shape[0]
        cdef int x2 = (x1 + 1) % self.data.shape[0]
        cdef int y1 = <int>y % self.data.shape[1]
        cdef int y2 = (y1 + 1) % self.data.shape[1]

        cdef float xt = fmod(x, 1.0)
        if xt < 0.0: xt += 1.0
        cdef float yt = fmod(y, 1.0)
        if yt < 0.0: yt += 1.0

        cdef float[:] result = np.ndarray(shape=(self.data.shape[2]), dtype=np.float32)

        cdef int channel
        for channel in range(self.data.shape[2]):
            f1 = (1.0 - xt) * self.data[x1,y1,channel] + xt * self.data[x2,y1,channel]
            f2 = (1.0 - xt) * self.data[x1,y2,channel] + xt * self.data[x2,y2,channel]
            result[channel] = (1.0 - yt) * f1 + yt * f2

        return result

# cdef enum Type:
#     scalar, vector, array, function, mesh, list

# cdef enum Instruction:


# cdef struct Function:
#     cdef int dimensions
#     cdef bool time

def compile(object node_tree):
    pass

cpdef displace(Mesh mesh, Texture2D texture):
    mesh.displace(texture)