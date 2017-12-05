cdef enum DataTag:
    ARRAY
    MESH
    MESH_SEQUENCE

cdef class Data:
    cdef DataTag tag
