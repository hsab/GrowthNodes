cdef struct Mesh:
    float[:,:] vertices
    float[:,:] normals
    int[:] polygon_vertices
    int[:,:] polygons

cpdef void displace(Mesh mesh, float[:,:,:,:,:] texture)
