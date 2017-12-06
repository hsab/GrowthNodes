from ..packages.cymem.cymem cimport Pool
from data cimport *

cdef class Array(Data):
    cdef Pool mem
    cdef public float[::1,:,:,:,:] array

cdef void clear(Array array)
cdef void copy_array(Array dest, Array src)
cdef void from_memoryview(Array array, float[:,:,:,:,:] memoryview)
cdef void from_blender_texture(Array array, object blender_texture)
cdef float sample_texture(Array array, float x, float y, float z)
