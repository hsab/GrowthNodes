import numpy as np
cimport numpy as np

import bpy

import cython
cimport cython
from cpython.ref cimport PyObject
from libc.stdlib cimport malloc, free

import types
cimport types
import mesh
cimport mesh

# data

cdef class ArrayData:
    def __init__(self):
        self.tag = ARRAY

cdef class MeshData:
    def __init__(self):
        self.tag = MESH

# engine

cdef class Engine:
    cdef size_t buffers_count
    cdef Data *buffers
    
    cdef size_t instructions_count
    cdef Instruction *instructions

    def __init__(self, list nodes):
        index = 0
        indices = {}

        self.instructions_count = len(nodes)
        self.instructions = <Instruction *>malloc(self.instructions_count * sizeof(Instruction))

        self.buffers_count = 0
        for (node, inputs) in nodes:
            self.buffers_count += len(node.outputs)
        self.buffers = <Data *>malloc(self.buffers_count * sizeof(Data))

        # cdef types.Type output_type
        for (node_i, (node, inputs)) in enumerate(nodes):
            operation = node.operation()
            input_types = node.input_types()
            output_types = node.output_types()

            self.instructions[node_i].op = operation

            for (socket_i, output) in enumerate(node.outputs):
                indices[(node_i, socket_i)] = index
                self.instructions[node_i].outs[socket_i] = index

                output_type = output_types[socket_i]
                if output_type.tag == types.SCALAR:
                    self.buffers[index].tag = ARRAY
                    self.buffers[index].contents.array = np.ndarray(shape=(1,1,1,1,1), dtype=np.float32)
                elif output_type.tag == types.VECTOR:
                    self.buffers[index].tag = ARRAY
                    self.buffers[index].contents.array = np.ndarray(shape=(output_type.contents.vector.channels,1,1,1,1), dtype=np.float32)
                elif output_type.tag == types.ARRAY:
                    self.buffers[index].tag = ARRAY
                    self.buffers[index].contents.array = np.ndarray(shape=(
                        output_type.contents.array.channels,
                        output_type.contents.array.x_size,
                        output_type.contents.array.y_size,
                        output_type.contents.array.z_size,
                        output_type.contents.array.t_size), dtype=np.float32)
                elif output_type.tag == types.FUNCTION:
                    pass
                elif output_type.tag == types.MESH:
                    self.buffers[index].tag = MESH

                index += 1

            for (input_i, (node_index, socket_index)) in enumerate(inputs):
                self.instructions[node_i].ins[input_i] = indices[(node_index, socket_index)]

    def __dealloc__(self):
        free(self.instructions)
        free(self.buffers)
