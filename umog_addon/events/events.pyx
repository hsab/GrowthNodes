import copy
import numpy as np
from cython.parallel import prange
import cython
cimport cython

#convolves the image and loads the result in output
#mask must be square
@cython.boundscheck(False)
def convolve2d(double[:,:,:] array, double[:,:] mask, double [:,:,:] output):
    adim = array.shape
    #print(str(array.shape))
    #ignore the edges of the image
    cdef int edge_offset = mask.shape[0] // 2
    
    cdef int xlim = adim[0]
    cdef int ylim = adim[1]
    cdef int zlim = adim[2] -1
    
    cdef int mx = mask.shape[0]
    cdef int my = mask.shape[1]
    
    cdef int i,j,k,ii,jj
    for i in prange(xlim, nogil=True):
        for j in range(ylim):
            for k in range(zlim):
                for ii in range(mx):
                    for jj in range(my):
                        output[i][j][k] += array[(i + ii - edge_offset) % xlim][(j + jj - edge_offset)% ylim][k]*mask[ii][jj]
            output[i][j][zlim] = 1.0
                

@cython.boundscheck(False)
def ReactionDiffusion2d(double [:,:,:] A,double [:,:,:] Ap,double [:,:,:] LA,
    double [:,:,:] B,double [:,:,:] Bp,double [:,:,:] LB, double [:,:] mask,
    double Da, double Db, double feed, double kill, double dt):
    
    adim = Ap.shape
    
    cdef int xlim = adim[0]
    cdef int ylim = adim[1]
    cdef int zlim = adim[2]-1
    
    cdef int i,j,k
    for i in prange(xlim, nogil=True):
        for j in range(ylim):
            for k in range(zlim):
                Ap[i][j][k] = max(A[i][j][k] + (Da*LA[i][j][k] - (A[i][j][k]*B[i][j][k]*B[i][j][k]) + feed*(1.0 - A[i][j][k]))* dt,0)
                Bp[i][j][k] = max(B[i][j][k] + (Db * LB[i][j][k] + (A[i][j][k]*B[i][j][k]*B[i][j][k]) -(kill + feed)* B[i][j][k])*dt,0)
            #no mess with alpha
            Ap[i][j][zlim] = 0.0
            Bp[i][j][zlim] = 0.0
