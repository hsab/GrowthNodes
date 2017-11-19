class Type:
    tag = NONE

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

def binary_scalar(a, b):
    if a.channels == b.channels:
        channels = a.channels
    elif a.channels == 0:
        channels = b.channels
    elif b.channels == 0:
        channels = a.channels
    else:
        raise UMOGTypeError()

    if a.x_size == b.x_size and a.y_size == b.y_size and a.z_size == b.z_size:
        x_size = a.x_size
        y_size = a.y_size
        z_size = a.z_size
    elif a.x_size == 0 and a.y_size == 0 and a.z_size == 0:
        x_size = b.x_size
        y_size = b.y_size
        z_size = b.z_size
    elif b.x_size == 0 and b.y_size == 0 and b.z_size == 0:
        x_size = a.x_size
        y_size = a.y_size
        z_size = a.z_size
    else:
        raise UMOGTypeError()

    if a.t_start == b.t_start and a.t_size == b.t_size:
        t_start = a.t_start
        t_size = a.t_size
    elif a.t_size == 0:
        t_start = b.t_start
        t_size = b.t_size
    elif b.t_size == 0:
        t_start = a.t_start
        t_size = a.t_size
    else:
        raise UMOGTypeError()

    return [Array(channels, x_size, y_size, z_size, t_start, t_size)]

def assert_type(type, tag):
    if type.tag != tag:
        raise UMOGTypeError()
