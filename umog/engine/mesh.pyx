import cython

from libc.stdint cimport uintptr_t
from libc.string cimport memset, memcpy

from ..packages.cymem.cymem cimport Pool

from data cimport *
from array cimport *

cdef class Mesh(Data):
    def __init__(Mesh self):
        self.tag = MESH
        self.mem = Pool()

cdef void allocate(Mesh mesh, int n_vertices, int n_polygon_vertices, int n_polygons):
    mesh.n_vertices = n_vertices
    mesh.n_polygon_vertices = n_polygon_vertices
    mesh.n_polygons = n_polygons

    mesh.vertices = <Vec3 *>mesh.mem.alloc(n_vertices, sizeof(Vec3))
    mesh.normals = <Vec3 *>mesh.mem.alloc(n_vertices, sizeof(Vec3))
    mesh.polygon_vertices = <int *>mesh.mem.alloc(n_polygon_vertices, sizeof(int))
    mesh.polygons = <int *>mesh.mem.alloc(n_polygons * 2, sizeof(int))

@cython.boundscheck(False)
cdef void from_blender_mesh(Mesh mesh, BlenderMesh *blender_mesh) nogil:
    cdef int i
    for i in range(blender_mesh.totvert):
        mesh.vertices[i].x = blender_mesh.mvert[i].co[0]
        mesh.vertices[i].y = blender_mesh.mvert[i].co[1]
        mesh.vertices[i].z = blender_mesh.mvert[i].co[2]

        mesh.normals[i].x = blender_mesh.mvert[i].no[0]
        mesh.normals[i].y = blender_mesh.mvert[i].no[1]
        mesh.normals[i].z = blender_mesh.mvert[i].no[2]
        vec3_normalize(&mesh.normals[i], &mesh.normals[i])

    for i in range(blender_mesh.totloop):
        mesh.polygon_vertices[i] = blender_mesh.mloop[i].v

    for i in range(blender_mesh.totpoly):
        mesh.polygons[2*i] = blender_mesh.mpoly[i].loopstart
        mesh.polygons[2*i + 1] = blender_mesh.mpoly[i].totloop

@cython.boundscheck(False)
cpdef void to_blender_mesh(Mesh mesh, uintptr_t blender_mesh_ptr) nogil:
    cdef BlenderMesh *blender_mesh = <BlenderMesh *>blender_mesh_ptr
    cdef int i
    for i in range(mesh.n_vertices):
        blender_mesh.mvert[i].co[0] = mesh.vertices[i].x
        blender_mesh.mvert[i].co[1] = mesh.vertices[i].y
        blender_mesh.mvert[i].co[2] = mesh.vertices[i].z

        blender_mesh.mvert[i].no[0] = mesh.normals[i].x
        blender_mesh.mvert[i].no[1] = mesh.normals[i].y
        blender_mesh.mvert[i].no[2] = mesh.normals[i].z

cdef Mesh copy_mesh(Mesh old):
    cdef Mesh new = Mesh()
    allocate(new, old.n_vertices, old.n_polygon_vertices, old.n_polygons)
    memcpy(new.vertices, old.vertices, old.n_vertices * sizeof(Vec3))
    memcpy(new.normals, old.normals, old.n_vertices * sizeof(Vec3))
    memcpy(new.polygon_vertices, old.polygon_vertices, old.n_polygon_vertices * sizeof(int))
    memcpy(new.polygons, old.polygons, old.n_polygons * 2 * sizeof(int))
    return new

cdef void displace(Mesh mesh, Array texture):
    cdef int i
    cdef float value
    cdef float c
    cdef Vec3 normal
    for i in range(mesh.n_vertices):
        # value = sample_texture(texture, 100.0 * mesh.vertices[i].x, 100.0 * mesh.vertices[i].y)
        # value = texture[0,<int>(100 * mesh.vertices[i].x + 50) % 100,<int>(100 * mesh.vertices[i].y + 50) % 100,0,0]
        value = sample_texture(texture,100 * mesh.vertices[i].x + 50,100 * mesh.vertices[i].y)
        c = value
        vec3_scale(&normal, c, &mesh.normals[i])
        vec3_add(&mesh.vertices[i], &mesh.vertices[i], &normal)

    recalculate_normals(mesh)

cdef void iterated_displace(Mesh mesh, Array texture, int iterations):
    cdef int i
    for i in range(iterations):
        displace(mesh, texture)

@cython.cdivision(True)
cdef void recalculate_normals(Mesh mesh):
    cdef Pool mem = Pool()
    cdef int i, j
    cdef int polygon_start, polygon_length
    cdef Vec3 *a
    cdef Vec3 *b
    cdef Vec3 *c
    cdef Vec3 ab, ac
    cdef Vec3 polygon_normal

    memset(mesh.normals, 0, mesh.n_vertices * sizeof(Vec3))

    for i in range(mesh.n_polygons):
        polygon_start = mesh.polygons[2*i]
        polygon_length = mesh.polygons[2*i + 1]
        a = &mesh.vertices[mesh.polygon_vertices[polygon_start]]
        b = &mesh.vertices[mesh.polygon_vertices[polygon_start + 1]]
        c = &mesh.vertices[mesh.polygon_vertices[polygon_start + 2]]
        vec3_sub(&ab, b, a)
        vec3_sub(&ac, c, a)
        vec3_cross(&polygon_normal, &ab, &ac)
        for j in range(polygon_start, polygon_start + polygon_length):
            vec3_add(&mesh.normals[mesh.polygon_vertices[j]], &mesh.normals[mesh.polygon_vertices[j]], &polygon_normal)

    for i in range(mesh.n_vertices):
        vec3_normalize(&mesh.normals[i], &mesh.normals[i])
