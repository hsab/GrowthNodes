import cython

from libc.stdint cimport uintptr_t
from libc.string cimport memset, memcpy
from libc.math cimport atan2, asin, M_PI

from ..packages.cymem.cymem cimport Pool

from data cimport *
from array cimport *

cdef class Mesh(Data):
    def __init__(Mesh self):
        self.tag = MESH
        self.mem = Pool()

cdef void allocate(Mesh mesh, int n_vertices, int n_triangles):
    mesh.n_vertices = n_vertices
    mesh.n_triangles = n_triangles

    mesh.vertices = <Vec3 *>mesh.mem.alloc(n_vertices, sizeof(Vec3))
    mesh.normals = <Vec3 *>mesh.mem.alloc(n_vertices, sizeof(Vec3))
    mesh.uvs = <Vec2 *>mesh.mem.alloc(n_vertices, sizeof(Vec2))
    mesh.triangles = <int *>mesh.mem.alloc(n_triangles * 3, sizeof(int))

@cython.boundscheck(False)
cdef void from_blender_mesh(Mesh mesh, BlenderMesh *blender_mesh):
    cdef int i, j

    cdef int n_vertices = blender_mesh.totvert, n_triangles = blender_mesh.totface
    for i in range(blender_mesh.totface):
        if blender_mesh.mface[i].v4:
            n_triangles += 1

    allocate(mesh, n_vertices, n_triangles)

    cdef Vec3 normalized
    with nogil:
        for i in range(blender_mesh.totvert):
            mesh.vertices[i].x = blender_mesh.mvert[i].co[0]
            mesh.vertices[i].y = blender_mesh.mvert[i].co[1]
            mesh.vertices[i].z = blender_mesh.mvert[i].co[2]

            mesh.normals[i].x = blender_mesh.mvert[i].no[0]
            mesh.normals[i].y = blender_mesh.mvert[i].no[1]
            mesh.normals[i].z = blender_mesh.mvert[i].no[2]
            vec3_normalize(&mesh.normals[i], &mesh.normals[i])

        j = 0
        for i in range(blender_mesh.totface):
            mesh.triangles[j * 3] = blender_mesh.mface[i].v1
            mesh.triangles[j * 3 + 1] = blender_mesh.mface[i].v2
            mesh.triangles[j * 3 + 2] = blender_mesh.mface[i].v3
            j += 1

            if blender_mesh.mface[i].v4:
                mesh.triangles[j * 3] = blender_mesh.mface[i].v1
                mesh.triangles[j * 3 + 1] = blender_mesh.mface[i].v3
                mesh.triangles[j * 3 + 2] = blender_mesh.mface[i].v4
                j += 1

        if blender_mesh.mtface:
            j = 0
            for i in range(blender_mesh.totface):
                mesh.uvs[mesh.triangles[j * 3]].x = blender_mesh.mtface[i].uv[0][0]
                mesh.uvs[mesh.triangles[j * 3]].y = blender_mesh.mtface[i].uv[0][1]
                mesh.uvs[mesh.triangles[j * 3 + 1]].x = blender_mesh.mtface[i].uv[1][0]
                mesh.uvs[mesh.triangles[j * 3 + 1]].y = blender_mesh.mtface[i].uv[1][1]
                mesh.uvs[mesh.triangles[j * 3 + 2]].x = blender_mesh.mtface[i].uv[2][0]
                mesh.uvs[mesh.triangles[j * 3 + 2]].y = blender_mesh.mtface[i].uv[2][1]
                j += 1

                if blender_mesh.mface[i].v4:
                    mesh.uvs[mesh.triangles[j * 3]].x = blender_mesh.mtface[i].uv[0][0]
                    mesh.uvs[mesh.triangles[j * 3]].y = blender_mesh.mtface[i].uv[0][1]
                    mesh.uvs[mesh.triangles[j * 3 + 1]].x = blender_mesh.mtface[i].uv[2][0]
                    mesh.uvs[mesh.triangles[j * 3 + 1]].y = blender_mesh.mtface[i].uv[2][1]
                    mesh.uvs[mesh.triangles[j * 3 + 2]].x = blender_mesh.mtface[i].uv[3][0]
                    mesh.uvs[mesh.triangles[j * 3 + 2]].y = blender_mesh.mtface[i].uv[3][1]
                    j += 1
        else:
            i = 0
            for i in range(mesh.n_vertices):
                vec3_normalize(&normalized, &mesh.vertices[i])
                mesh.uvs[i].x = 0.5 + atan2(-normalized.z, -normalized.x)
                mesh.uvs[i].y = 0.5 - asin(-normalized.y / M_PI)

@cython.boundscheck(False)
cpdef void to_blender_mesh(Mesh mesh, object b_mesh):
    b_mesh.vertices.add(mesh.n_vertices)
    b_mesh.loops.add(mesh.n_triangles * 3)
    b_mesh.polygons.add(mesh.n_triangles)

    cdef BlenderMesh *blender_mesh = <BlenderMesh *><uintptr_t>b_mesh.as_pointer()

    cdef int i
    with nogil:
        for i in range(mesh.n_vertices):
            blender_mesh.mvert[i].co[0] = mesh.vertices[i].x
            blender_mesh.mvert[i].co[1] = mesh.vertices[i].y
            blender_mesh.mvert[i].co[2] = mesh.vertices[i].z

            blender_mesh.mvert[i].no[0] = mesh.normals[i].x
            blender_mesh.mvert[i].no[1] = mesh.normals[i].y
            blender_mesh.mvert[i].no[2] = mesh.normals[i].z

        for i in range(mesh.n_triangles):
            blender_mesh.mloop[i * 3].v = mesh.triangles[i * 3]
            blender_mesh.mloop[i * 3 + 1].v = mesh.triangles[i * 3 + 1]
            blender_mesh.mloop[i * 3 + 2].v = mesh.triangles[i * 3 + 2]

            blender_mesh.mpoly[i].loopstart = i * 3
            blender_mesh.mpoly[i].totloop = 3

    # if blender_mesh.mloopuv:
    #     for i in range(mesh.n_triangles):
    #         blender_mesh.mloopuv[i * 3].uv[0] = mesh.uvs[i * 3].x
    #         blender_mesh.mloopuv[i * 3].uv[1] = mesh.uvs[i * 3].y
    #         blender_mesh.mloopuv[i * 3 + 1].uv[0] = mesh.uvs[i * 3 + 1].x
    #         blender_mesh.mloopuv[i * 3 + 1].uv[1] = mesh.uvs[i * 3 + 1].y
    #         blender_mesh.mloopuv[i * 3 + 2].uv[0] = mesh.uvs[i * 3 + 2].x
    #         blender_mesh.mloopuv[i * 3 + 2].uv[1] = mesh.uvs[i * 3 + 2].y

cdef Mesh copy_mesh(Mesh old):
    cdef Mesh new = Mesh()
    allocate(new, old.n_vertices, old.n_triangles)
    memcpy(new.vertices, old.vertices, old.n_vertices * sizeof(Vec3))
    memcpy(new.normals, old.normals, old.n_vertices * sizeof(Vec3))
    memcpy(new.uvs, old.uvs, old.n_vertices * sizeof(Vec2))
    memcpy(new.triangles, old.triangles, old.n_triangles * 3 * sizeof(int))
    return new

cdef void displace(Mesh mesh, Array texture):
    cdef int i
    cdef float value
    cdef Vec3 normal
    for i in range(mesh.n_vertices):
        value = sample_texture(texture, mesh.vertices[i].x, mesh.vertices[i].y, mesh.vertices[i].z)
        vec3_scale(&normal, value, &mesh.normals[i])
        vec3_add(&mesh.vertices[i], &mesh.vertices[i], &normal)

    recalculate_normals(mesh)

cdef void iterated_displace(Mesh mesh, Array texture, int iterations):
    cdef int i, t
    cdef float value
    cdef Vec3 normal
    for t in range(iterations):
        for i in range(mesh.n_vertices):
            value = sample_texture(texture, mesh.vertices[i].x, mesh.vertices[i].y, mesh.vertices[i].z)
            vec3_scale(&normal, value, &mesh.normals[i])
            vec3_add(&mesh.vertices[i], &mesh.vertices[i], &normal)

        recalculate_normals(mesh)

@cython.cdivision(True)
cdef void recalculate_normals(Mesh mesh):
    cdef int i
    cdef Vec3 *a
    cdef Vec3 *b
    cdef Vec3 *c
    cdef Vec3 ab, ac
    cdef Vec3 triangle_normal

    memset(mesh.normals, 0, mesh.n_vertices * sizeof(Vec3))

    for i in range(mesh.n_triangles):
        a = &mesh.vertices[mesh.triangles[i * 3]]
        b = &mesh.vertices[mesh.triangles[i * 3 + 1]]
        c = &mesh.vertices[mesh.triangles[i * 3 + 2]]

        vec3_sub(&ab, b, a)
        vec3_sub(&ac, c, a)
        vec3_cross(&triangle_normal, &ab, &ac)

        vec3_add(&mesh.normals[mesh.triangles[i * 3]], &mesh.normals[mesh.triangles[i * 3]], &triangle_normal)
        vec3_add(&mesh.normals[mesh.triangles[i * 3 + 1]], &mesh.normals[mesh.triangles[i * 3 + 1]], &triangle_normal)
        vec3_add(&mesh.normals[mesh.triangles[i * 3 + 2]], &mesh.normals[mesh.triangles[i * 3 + 2]], &triangle_normal)

    for i in range(mesh.n_vertices):
        vec3_normalize(&mesh.normals[i], &mesh.normals[i])
