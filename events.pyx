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
    for i in prange(1, xlim, nogil=True):
        for j in range(1, ylim):
            for k in range(zlim):
                for ii in range(mx):
                    for jj in range(my):
                        result[i][j][k] += array[i + ii - edge_offset][j + jj - edge_offset][k]
                
    return result
