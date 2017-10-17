cdef struct Mesh:
    float[:,:] vertices
    float[:,:] normals
    int[:] polygon_vertices
    int[:,:] polygons

cpdef void copy(Mesh src, Mesh dst)
cpdef void displace(Mesh mesh, float[:,:,:,:,:] texture)
