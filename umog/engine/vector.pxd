from libc.math cimport sqrt

cdef struct Vec3:
    float x, y, z

cdef inline Vec3 vec3(float x, float y, float z) nogil:
    cdef Vec3 v
    v.x = x
    v.y = y
    v.z = z
    return v

cdef inline void vec3_add(Vec3 *out, Vec3 *a, Vec3 *b) nogil:
    out.x = a.x + b.x
    out.y = a.y + b.y
    out.z = a.z + b.z

cdef inline void vec3_sub(Vec3 *out, Vec3 *a, Vec3 *b) nogil:
    out.x = a.x - b.x
    out.y = a.y - b.y
    out.z = a.z - b.z

cdef inline void vec3_scale(Vec3 *out, float s, Vec3 *a) nogil:
    out.x = s * a.x
    out.y = s * a.y
    out.z = s * a.z

cdef inline float vec3_magnitude(Vec3 *a) nogil:
    return sqrt(a.x * a.x + a.y * a.y + a.z * a.z)

cdef inline void vec3_normalize(Vec3 *out, Vec3 *a) nogil:
    cdef float length = vec3_magnitude(a)
    out.x = a.x / length
    out.y = a.y / length
    out.z = a.z / length

cdef inline float vec3_dot(Vec3 *a, Vec3 *b) nogil:
    return a.x * b.x + a.y * b.y + a.z * b.z

cdef inline void vec3_cross(Vec3 *out, Vec3 *a, Vec3 *b) nogil:
    out.x = a.y * b.z - a.z * b.y
    out.y = a.z * b.x - a.x * b.z
    out.z = a.x * b.y - a.y * b.x

cdef struct Vec2:
    float x, y
