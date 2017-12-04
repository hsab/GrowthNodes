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
    def __init__(self, t_start = 0, t_size = 0):
        self.t_start = t_start
        self.t_size = t_size

class CompilationError(Exception):
    pass

class CyclicNodeGraphError(CompilationError):
    pass

class UMOGTypeError(CompilationError):
    pass

def binary_scalar(a, b):
    assert_type(a, ARRAY)
    assert_type(b, ARRAY)

    channels = broadcast_channels(a, b)
    x_size, y_size, z_size = broadcast_dimensions(a, b)
    t_start, t_size = broadcast_time(a, b)

    return [Array(channels, x_size, y_size, z_size, t_start, t_size)]

def assert_type(type, tag):
    if type.tag != tag:
        raise UMOGTypeError()

def broadcast_channels(a, b):
    if a.channels == b.channels:
        channels = a.channels
    elif a.channels == 0:
        channels = b.channels
    elif b.channels == 0:
        channels = a.channels
    else:
        raise UMOGTypeError()

    return channels

def broadcast_dimensions(a, b):
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

    return x_size, y_size, z_size

def broadcast_time(a, b):
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

    return t_start, t_size
