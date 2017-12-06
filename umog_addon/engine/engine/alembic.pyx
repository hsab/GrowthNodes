# # distutils: language = c++
# # distutils: extra_compile_args = -I/usr/local/include/OpenEXR -std=c++11
# # distutils: libraries = Alembic

# from libcpp.string cimport string
# from libc.stdint cimport *
# from libc.stdlib cimport malloc, free

# from mesh cimport Mesh, MeshSequence

# cdef extern from "Alembic/Abc/All.h" namespace "Alembic::Abc":
#     cdef cppclass OArchive:
#         OArchive(ArchiveWriterPtr iPtr, WrapExistingFlag, Policy iPolicy)
#         OObject getTop()

#     cdef cppclass OObject:
#         OObject(OArchive &iArchive)

#     cdef cppclass Argument:
#         pass

#     enum WrapExistingFlag:
#         kWrapExisting

#     cdef cppclass V3fArraySample:
#         V3fArraySample(const V3f *iValues, size_t iNumVals) 
#     cdef cppclass Int32ArraySample:
#         Int32ArraySample(const int32_t *iValues, size_t iNumVals) 

# cdef extern from "Alembic/Abc/All.h" namespace "Alembic::Abc::ErrorHandler":
#     enum Policy:
#         kQuietNoopPolicy
#         kNoisyNoopPolicy
#         kThrowPolicy

# cdef extern from "Alembic/Abc/All.h" namespace "Imath":
#     cdef cppclass V3f:
#         float x, y, z

# cdef extern from "Alembic/AbcCoreAbstract/All.h" namespace "Alembic::AbcCoreAbstract":
#     cdef cppclass ArchiveWriterPtr:
#         pass
#     cdef cppclass MetaData:
#         pass

# cdef extern from "Alembic/AbcCoreOgawa/All.h" namespace "Alembic::AbcCoreOgawa":
#     cdef cppclass WriteArchive:
#         WriteArchive() 
#         ArchiveWriterPtr operator()(const string &iFileName, const MetaData &iMetaData) 

# cdef extern from "Alembic/AbcGeom/OPolyMesh.h" namespace "Alembic::AbcGeom":
#     cdef cppclass OPolyMesh:
#         OPolyMesh(OObject iParent, const string &iName)
#         OPolyMeshSchema &getSchema() 

#     cdef cppclass OPolyMeshSchema:
#         void set(const OPolyMeshSchemaSample &iSamp)

#     enum GeometryScope:
#         kConstantScope = 0
#         kUniformScope = 1
#         kVaryingScope = 2
#         kVertexScope = 3
#         kFacevaryingScope = 4

#         kUnknownScope = 127

# cdef extern from "Alembic/AbcGeom/OGeomParam.h":
#     cdef cppclass ON3fGeomParamSample "Alembic::AbcGeom::ON3fGeomParam::Sample":
#         void setScope(GeometryScope iScope) 
#         void setVals(const V3fArraySample &iVals) 

# cdef extern from "Alembic/AbcGeom/OPolyMesh.h":
#     cdef cppclass OPolyMeshSchemaSample "Alembic::AbcGeom::OPolyMeshSchema::Sample":
#         OPolyMeshSchemaSample(const V3fArraySample &iPos,
#                 const Int32ArraySample &iInd,
#                 const Int32ArraySample &iCnt) 
#         void setNormals(const ON3fGeomParamSample &iNormals) 

# cdef export_mesh_sequence_(MeshSequence mesh_sequence, string filename):
#     cdef WriteArchive archive_writer
#     cdef MetaData md
#     cdef OArchive *archive
#     cdef OObject *obj
#     cdef OPolyMesh *poly_mesh
#     cdef OPolyMeshSchema mesh_schema
#     cdef int i
#     cdef Mesh mesh
#     cdef V3f *vertices
#     cdef int32_t *poly_verts
#     cdef int32_t *loop_counts
#     cdef OPolyMeshSchemaSample *mesh_sample
#     cdef V3f *normals
#     cdef ON3fGeomParamSample normals_sample

#     try:
#         # md.set("FramesPerTimeUnit", str_fps)
#         archive = new OArchive(archive_writer(filename, md), kWrapExisting, kThrowPolicy)
#         obj = new OObject(archive[0])
#         poly_mesh = new OPolyMesh(obj[0], "mesh")
#         mesh_schema = poly_mesh.getSchema()

#         for mesh in mesh_sequence.frames:
#             if mesh.n_vertices > 0 and mesh.n_triangles > 0:
#                 try:
#                     vertices = <V3f *>malloc(mesh.n_vertices * sizeof(V3f))
#                     for i in range(mesh.n_vertices):
#                         # store as y-up
#                         vertices[i].x = mesh.vertices[i].x
#                         vertices[i].y = mesh.vertices[i].z
#                         vertices[i].z = -mesh.vertices[i].y

#                     poly_verts = <int32_t *>malloc(mesh.n_triangles * 3 * sizeof(int32_t))
#                     loop_counts = <int32_t *>malloc(mesh.n_triangles * sizeof(int32_t))
#                     for i in range(mesh.n_triangles):
#                         # wind clockwise
#                         poly_verts[i * 3] = mesh.triangles[i * 3]
#                         poly_verts[i * 3 + 1] = mesh.triangles[i * 3 + 2]
#                         poly_verts[i * 3 + 2] = mesh.triangles[i * 3 + 1]
#                         loop_counts[i] = 3

#                     mesh_sample = new OPolyMeshSchemaSample(
#                         V3fArraySample(vertices, mesh.n_vertices),
#                         Int32ArraySample(poly_verts, mesh.n_triangles * 3),
#                         Int32ArraySample(loop_counts, mesh.n_triangles))

#                     normals = <V3f *>malloc(mesh.n_vertices * sizeof(V3f))
#                     for i in range(mesh.n_vertices):
#                         # store as y-up
#                         normals[i].x = mesh.normals[i].x
#                         normals[i].y = mesh.normals[i].z
#                         normals[i].z = -mesh.normals[i].y

#                     normals_sample.setScope(kVertexScope)
#                     normals_sample.setVals(V3fArraySample(normals, mesh.n_vertices))

#                     mesh_sample.setNormals(normals_sample)

#                     mesh_schema.set(mesh_sample[0])
#                 finally:
#                     pass
#                     # free(vertices)
#                     # free(poly_verts)
#                     # free(loop_counts)
#                     # free(normals)
#     finally:
#         del archive
#         del obj
#         del poly_mesh
#         del mesh_sample

# def export_mesh_sequence(MeshSequence mesh_sequence, string filename):
#     export_mesh_sequence_(mesh_sequence, filename)
