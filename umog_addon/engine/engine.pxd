cimport mesh

# instructions

cdef enum:
    MAX_INS = 2
    MAX_OUTS = 2

cpdef enum Opcode:
    ADD
    SUBTRACT
    MULTIPLY
    DIVIDE
    DISPLACE
    LOOP
    NOP

cdef class Instruction:
    cdef Opcode op
    cdef int ins[MAX_INS]
    cdef int outs[MAX_OUTS]

# data

cdef enum DataTag:
    ARRAY
    FUNCTION
    MESH

cdef class Data:
    cdef DataTag tag

cdef class ArrayData(Data):
    cdef float[:,:,:,:,:] array

cdef class MeshData(Data):
    cdef mesh.Mesh mesh
