import cython
from cython.parallel import prange

from data cimport *
from array cimport *

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
    COND

cdef class Instruction:
    cdef Opcode op
    cdef int ins[MAX_INS]
    cdef int outs[MAX_OUTS]
    cdef int parameters[MAX_PARAMETERS]

@cython.boundscheck(False)
cdef inline void add(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] + b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void sub(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] - b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void mul(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] * b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void div(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] / b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void neg(Array out, Array a) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = -a.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void pow(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] ** b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void mod(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] % b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void eq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] == b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void neq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] != b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void lt(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] < b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void gt(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] > b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void leq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] <= b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void geq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] >= b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_not(Array out, Array a) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = not a.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_and(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] and b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_or(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = a.array[channel,x,y,z,t] or b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void boolean_xor(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = <bint>a.array[channel,x,y,z,t] ^ <bint>b.array[channel,x,y,z,t]

@cython.boundscheck(False)
cdef inline void convolve(Array out, Array kernel, Array a) nogil:
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
