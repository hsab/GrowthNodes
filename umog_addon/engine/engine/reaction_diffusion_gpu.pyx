import numpy as np
cimport numpy as np

cimport array

import threading
import sys
import bpy

import traceback

from impls import reaction_diffusion2d
from impls import pyglet_lathe_impl
from impls import pyglet_cr_sphere_impl
from impls import pyglet_sg_impl
from impls import pyglet_tr_impl
from impls import pyglet_3dRD_impl
from ...packages import transformations
from ...packages import mcubes

import copy

def reaction_diffusion_gpu(Aout, Bout, A, B, dA, dB, dt, steps, feed, kill):
    print("rd python function")
    #array.copy_array(Aout, A)
    #array.copy_array(Bout, B)
    
    Atemp = np.asarray(A.array, order="F")
    Btemp = np.asarray(B.array, order="F")
    
    Atemp = np.moveaxis(Atemp, [0,1,2], [2, 0,1])
    Btemp = np.moveaxis(Btemp, [0,1,2], [2, 0,1])
    print(Atemp.shape)
    print(steps)
    
    args = {}
    args["A"] = Atemp 
    args["B"] = Btemp
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

def reaction_diffusion_3d_gpu(Aout, Bout, A, B, dA, dB, dt, steps, feed, kill):
    print("rd 3d python function")
    #array.copy_array(Aout, A)
    #array.copy_array(Bout, B)
    
    Atemp = np.asarray(A.array, order="F")
    Btemp = np.asarray(B.array, order="F")
    print("shapes " + str(Atemp.shape) + " " + str(Btemp.shape))
    args = {}
    args["A"] = Atemp 
    args["B"] = Btemp
    args["feed"] = feed
    args["kill"] = kill
    args["dA"] = dA
    args["dB"] = dB
    args["dt"] = dt
    try:
        #start a new thread to avoid poluting blender's opengl context
        t = threading.Thread(target=pyglet_3dRD_impl.OffScreenRender, 
                            args=(int(steps), args,))
        
        t.start()
        t.join()
        print("OpenglRender done")
        #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
        #print(temps["Aout"])
        
        array.from_memoryview(Aout, <np.ndarray[float, ndim=5, mode="c"]>args["Aout"])
        
        array.from_memoryview(Bout, <np.ndarray[float, ndim=5, mode="c"]>args["Bout"])
        print("shapes " + str(args["Aout"].shape) + " " + str(args["Bout"].shape))
    except:
        print("thread start failed")
        print("Unexpected error:", sys.exc_info()[0])
    pass

def lathe_gpu(Aout, A, resolution):
    
    Ac = np.asarray(A.array, order="F")
    Ac = np.moveaxis(Ac, [0,1,2], [2, 0,1])
    #print("lathe resolution is:" + str(resolution))
    temps = {}
    temps["A"] = Ac
    temps["outResolution"] = resolution
    
    try:
        #start a new thread to avoid poluting blender's opengl context
        t = threading.Thread(target=pyglet_lathe_impl.OffScreenRender, 
                            args=(temps,))
        
        t.start()
        t.join()
        print("OpenglRender done")
        #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
        #print(temps["Aout"])
        
        #tempA = np.moveaxis(temps["Aout"], [2, 0,1], [0,1,2])
        tempA = temps["Aout"]
        tempA = np.expand_dims(tempA, 3)
        tempA = np.expand_dims(tempA, 4)
        #print("tempA shape:" +     def get_buffer_values(self):
        array.from_memoryview(Aout, <np.ndarray[float, ndim=5, mode="c"]>tempA)

    except:
        print("thread start failed")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        
        
def pre_def_3dtexture(Aout, height, radius, shape, resolution):
    temps = {}
    if shape == 0:
        temps["shape"] = "sphere"
    elif shape == 1:
        temps["shape"] = "cylinder"
    temps["center"] = (0.5,0.5,0.5)

    temps["height"] = height
    temps["radius"] = radius
    temps["resolution"] = resolution
    print("h " + str(height) + " r " + str(radius) + " res " + str(resolution))
    try:
        #start a new thread to avoid poluting blender's opengl context
        t = threading.Thread(target=pyglet_cr_sphere_impl.OffScreenRender, 
                            args=(temps,))
        
        t.start()
        t.join()
        print("OpenglRender done")
        #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
        #print(temps["Aout"])
        
        tempA = temps["Aout"]
        tempA = np.expand_dims(tempA, 3)
        tempA = np.expand_dims(tempA, 4)
        array.from_memoryview(Aout, <np.ndarray[float, ndim=5, mode="c"]>tempA)

    except:
        print("thread start failed")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    #pydevd.settrace()
    
def solid_geometry(Aout, A, B, operation, threshold):
    A = np.asarray(A.array, order="F")
    B = np.asarray(B.array, order="F")
    temps = {}
    temps["A"] = A
    temps["B"] = B
    if operation == 0:
        temps["operation"] = "difference"
    elif operation == 1:
        temps["operation"] = "similar"
    elif operation == 2:
        temps["operation"] = "union"
    elif operation == 3:
        temps["operation"] = "intersect"
    else:
        print("invalid op used")
    temps["threshold"] = threshold
    #pydevd.settrace()
    try:
        #start a new thread to avoid poluting blender's opengl context
        t = threading.Thread(target=pyglet_sg_impl.OffScreenRender, 
                            args=(temps,))
        
        t.start()
        t.join()
        print("OpenglRender done")
        #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
        #print(temps["Aout"])
        
    
        tempA = temps["Aout"]
        print("shape of sg result " + str(tempA.shape))
        array.from_memoryview(Aout, <np.ndarray[float, ndim=5, mode="c"]>tempA)

    except:
        print("thread start failed")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)


def transformation(Aout, A, matrix):
    A = np.asarray(A.array, order="F")
    matrix = np.asarray(matrix.array, order="C")
    temps = {}
    temps["A"] = A
    #set transform with the correct mat4
    temps["transform"] = matrix
    print(temps["transform"])
    #pydevd.settrace()
    try:
        #start a new thread to avoid poluting blender's opengl context
        t = threading.Thread(target=pyglet_tr_impl.OffScreenRender, 
                            args=(temps,))
        
        t.start()
        t.join()
        print("OpenglRender done")
        #buf = np.frombuffer(refholder.execution_scratch[self.name]["buffer"], dtype=np.float)
        #print(temps["Aout"])
    
        array.from_memoryview(Aout, <np.ndarray[float, ndim=5, mode="c"]>temps["Aout"])

    except:
        print("thread start failed")
        print("Unexpected error:", sys.exc_info()[0])
        
def tex3d_to_mesh(A, mesh_name, iso_level):
    A = np.asarray(A.array, order="F")
    A = np.moveaxis(A, [0,1,2], [2, 0,1])
    verts, tris = mcubes.marching_cubes(A, iso_level)
    
    me = bpy.data.meshes.new(mesh_name)
    ob = bpy.data.objects.new(mesh_name, me)
    ob.location = (0,0,0)
    ob.show_name = True
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    
    resolution = A.shape[0]
    
    for vert_i in range(len(verts)):
        for pos_i in range(len(verts[vert_i])):
            verts[vert_i][pos_i] = verts[vert_i][pos_i]/resolution -0.5
    
    #type conversions
    verts = tuple(tuple(x) for x in verts)
    tris = tuple(tuple(x) for x in tris)

    #pydevd.settrace()
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, [], tris)

    # Update mesh with new data
    me.update(calc_edges=True)

### channels may be set to -1 to 4
#-1 set channel to 1
#0 set channel to 0
#1-channels in A set channel to in[channel -1]
def mux_channels(Aout, A, new_channels):
    Atemp = np.asarray(A.array, order="F", dtype=np.float32)
    #print(Atemp.shape)
    outA = np.zeros(Atemp.shape, dtype=np.float32, order="F")
    for cur in range(Atemp.shape[0]):
        if new_channels[cur] == -1:
            outA[cur] = np.ones(Atemp.shape[1:],dtype=np.float32, order="F")
        elif new_channels[cur] == 0:
            pass
        else:
            outA[cur] = Atemp[new_channels[cur]-1]
    #for i in range(Atemp.shape[0]):
        #for j in range(Atemp.shape[1]):
            #for k in range(Atemp.shape[2]):
                #if new_channels[i] == -1:
                    #outA[i,j,k,0,0] = 1
                #elif new_channels[i] == 0:
                    #pass
                #else:
                    #outA[i,j,k,0,0] = Atemp[(new_channels[i]-1),j,k,0,0]
    
    array.from_memoryview(Aout, <np.ndarray[float, ndim=5, mode="fortran"]>outA)
