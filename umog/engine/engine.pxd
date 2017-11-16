import cython
from cython.parallel import prange

cimport mesh

# instructions

cdef enum:
    MAX_INS = 2
    MAX_OUTS = 2

cpdef enum Opcode:
    CONST
    OUT
    NOP

    # math
    ADD
    SUBTRACT
    MULTIPLY
    DIVIDE
    NEGATE
    POWER
    MODULUS

    # array
    CONVOLVE

    # mesh
    DISPLACE

    # control
    LOOP

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

@cython.boundscheck(False)
cdef inline void sub(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] - b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void mul(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] * b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void div(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] / b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void neg(ArrayData out, ArrayData a) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = -a.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void pow(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] ** b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void mod(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] % b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void convolve(ArrayData out, ArrayData kernel, ArrayData a) nogil:
    cdef int cx = kernel.array.shape[1] // 2
    cdef int cy = kernel.array.shape[2] // 2
    cdef int cz = kernel.array.shape[3] // 2

    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    # for dx in prange()

                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t]
