import copy

#convolves the image and returns the result
#mask must be square
def convolve2d(array, mask):
    adim = array.shape
    
    result = copy.deepcopy(array)
    #ignore the edges of the image
    edge_offset = mask.shape[0] // 2
    
    
    for i in range(1, adim[0]-edge_offset):
        for j in range(1, adim[1]-edge_offset):
            for k in range(adim[2]):
                c_sum = 0.0
                for ii in range(mask.shape[0]):
                    for jj in range(mask.shape[1]):
                        c_sum += array[i + ii - edge_offset][j + jj - edge_offset][k]
                result[i][j][k] = c_sum
                
    return result
