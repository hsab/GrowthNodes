cdef struct Mesh:
    float[:,:] vertices
    float[:,:] normals
    int[:] polygon_vertices
    int[:,:] polygons
