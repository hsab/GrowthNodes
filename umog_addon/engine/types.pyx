cdef class Type:
    cdef TypeTag tag
    cdef TypeContents contents

    @staticmethod
    def scalar():
        cdef Type t = Type()
        t.tag = SCALAR
        return t

    @staticmethod
    def vector(int channels):
        cdef Type t = Type()
        t.tag = VECTOR
        t.contents.vector.channels = channels
        return t

    @staticmethod
    def array(int channels, int x_size, int y_size, int z_size, int t_start, int t_size):
        cdef Type t = Type()
        t.tag = ARRAY
        t.contents.array.channels = channels
        t.contents.array.x_size = x_size; t.contents.array.y_size = y_size; t.contents.array.z_size = z_size
        t.contents.array.t_start = t_start; t.contents.array.t_size = t_size
        return t

    @staticmethod
    def function(int channels, int dimensions, bint time):
        cdef Type t = Type()
        t.tag = FUNCTION
        t.contents.function.channels = channels; t.contents.function.dimensions = dimensions; t.contents.function.time = time
        return t

    @staticmethod
    def mesh():
        cdef Type t = Type()
        t.tag = MESH
        return t
