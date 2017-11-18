from ..packages.cymem.cymem cimport Pool
from vector cimport *
from data cimport *

cdef class Mesh(Data):
    cdef Pool mem
    cdef int n_vertices, n_polygon_vertices, n_polygons
    cdef Vec3 *vertices
    cdef Vec3 *normals
    cdef int *polygon_vertices
    cdef int *polygons

cdef void allocate(Mesh mesh, int n_vertices, int n_polygon_vertices, int n_polygons)
cdef void from_blender_mesh(Mesh mesh, BlenderMesh *blender_mesh) nogil
cdef Mesh copy(Mesh mesh)
cdef void displace(Mesh mesh, float[:,:,:,:,:] texture)
cdef void iterated_displace(Mesh mesh, float[:,:,:,:,:] texture, int iterations)

cdef extern from "blender/makesdna/DNA_meshdata_types.h":
    cdef struct MVert:
        float co[3]
        float no[3]
    cdef struct MEdge:
        unsigned int v1, v2
    cdef struct MPoly:
        int loopstart
        int totloop
    cdef struct MLoop:
        unsigned int v
        unsigned int e
    cdef struct MLoopUV:
        float uv[2]
    cdef struct MLoopCol:
        unsigned char r, g, b, a

cdef extern from "blender/makesdna/DNA_mesh_types.h":
    cdef struct BlenderMesh "Mesh":
        int totvert, totedge, totpoly, totloop
        MVert *mvert
        MEdge *medge
        MPoly *mpoly
        MLoop *mloop
        MLoopUV *mloopuv
        MLoopCol *mloopcol
