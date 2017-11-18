class Type:
    pass

class Array(Type):
    tag = ARRAY
    def __init__(self, channels, x_size, y_size, z_size, t_start, t_size):
        self.channels = channels
        self.x_size = x_size; self.y_size = y_size; self.z_size = z_size
        self.t_start = t_start; self.t_size = t_size

class Mesh(Type):
    tag = MESH

class CompilationError(Exception):
    pass

class CyclicNodeGraphError(CompilationError):
    pass

class UMOGTypeError(CompilationError):
    pass
