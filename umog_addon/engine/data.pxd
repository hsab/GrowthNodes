from mesh cimport *

cdef enum DataTag:
    ARRAY
    FUNCTION
    MESH

cdef union DataContents:
    float[:,:,:,:,:] array
    Mesh mesh

cdef struct Data:
    DataTag tag
    DataContents contents
