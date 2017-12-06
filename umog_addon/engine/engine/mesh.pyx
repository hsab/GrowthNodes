import cython

from libc.stdint cimport uintptr_t
from libc.string cimport memset, memcpy
from libc.math cimport atan2, asin, acos, fmin, fmax, M_PI
from libc.stdlib cimport qsort
from libc.stdlib cimport malloc, free

from ..packages.cymem.cymem cimport Pool

from data cimport *
from array cimport *

cdef class MeshSequence(Data):
    def __init__(MeshSequence self, int n_frames):
        self.tag = MESH_SEQUENCE
        self.frames = []
        for i in range(n_frames):
            self.frames.append(Mesh())

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
    mesh.opposites = <int *>mesh.mem.alloc(n_triangles * 3, sizeof(int))

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

    build_opposites(mesh)

cdef struct HalfEdge:
    int index, v1, v2

@cython.boundscheck(False)
cdef void build_opposites(Mesh mesh):
    cdef HalfEdge *half_edges = <HalfEdge *>malloc(mesh.n_triangles * 3 * sizeof(HalfEdge))

    cdef int i, tmp
    for i in range(mesh.n_triangles * 3):
        half_edges[i].index = i
        half_edges[i].v1 = mesh.triangles[i]
        half_edges[i].v2 = mesh.triangles[(i / 3) * 3 + (i + 1) % 3]
        if half_edges[i].v2 < half_edges[i].v1:
            tmp = half_edges[i].v1
            half_edges[i].v1 = half_edges[i].v2
            half_edges[i].v2 = tmp

    qsort(<void *>half_edges, mesh.n_triangles * 3, sizeof(HalfEdge), half_edge_cmp)

    cdef HalfEdge prev, curr
    for i in range(1, mesh.n_triangles * 3):
        prev = half_edges[i-1]
        curr = half_edges[i]
        if prev.v1 == curr.v1 and prev.v2 == curr.v2:
            mesh.opposites[prev.index] = curr.index
            mesh.opposites[curr.index] = prev.index

    free(half_edges)

cdef int half_edge_cmp(const void *a_ptr, const void *b_ptr) nogil:
    cdef HalfEdge a = (<HalfEdge *>a_ptr)[0], b = (<HalfEdge *>b_ptr)[0]
    if a.v1 == b.v1:
        return a.v2 - b.v2
    else:
        return a.v1 - b.v1

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
    memcpy(new.opposites, old.opposites, old.n_triangles * 3 * sizeof(int))
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

cdef void iterated_displace(MeshSequence mesh_sequence, Array texture):
    cdef int i, j, t
    cdef Mesh mesh
    cdef float value
    cdef Vec3 normal
    cdef int n_to_subdivide
    cdef int *to_subdivide
    for t in range(1, len(mesh_sequence.frames)):
        mesh = copy_mesh(mesh_sequence.frames[t - 1])
        mesh_sequence.frames[t] = mesh

        for i in range(mesh.n_vertices):
            value = sample_texture(texture, mesh.vertices[i].x, mesh.vertices[i].y, mesh.vertices[i].z)
            vec3_scale(&normal, value, &mesh.normals[i])
            vec3_add(&mesh.vertices[i], &mesh.vertices[i], &normal)

        # subdivide triangles with too high of angle
        n_to_subdivide = 0
        to_subdivide = <int *>malloc(mesh.n_triangles * sizeof(int))
        memset(to_subdivide, 0, mesh.n_triangles * sizeof(int))
        for i in range(mesh.n_triangles):
            if triangle_max_angle(mesh, i) > M_PI / 3:
                to_subdivide[i] = 1
                n_to_subdivide += 1

        # subdivide_triangles(mesh, to_subdivide)

        # print(str(mesh.n_vertices) + " vertices")

        recalculate_normals(mesh)

        free(to_subdivide)

cdef float triangle_max_angle(Mesh mesh, int triangle):
    cdef Vec3 a, b, c
    cdef float angle1, angle2, angle3
    a = mesh.normals[mesh.triangles[triangle * 3]]
    b = mesh.normals[mesh.triangles[triangle * 3 + 1]]
    c = mesh.normals[mesh.triangles[triangle * 3 + 2]]
    angle1 = acos(vec3_dot(&a, &b))
    angle2 = acos(vec3_dot(&b, &c))
    angle3 = acos(vec3_dot(&c, &a))
    return fmax(fmax(angle1, angle2), angle2)

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

cdef void subdivide_triangles(Mesh mesh, int *triangles):
    cdef int *half_edges_split = <int *>malloc(mesh.n_triangles * 3 * sizeof(int))
    memset(half_edges_split, 0, mesh.n_triangles * 3 * sizeof(int))
    cdef int split_edges = 0

    cdef int i, edge
    for i in range(mesh.n_triangles):
        if triangles[i]:
            for edge in range(i * 3, i * 3 + 3):
                if not half_edges_split[edge]:
                    half_edges_split[edge] = 1
                    half_edges_split[mesh.opposites[edge]] = 1
                    split_edges += 1

    cdef int vertices_i = mesh.n_vertices
    cdef int triangles_i = mesh.n_triangles
    cdef int n_triangles_old = mesh.n_triangles
    mesh.n_vertices += split_edges
    mesh.n_triangles += 2 * split_edges

    mesh.vertices = <Vec3 *>mesh.mem.realloc(mesh.vertices, mesh.n_vertices * sizeof(Vec3))
    mesh.normals = <Vec3 *>mesh.mem.realloc(mesh.normals, mesh.n_vertices * sizeof(Vec3))
    mesh.uvs = <Vec2 *>mesh.mem.realloc(mesh.uvs, mesh.n_vertices * sizeof(Vec2))
    mesh.triangles = <int *>mesh.mem.realloc(mesh.triangles, mesh.n_triangles * 3 * sizeof(int))
    mesh.opposites = <int *>mesh.mem.realloc(mesh.opposites, mesh.n_triangles * 3 * sizeof(int))

    cdef int *half_edges_verts = <int *>malloc(n_triangles_old * 3 * sizeof(int))

    for i in range(n_triangles_old * 3):
        half_edges_verts[i] = -1

    cdef Vec3 v1, v2
    for i in range(n_triangles_old):
        for edge in range(i * 3, i * 3 + 3):
            if half_edges_split[edge] and half_edges_verts[edge] == -1:
                half_edges_verts[edge] = vertices_i
                half_edges_verts[mesh.opposites[edge]] = vertices_i

                v1 = mesh.vertices[mesh.triangles[edge]]
                v2 = mesh.vertices[mesh.triangles[i * 3 + (edge + 1) % 3]]
                mesh.vertices[vertices_i] = vec3((v1.x + v2.x) / 2, (v1.y + v2.y) / 2, (v1.z + v2.z) / 2)

                vertices_i += 1

    cdef edge1, edge2
    for i in range(n_triangles_old):
        if half_edges_split[i * 3] and half_edges_split[i * 3 + 1] and half_edges_split[i * 3 + 2]:
            # print("splitting entire triangle " + str(i))
            for edge in range(i * 3, i * 3 + 3):
                edge2 = i * 3 + (edge + 2) % 3
                mesh.triangles[triangles_i * 3] = mesh.triangles[edge]
                mesh.triangles[triangles_i * 3 + 1] = half_edges_verts[edge]
                mesh.triangles[triangles_i * 3 + 2] = half_edges_verts[edge2]
                triangles_i += 1

            mesh.triangles[i * 3] = half_edges_verts[i * 3]
            mesh.triangles[i * 3 + 1] = half_edges_verts[i * 3 + 1]
            mesh.triangles[i * 3 + 2] = half_edges_verts[i * 3 + 2]
        else:
            for edge in range(i * 3, i * 3 + 3):
                edge1 = i * 3 + (edge + 1) % 3
                edge2 = i * 3 + (edge + 2) % 3
                if half_edges_split[edge]:
                    mesh.triangles[triangles_i * 3] = half_edges_verts[edge]
                    mesh.triangles[triangles_i * 3 + 1] = mesh.triangles[edge1]
                    mesh.triangles[triangles_i * 3 + 2] = mesh.triangles[edge2]
                    # print("splitting triangle " + str(i) + " once: " + str(mesh.triangles[triangles_i * 3]) + "," + str(mesh.triangles[triangles_i * 3 + 1]) + "," + str(mesh.triangles[triangles_i * 3 + 2]))
                    triangles_i += 1

                    mesh.triangles[edge1] = half_edges_verts[edge]

                    if half_edges_split[edge1]:
                        mesh.triangles[triangles_i * 3] = half_edges_verts[edge]
                        mesh.triangles[triangles_i * 3 + 1] = mesh.triangles[edge1]
                        mesh.triangles[triangles_i * 3 + 2] = half_edges_verts[edge1]
                        print("splitting triangle " + str(i) + " twice: " + str(mesh.triangles[triangles_i * 3]) + "," + str(mesh.triangles[triangles_i * 3 + 1]) + "," + str(mesh.triangles[triangles_i * 3 + 2]))
                        triangles_i += 1

                        mesh.triangles[(triangles_i - 1) * 3 + 1] = half_edges_verts[edge1]
                        print(str(half_edges_verts[edge1]))
                    elif half_edges_split[edge2]:
                        mesh.triangles[triangles_i * 3] = half_edges_verts[edge2]
                        mesh.triangles[triangles_i * 3 + 1] = half_edges_verts[edge]
                        mesh.triangles[triangles_i * 3 + 2] = mesh.triangles[edge2]
                        print("splitting triangle " + str(i) + " twice: " + str(mesh.triangles[triangles_i * 3]) + "," + str(mesh.triangles[triangles_i * 3 + 1]) + "," + str(mesh.triangles[triangles_i * 3 + 2]))
                        triangles_i += 1

                        mesh.triangles[edge2] = half_edges_verts[edge2]
                        print(str(half_edges_verts[edge2]))

                    break

    free(half_edges_split)
    free(half_edges_verts)

    build_opposites(mesh)
    recalculate_normals(mesh)
