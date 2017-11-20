import numpy as np
cimport numpy as np
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

def array_from_texture(object blender_texture, int width, int height):
    texture = np.ndarray(shape=(4,width,height,1,1), dtype=np.float32, order="F")

    cdef int x, y, i
    cdef object pixel
    for x in range(width):
        for y in range(height):
            pixel = blender_texture.evaluate([<float>x / <float>width, <float>y / <float>height, 0.0])
            texture.data[0,x,y,0,0] = pixel[0]
            texture.data[1,x,y,0,0] = pixel[1]
            texture.data[2,x,y,0,0] = pixel[2]
            texture.data[3,x,y,0,0] = pixel[3]

    return texture

cdef float sample_texture(Array array, float x, float y):
    cdef int x1 = <int>x % array.array.shape[0]
    cdef int x2 = (x1 + 1) % array.array.shape[0]
    cdef int y1 = <int>y % array.array.shape[1]
    cdef int y2 = (y1 + 1) % array.array.shape[1]

    cdef float xt = fmod(x, 1.0)
    if xt < 0.0: xt += 1.0
    cdef float yt = fmod(y, 1.0)
    if yt < 0.0: yt += 1.0

    cdef float result

    f1 = (1.0 - xt) * array.array[0,x1,y1,0,0] + xt * array.array[0,x2,y1,0,0]
    f2 = (1.0 - xt) * array.array[0,x1,y2,0,0] + xt * array.array[0,x2,y2,0,0]
    result = (1.0 - yt) * f1 + yt * f2

    return result
