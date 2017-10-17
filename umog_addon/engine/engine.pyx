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

from collections import namedtuple
from enum import Enum

# operation

Operation = namedtuple('Operation', ['opcode', 'input_types', 'output_types', 'buffer_types', 'arguments'])
class ArgumentType(Enum):
    SOCKET = 0
    BUFFER = 1
Argument = namedtuple('Argument', ['type', 'index'])

# data

cdef class ArrayData:
    def __init__(self):
        self.tag = ARRAY

cdef class MeshData:
    def __init__(self):
        self.tag = MESH

# engine

cdef class Engine:
    cdef list buffers
    cdef list instructions

    def __init__(self, list nodes):
        self.instructions = []
        self.buffers = []

        index = 0
        indices = {}

        cdef object output_type
        cdef ArrayData array_data
        cdef MeshData mesh_data
        for (node_i, (node, inputs)) in enumerate(nodes):
            operation = node.get_operation()
            buffer_values = node.get_buffer_values()

            instruction = Instruction()
            instruction.op = operation.opcode

            # create internal buffers
            buffer_indices = []
            for (buffer_i, buffer_value) in enumerate(buffer_values):
                self.buffers.append(create_buffer(operation.buffer_types[buffer_i], buffer_value))
                buffer_indices.append(index)
                index += 1

            # set instruction argument indices
            for (argument_i, argument) in enumerate(operation.arguments):
                if argument.type == ArgumentType.BUFFER:
                    instruction.ins[argument_i] = buffer_indices[argument.index]
                elif argument.type == ArgumentType.SOCKET:
                    instruction.ins[argument_i] = indices[inputs[argument.index]]

            # create output buffers
            if instruction.op == CONST:
                indices[(node_i, 0)] = buffer_indices[0]
            elif instruction.op != NOP:
                for (output_i, output_type) in enumerate(operation.output_types):
                    indices[(node_i, output_i)] = index
                    instruction.outs[output_i] = index
                    self.buffers.append(create_buffer(output_type))
                    index += 1

                self.instructions.append(instruction)

    def run(self):
        cdef Instruction instruction
        for instruction in self.instructions:
            if instruction.op == ADD:
                add(<ArrayData>self.buffers[instruction.outs[0]], <ArrayData>self.buffers[instruction.ins[0]], <ArrayData>self.buffers[instruction.ins[1]])
            elif instruction.op == SUBTRACT:
                pass
            elif instruction.op == MULTIPLY:
                pass
            elif instruction.op == DIVIDE:
                pass
            elif instruction.op == DISPLACE:
                print((<ArrayData>self.buffers[instruction.ins[0]]).array[0,0,0,0,0])
            elif instruction.op == LOOP:
                pass
            elif instruction.op == CONST:
                pass
            elif instruction.op == NOP:
                pass

def create_buffer(buffer_type, value=None):
    if buffer_type.tag == types.SCALAR:
        array_data = ArrayData()
        array_data.array = np.ndarray(shape=(1,1,1,1,1), dtype=np.float32)
        if value is not None:
            array_data.array[0,0,0,0,0] = value
        return array_data
    elif buffer_type.tag == types.VECTOR:
        array_data = ArrayData()
        array_data.array = np.ndarray(shape=(buffer_type.channels,1,1,1,1), dtype=np.float32)
        if value is not None:
            array_data.array[:,0,0,0,0] = value
        return array_data
    elif buffer_type.tag == types.ARRAY:
        array_data = ArrayData()
        if value is None:
            array_data.array = np.ndarray(shape=(
                buffer_type.channels,
                buffer_type.x_size,
                buffer_type.y_size,
                buffer_type.z_size,
                buffer_type.t_size), dtype=np.float32)
        else:
            array_data.array = value
        return array_data
    elif buffer_type.tag == types.FUNCTION:
        pass
    elif buffer_type.tag == types.MESH:
        mesh_data = MeshData()
        if value is not None:
            mesh_data.mesh = value
        return mesh_data

