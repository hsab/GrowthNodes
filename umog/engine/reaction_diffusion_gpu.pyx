cimport array


def reaction_diffusion_gpu(Aout, Bout, A, B, Da, Db, dt, steps, feed, kill):
    print("rd python function")
    array.array_copy(A, Aout)
    array.array_copy(B, Bout)
    pass
