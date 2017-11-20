from ..packages.cymem.cymem cimport Pool
from data cimport *

cdef class Array(Data):
    cdef Pool mem
    cdef public float[::1,:,:,:,:] array

cdef void clear(Array array)
cdef void copy(Array dest, Array src)
cdef void from_memoryview(Array array, float[:,:,:,:,:] memoryview)
