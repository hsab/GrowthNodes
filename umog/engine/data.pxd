cdef enum DataTag:
    ARRAY
    MESH

cdef class Data:
    cdef DataTag tag
