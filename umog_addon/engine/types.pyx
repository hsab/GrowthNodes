class Type:
    pass

class Scalar(Type):
    tag = SCALAR

class Vector(Type):
    tag = VECTOR
    def __init__(self, channels):
        self.channels = channels

class Array(Type):
    tag = ARRAY
    def __init__(self, channels, x_size, y_size, z_size, t_start, t_size):
        self.channels = channels
        self.x_size = x_size; self.y_size = y_size; self.z_size = z_size
        self.t_start = t_start; self.t_size = t_size

class Function(Type):
    tag = FUNCTION
    def __init__(self, channels, dimensions, time):
        self.channels = channels; self.dimensions = dimensions; self.time = time

class Mesh(Type):
    tag = MESH
