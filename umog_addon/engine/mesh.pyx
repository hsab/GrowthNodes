import numpy as np
cimport numpy as np

import cython

from libc.math cimport fmod

@cython.boundscheck(False)
def from_blender_mesh(object blender_mesh):
    cdef Mesh mesh

    mesh.vertices = np.ndarray(shape=(len(blender_mesh.vertices),3), dtype=np.float32)
    mesh.normals = np.ndarray(shape=(len(blender_mesh.vertices),3), dtype=np.float32)
    mesh.polygon_vertices = np.ndarray(shape=(len(blender_mesh.loops)), dtype=np.int32)
    mesh.polygons = np.ndarray(shape=(len(blender_mesh.polygons),2), dtype=np.int32)

    cdef int i
    for i in range(len(blender_mesh.vertices)):
        vector = blender_mesh.vertices[i].co
        mesh.vertices[i,0] = vector.x
        mesh.vertices[i,1] = vector.y
        mesh.vertices[i,2] = vector.z

        normal = blender_mesh.vertices[i].normal
        mesh.normals[i,0] = normal.x
        mesh.normals[i,1] = normal.y
        mesh.normals[i,2] = normal.z

    for i in range(len(blender_mesh.loops)):
        mesh.polygon_vertices[i] = blender_mesh.loops[i].vertex_index

    for i in range(len(blender_mesh.polygons)):
        mesh.polygons[i,0] = blender_mesh.polygons[i].loop_start
        mesh.polygons[i,1] = blender_mesh.polygons[i].loop_total

    return mesh

def to_pydata(Mesh mesh):
    cdef list vertices = []
    cdef list faces = []

    cdef int i, j

    for i in range(mesh.vertices.shape[0]):
        vertices.append((mesh.vertices[i,0], mesh.vertices[i,1], mesh.vertices[i,2]))

    cdef list polygon
    for i in range(mesh.polygons.shape[0]):
        polygon = []
        for j in range(mesh.polygons[i,0], mesh.polygons[i,0] + mesh.polygons[i,1]):
            polygon.append(mesh.polygon_vertices[j])
        faces.append(tuple(polygon))

    return vertices, [], faces

def displace(Mesh mesh, float[:,:,:] texture):
    cdef int i
    cdef float[:] value
    cdef float c
    for i in range(mesh.vertices.shape[0]):
        value = sample_texture(texture, 1000.0 * mesh.vertices[i,0], 1000.0 * mesh.vertices[i,1])
        c = 0.1 * ((value[0] + value[1] + value[2] + value[3]) / 4.0 - 0.5)
        mesh.vertices[i,0] += c * mesh.normals[i,0]
        mesh.vertices[i,1] += c * mesh.normals[i,1]
        mesh.vertices[i,2] += c * mesh.normals[i,2]

def array_from_texture(object blender_texture, int width, int height):
    texture = np.ndarray(shape=(width,height,4), dtype=np.float32)

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

cdef float[:] sample_texture(float[:,:,:] data, float x, float y):
    cdef int x1 = <int>x % data.shape[0]
    cdef int x2 = (x1 + 1) % data.shape[0]
    cdef int y1 = <int>y % data.shape[1]
    cdef int y2 = (y1 + 1) % data.shape[1]

    cdef float xt = fmod(x, 1.0)
    if xt < 0.0: xt += 1.0
    cdef float yt = fmod(y, 1.0)
    if yt < 0.0: yt += 1.0

    cdef float[:] result = np.ndarray(shape=(data.shape[2]), dtype=np.float32)

    cdef int channel
    for channel in range(data.shape[2]):
        f1 = (1.0 - xt) * data[x1,y1,channel] + xt * data[x2,y1,channel]
        f2 = (1.0 - xt) * data[x1,y2,channel] + xt * data[x2,y2,channel]
        result[channel] = (1.0 - yt) * f1 + yt * f2

    return result
