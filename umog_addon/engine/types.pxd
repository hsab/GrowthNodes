cdef struct VectorType:
    int channels

cdef struct ArrayType:
    int channels
    int x_size
    int y_size
    int z_size
    int t_start
    int t_size

cdef struct FunctionType:
    int channels
    int dimensions
    bint time

cdef enum TypeTag:
    SCALAR, VECTOR, ARRAY, FUNCTION, MESH

cdef union TypeContents:
    VectorType vector
    ArrayType array
    FunctionType function
    # currently no parameters for MESH
