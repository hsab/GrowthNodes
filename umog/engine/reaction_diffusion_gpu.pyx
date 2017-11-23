import numpy as np
cimport numpy as np

cimport array

import threading
import sys

import reaction_diffusion2d

def reaction_diffusion_gpu(Aout, Bout, A, B, dA, dB, dt, steps, feed, kill):
    print("rd python function")
    #array.copy_array(Aout, A)
    #array.copy_array(Bout, B)
    
    A = np.asarray(A.array, order="F")
    B = np.asarray(B.array, order="F")
    
    A = np.moveaxis(A, [0,1,2], [2, 0,1])
    B = np.moveaxis(B, [0,1,2], [2, 0,1])
    print(A.shape)
    print(steps)
    
    args = {}
    args["A"] = A 
    args["B"] = B
    args["feed"] = feed
    args["kill"] = kill
    args["dA"] = dA
    args["dB"] = dB
    args["dt"] = dt
    try:
        #start a new thread to avoid poluting blender's opengl context
        t = threading.Thread(target=reaction_diffusion2d.OffScreenRender, 
                            args=(int(steps), args,))
        
        t.start()
        t.join()
        print("OpenglRender done")
        #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
        #print(temps["Aout"])
        
        tempA = np.moveaxis(args["Aout"], [2, 0,1], [0,1,2])
        
        array.from_memoryview(Aout, <np.ndarray[float, ndim=5, mode="c"]>tempA)
        
        tempB = np.moveaxis(args["Aout"], [2, 0,1], [0,1,2])
        
        array.from_memoryview(Bout, <np.ndarray[float, ndim=5, mode="c"]>tempB)
        
    except:
        print("thread start failed")
        print("Unexpected error:", sys.exc_info()[0])
    pass
