from ..packages.cymem.cymem cimport Pool
from vector cimport *
from data cimport *
from array cimport Array

cdef class MeshSequence(Data):
    cdef public list frames

cdef class Mesh(Data):
    cdef Pool mem
    cdef int n_vertices, n_triangles
    cdef Vec3 *vertices
    cdef Vec3 *normals
    cdef int *triangles
    cdef Vec2 *uvs

cdef void allocate(Mesh mesh, int n_vertices, int n_triangles)
cdef void from_blender_mesh(Mesh mesh, BlenderMesh *blender_mesh)
cdef Mesh copy_mesh(Mesh mesh)
cdef void displace(Mesh mesh, Array texture)
cdef void iterated_displace(MeshSequence mesh, Array texture)

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
    cdef struct MFace:
        unsigned int v1, v2, v3, v4
    cdef struct MTFace:
        float uv[4][2]

cdef extern from "blender/makesdna/DNA_mesh_types.h":
    cdef struct BlenderMesh "Mesh":
        int totvert, totedge, totpoly, totloop, totface
        MVert *mvert
        MEdge *medge
        MPoly *mpoly
        MLoop *mloop
        MLoopUV *mloopuv
        MLoopCol *mloopcol
        MFace *mface
        MTFace *mtface
