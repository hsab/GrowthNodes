import cython
from cython.parallel import prange
from libc.math cimport fmin, fmax
from libc.stdio cimport printf

from data cimport *
from array cimport *

import numpy as np
cimport numpy as np
from numpy import linalg as la

# instructions

cdef enum:
    MAX_INS = 4
    MAX_OUTS = 4
    MAX_PARAMETERS = 10

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
    MATRIX_TRANSPOSE
    MATRIX_NORM_FRO
    MATRIX_NORM_1
    MATRIX_NORM_2
    MATRIX_NORM_INF
    MATRIX_INVERSE
    MATRIX_DETERMINANT
    MULTIPLY_MATRIX_MATRIX
    MULTIPLY_MATRIX_VECTOR
    CONVOLVE

    REACTION_DIFFUSION_STEP
    MUX_CHANNELS
    

    # mesh
    DISPLACE
    DISPLACE_SEQUENCE
    ITERATED_DISPLACE

    # control
    LOOP
    COND
    
    # gpu
    REACTION_DIFFUSION_GPU_STEP
    REACTION_DIFFUSION_VOXEL_GPU
    
    SHAPE_GPU
    LATHE_GPU
    SOLID_GEOMETRY_GPU
    TRANSFORM_GPU
    
    

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
                            <bint>a.array[channel % a.array.shape[0], x % a.array.shape[1], y % a.array.shape[2], z % a.array.shape[3], t % a.array.shape[4]] ^ \
                            <bint>b.array[channel % b.array.shape[0], x % b.array.shape[1], y % b.array.shape[2], z % b.array.shape[3], t % b.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_transpose(Array out, Array a) nogil:
    cdef int x, y, t, i
    for t in prange(out.array.shape[4]):
        for y in prange(out.array.shape[2]):
            for x in prange(out.array.shape[1]):
                out.array[0,x,y,0,t] = a.array[0,y,x,0,t]
 
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_determinant(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = <np.ndarray[float, ndim=2, mode="fortran"]>a.array[0, : , :, 0, t]
        out.array[0, 0, 0, 0, t] = la.det(input)
        
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_inverse(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = <np.ndarray[float, ndim=2, mode="fortran"]>a.array[0, : , :, 0, t]
        if la.det(input) != 0:
            out.array[0, :, :, 0, t] = la.inv(input)
        else:
            out.array = a.array
        
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_fro(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = <np.ndarray[float, ndim=2, mode="fortran"]>a.array[0, : , :, 0, t]
        out.array[0, 0, 0, 0, t] = la.norm(input, 'fro')
        
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_1(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = <np.ndarray[float, ndim=2, mode="fortran"]>a.array[0, : , :, 0, t]
        out.array[0, 0, 0, 0, t] = la.norm(input,1)
        
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_2(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = <np.ndarray[float, ndim=2, mode="fortran"]>a.array[0, : , :, 0, t]
        out.array[0, 0, 0, 0, t] = la.norm(input, 2)


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_inf(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = <np.ndarray[float, ndim=2, mode="fortran"]>a.array[0, : , :, 0, t]
        out.array[0, 0, 0, 0, t] = la.norm(input, np.inf)
                
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

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void convolve(Array out, Array kernel, Array array) nogil:
    cdef int cx = (kernel.array.shape[1] - 1) // 2
    cdef int cy = (kernel.array.shape[2] - 1) // 2
    cdef int cz = (kernel.array.shape[3] - 1) // 2

    cdef int channel, x, y, z, t, x_, y_, z_
    for t in prange(out.array.shape[4]):
        for z in prange(out.array.shape[3]):
            for y in prange(out.array.shape[2]):
                for x in prange(out.array.shape[1]):
                    for channel in prange(out.array.shape[0]):
                        out.array[channel,x,y,z,t] = 0
                    for z_ in prange(max(0, z - cz), min(array.array.shape[3], z - cz + kernel.array.shape[3])):
                        for y_ in prange(max(0, y - cy), min(array.array.shape[2], y - cy + kernel.array.shape[2])):
                            for x_ in prange(max(0, x - cx), min(array.array.shape[1], x - cx + kernel.array.shape[1])):
                                for channel in prange(out.array.shape[0]):
                                    out.array[channel,x,y,z,t] += \
                                        kernel.array[channel % kernel.array.shape[0], cx + x_ - x, cy + y_ - y, cz + z_ - z, t % kernel.array.shape[4]] * \
                                        array.array[channel % array.array.shape[0], x_, y_, z_, t % array.array.shape[4]]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void reaction_diffusion_step(Array out, Array a, float feed, float kill, float Da, float Db, float dt):
    cdef int x, y

    cdef Array kernel = Array(1, 3, 3, 1, 1)
    kernel.array[0,0,0,0,0] = 0.25; kernel.array[0,1,0,0,0] = 0.5; kernel.array[0,2,0,0,0] = 0.25
    kernel.array[0,0,1,0,0] = 0.5; kernel.array[0,1,1,0,0] = -3; kernel.array[0,2,1,0,0] = 0.5
    kernel.array[0,0,2,0,0] = 0.25; kernel.array[0,1,2,0,0] = 0.5; kernel.array[0,2,2,0,0] = 0.25

    cdef Array laplacian = Array(a.array.shape[0], a.array.shape[1], a.array.shape[2], a.array.shape[3], a.array.shape[4])
    convolve(laplacian, kernel, a)

    with nogil:
        for y in prange(out.array.shape[2]):
            for x in range(out.array.shape[1]):
                out.array[0,x,y,0,0] = fmin(fmax(a.array[0,x,y,0,0] + (Da * laplacian.array[0,x,y,0,0] - (a.array[0,x,y,0,0]*a.array[1,x,y,0,0]*a.array[1,x,y,0,0]) + feed*(1.0 - a.array[0,x,y,0,0]))*dt, 0.0), 1.0)
                out.array[1,x,y,0,0] = fmin(fmax(a.array[1,x,y,0,0] + (Db * laplacian.array[1,x,y,0,0] + (a.array[0,x,y,0,0]*a.array[1,x,y,0,0]*a.array[1,x,y,0,0]) - (kill + feed)*a.array[1,x,y,0,0])*dt, 0.0), 1.0)
                out.array[2,x,y,0,0] = 0
                out.array[3,x,y,0,0] = 1

cdef inline int max(int a, int b) nogil:
    if a > b:
        return a
    else:
        return b

cdef inline int min(int a, int b) nogil:
    if a < b:
        return a
    else:
        return b
