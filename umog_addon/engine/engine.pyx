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

def compile(node_tree):
    pass