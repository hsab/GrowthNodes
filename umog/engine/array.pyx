import numpy as np
cimport numpy as np
import cython
from cython.parallel import prange
from ..packages.cymem.cymem cimport Pool
from libc.string cimport memset, memcpy
from libc.math cimport fmod
from data cimport *

cdef class Array(Data):
    def __init__(Array self, int channels, int x_size, int y_size, int z_size, int t_size):
        self.tag = ARRAY
        self.mem = Pool()

        self.array = <float[:channels:1, :x_size, :y_size, :z_size, :t_size]>self.mem.alloc(
            channels * x_size * y_size * z_size * t_size, sizeof(float))

cdef void clear(Array array):
    memset(&array.array[0,0,0,0,0], 0, array.array.shape[0] * array.array.shape[1] * array.array.shape[2] * array.array.shape[3] * array.array.shape[4] * sizeof(float))

cdef void copy_array(Array dest, Array src):
    memcpy(&dest.array[0,0,0,0,0], &src.array[0,0,0,0,0], dest.array.shape[0] * dest.array.shape[1] * dest.array.shape[2] * dest.array.shape[3] * dest.array.shape[4] * sizeof(float))

cdef void from_memoryview(Array array, float[:,:,:,:,:] memoryview):
    memcpy(&array.array[0,0,0,0,0], &memoryview[0,0,0,0,0], array.array.shape[0] * array.array.shape[1] * array.array.shape[2] * array.array.shape[3] * array.array.shape[4] * sizeof(float))

@cython.boundscheck(False)
@cython.wraparound(False)
cdef void from_blender_texture(Array array, object blender_texture):
    cdef int x, y, z
    cdef object pixel

    for z in range(array.array.shape[3]):
        for y in range(array.array.shape[2]):
            for x in range(array.array.shape[1]):
                pixel = blender_texture.evaluate([2 * <float>x / <float>array.array.shape[1] - 1, 2 * <float>y / <float>array.array.shape[2] - 1, 2 * <float>z / <float>array.array.shape[3] - 1])

                array.array[0,x,y,z,0] = pixel[0]
                array.array[1,x,y,z,0] = pixel[1]
                array.array[2,x,y,z,0] = pixel[2]
                array.array[3,x,y,z,0] = pixel[3]

cdef float sample_texture(Array array, float x, float y, float z):
    x *= array.array.shape[1] / 10.0
    y *= array.array.shape[2] / 10.0
    z *= array.array.shape[3] / 10.0

    cdef int x1 = <int>x % array.array.shape[1]
    cdef int x2 = (x1 + 1) % array.array.shape[1]
    cdef int y1 = <int>y % array.array.shape[2]
    cdef int y2 = (y1 + 1) % array.array.shape[2]
    cdef int z1 = <int>z % array.array.shape[3]
    cdef int z2 = (z1 + 1) % array.array.shape[3]

    cdef float xt = x - <float>(<int>x)
    if xt < 0.0: xt += 1.0
    cdef float yt = y - <float>(<int>y)
    if yt < 0.0: yt += 1.0
    cdef float zt = z - <float>(<int>z)
    if zt < 0.0: zt += 1.0

    cdef float a = (1.0 - xt) * array.array[0,x1,y1,z1,0] + xt * array.array[0,x2,y1,z1,0]
    cdef float b = (1.0 - xt) * array.array[0,x1,y2,z1,0] + xt * array.array[0,x2,y2,z1,0]
    cdef float ab = (1.0 - yt) * a + yt * b
    cdef float c = (1.0 - xt) * array.array[0,x1,y1,z2,0] + xt * array.array[0,x2,y1,z2,0]
    cdef float d = (1.0 - xt) * array.array[0,x1,y2,z2,0] + xt * array.array[0,x2,y2,z2,0]
    cdef float cd = (1.0 - yt) * c + yt * d
    cdef float result = (1.0 - zt) * ab + zt * cd

    return result
