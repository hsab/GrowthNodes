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
    MULTIPLY_MATRIX_MATRIX
    MULTIPLY_MATRIX_VECTOR
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
@cython.wraparound(False)
cdef inline void add(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] + \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void sub(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] - \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void mul(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] * \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void div(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] / \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void neg(Array out, Array a) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = -a.array[channel,x,y,z,t]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void pow(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] ** \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void mod(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] % \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void eq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] == \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void neq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] != \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void lt(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] < \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void gt(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] > \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void leq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] <= \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void geq(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] >= \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void boolean_not(Array out, Array a) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = not a.array[channel,x,y,z,t]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void boolean_and(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] and \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void boolean_or(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = \
                            a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] or \
                            b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void boolean_xor(Array out, Array a, Array b) nogil:
    cdef int channel, x, y, z, t
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] =  \
                            <bint>a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] ^\
                            <bint>b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void multiply_matrix_matrix(Array out, Array a, Array b) nogil:
    cdef int x, y, t, i
    for t in prange(out.array.shape[4]):
        for y in prange(out.array.shape[2]):
            for x in prange(out.array.shape[1]):
                out.array[0,x,y,0,t] = 0.0
                for i in prange(a.array.shape[1]):
                    out.array[0,x,y,0,t] += a.array[0,i,y,0,t % a.array.shape[4]] * b.array[0,x,i,0,t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void multiply_matrix_vector(Array out, Array matrix, Array vector) nogil:
    cdef int channel, x, y, z, t, i
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = 0
                        for i in prange(vector.array.shape[0]):
                            out.array[channel,x,y,z,t] += matrix.array[0, i, channel, 0, t % matrix.array.shape[4]] * vector.array[i, x, y, z, t % vector.array.shape[4]]

# @cython.boundscheck(False)
# @cython.wraparound(False)
# cdef inline void convolve(Array out, Array kernel, Array a) nogil:
#     cdef int cx = kernel.array.shape[1] // 2
#     cdef int cy = kernel.array.shape[2] // 2
#     cdef int cz = kernel.array.shape[3] // 2

#     cdef int channel, x, y, z, t
#     for t in prange(out.array.shape[4]):
#         for z in prange(out.array.shape[3]):
#             for y in prange(out.array.shape[2]):
#                 for x in prange(out.array.shape[1]):
#                     # for dx in prange()

#                     for channel in prange(out.array.shape[0]):
#                         out.array[channel,x,y,z,t] = matrix.array[channel,x,y,z,t]
