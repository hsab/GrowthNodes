from ..packages.cymem.cymem cimport Pool
from libc.string cimport memset, memcpy
from data cimport *

cdef class Array(Data):
    def __init__(Array self, int channels, int x_size, int y_size, int z_size, int t_size):
        self.tag = ARRAY
        self.mem = Pool()

        self.array = <float[:channels, :x_size, :y_size, :z_size, :t_size]>self.mem.alloc(
            channels * x_size * y_size * z_size * t_size, sizeof(float))

cdef void clear(Array array):
    memset(&array.array[0,0,0,0,0], 0, array.array.shape[0] * array.array.shape[1] * array.array.shape[2] * array.array.shape[3] * array.array.shape[4] * sizeof(float))

cdef void copy(Array dest, Array src):
    memcpy(&dest.array[0,0,0,0,0], &src.array[0,0,0,0,0], dest.array.shape[0] * dest.array.shape[1] * dest.array.shape[2] * dest.array.shape[3] * dest.array.shape[4] * sizeof(float))

cdef void from_memoryview(Array array, float[:,:,:,:,:] memoryview):
    memcpy(&array.array[0,0,0,0,0], &memoryview[0,0,0,0,0], array.array.shape[0] * array.array.shape[1] * array.array.shape[2] * array.array.shape[3] * array.array.shape[4] * sizeof(float))
