import numpy as np
cimport numpy as np

import bpy
from bpy import types

cdef class Mesh:
    cdef float[:,:] vertices
    cdef float[:,:] normals
    cdef int[:] polygon_vertices
    cdef int[:,:] polygons

    def __init__(self, object mesh):
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

cdef class Texture2D:
    cdef float[:,:,:] data

    def __init__(self, int width, int height, channels):
        self.data = np.ndarray(shape=(width,height,channels), dtype=np.float32)

    @staticmethod
    def from_texture(object texture, int width, int height):
        texture = Texture2D(width, height, 4)

        cdef int x, y, i
        cdef list pixel
        for x in range(width):
            for y in range(height):
                pixel = object.evaluate(x, y)
                texture.data[x,y,0] = pixel[0]
                texture.data[x,y,1] = pixel[1]
                texture.data[x,y,2] = pixel[2]
                texture.data[x,y,3] = pixel[3]

        return texture

def compile(node_tree):
    pass