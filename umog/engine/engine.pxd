import cython
from cython.parallel import prange

cimport mesh

# instructions

cdef enum:
    MAX_INS = 2
    MAX_OUTS = 2
    MAX_PARAMETERS = 1

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

    EQ
    NEQ
    LT
    GT
    LEQ
    GEQ

    # boolean
    NOT
    AND
    OR
    XOR

    # array
    CONVOLVE

    # mesh
    DISPLACE
    ITERATED_DISPLACE

    # control
    LOOP

cdef class Instruction:
    cdef Opcode op
    cdef int ins[MAX_INS]
    cdef int outs[MAX_OUTS]
    cdef int parameters[MAX_PARAMETERS]

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
cdef inline void eq(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] == b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void neq(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] != b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void lt(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] < b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void gt(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] > b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void leq(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] <= b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void geq(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] >= b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_not(ArrayData out, ArrayData a) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = not a.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_and(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] and b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_or(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] or b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_xor(ArrayData out, ArrayData a, ArrayData b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = <bint>a.array[channel,x,y,z,t] ^ <bint>b.array[channel,x,y,z,t]

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
