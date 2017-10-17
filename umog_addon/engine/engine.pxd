import cython
from cython.parallel import prange

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
    CONST
    OUT
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

@cython.boundscheck(False)
cdef inline void add(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] + b.array[channel,x,y,z,t]
