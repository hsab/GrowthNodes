import copy
import numpy as np
from cython.parallel import prange

#convolves the image and returns the result
#mask must be square
def convolve2d(double[:,:,:] array, double[:,:] mask):
    adim = array.shape
    #print(str(array.shape))
    cdef double[:,:,:] result = np.zeros(shape=[adim[0], adim[1], adim[2]])
    #ignore the edges of the image
    cdef int edge_offset = mask.shape[0] // 2
    
    cdef int xlim = adim[0]-edge_offset
    cdef int ylim = adim[1]-edge_offset
    cdef int zlim = adim[2]
    
    cdef int mx = mask.shape[0]
    cdef int my = mask.shape[1]
    
    cdef int i,j,k,ii,jj
    for i in prange(edge_offset, xlim, nogil=True):
        for j in range(edge_offset, ylim):
            for k in range(zlim):
                for ii in range(mx):
                    for jj in range(my):
                        result[i][j][k] += array[i + ii - edge_offset][j + jj - edge_offset][k]
                
    return result


def ReactionDiffusion2d(double [:,:,:] A,double [:,:,:] Ap,double [:,:,:] LA,
    double [:,:,:] B,double [:,:,:] Bp,double [:,:,:] LB, double [:,:] mask,
    double Da, double Db, double feed, double kill, double dt):
    
    adim = Ap.shape
    
    cdef int xlim = adim[0]
    cdef int ylim = adim[1]
    cdef int zlim = adim[2]
    
    cdef int i,j,k
    for i in prange(xlim, nogil=True):
        for j in range(ylim):
            for k in range(zlim):
                Ap[i][j][k] = A[i][j][k] + (Da*LA[i][j][k] - (A[i][j][k]*B[i][j][k]*B[i][j][k]) + feed*(1.0 - A[i][j][k]))* dt
                Bp[i][j][k] = B[i][j][k] + (Db * LB[i][j][k] + (A[i][j][k]*B[i][j][k]*B[i][j][k]) -(kill + feed)* B[i][j][k])*dt
