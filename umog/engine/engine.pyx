import numpy as np
cimport numpy as np

import bpy

import cython
cimport cython
from cpython.ref cimport PyObject
from libc.stdlib cimport malloc, free
from libc.stdint cimport uintptr_t

from libc.math cimport fmod

import types
cimport types
from data cimport *
cimport mesh
from mesh cimport Mesh, BlenderMesh
cimport array
from array cimport Array

from collections import namedtuple
from enum import Enum

# operation

Operation = namedtuple('Operation', ['opcode', 'output_types', 'buffer_types', 'arguments', 'parameters'])
class ArgumentType(Enum):
    SOCKET = 0
    BUFFER = 1
Argument = namedtuple('Argument', ['type', 'index'])

# engine

cdef class Engine:
    cdef list buffers
    cdef list instructions
    cdef list outputs

    def __init__(self, list nodes):
        self.instructions = []
        self.buffers = []
        self.outputs = []

        buffer_types = []

        index = 0
        indices = {}

        cdef object output_type
        for (node_i, (node, inputs)) in enumerate(nodes):
            input_types = []
            for input in inputs:
                if input is None:
                    input_types.append(types.Type())
                else:
                    input_types.append(buffer_types[indices[input]])
            operation = node.get_operation(input_types)
            buffer_values = node.get_buffer_values()

            instruction = Instruction()
            instruction.op = operation.opcode
            for (i, parameter) in enumerate(operation.parameters):
                instruction.parameters[i] = parameter

            # create internal buffers
            buffer_indices = []
            for (buffer_i, buffer_value) in enumerate(buffer_values):
                self.buffers.append(create_buffer(operation.buffer_types[buffer_i], buffer_value))
                buffer_types.append(operation.buffer_types[buffer_i])
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
                    buffer_types.append(output_type)
                    index += 1

                self.instructions.append(instruction)

            if node._IsOutputNode:
                self.outputs.append((node, instruction.ins[0]))

    def run(self):
        self.debug()

        cdef Instruction instruction
        for instruction in self.instructions:
            if instruction.op == ADD:
                add(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == SUBTRACT:
                sub(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == MULTIPLY:
                mul(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == DIVIDE:
                div(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == NEGATE:
                neg(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == POWER:
                pow(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == MODULUS:
                mod(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])

            elif instruction.op == EQ:
                eq(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == NEQ:
                neq(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == LT:
                lt(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == GT:
                gt(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == LEQ:
                leq(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == GEQ:
                geq(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])

            elif instruction.op == NOT:
                boolean_not(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == AND:
                boolean_and(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == OR:
                boolean_or(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == XOR:
                boolean_xor(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])

            elif instruction.op == MULTIPLY_MATRIX_MATRIX:
                multiply_matrix_matrix(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == MULTIPLY_MATRIX_VECTOR:
                multiply_matrix_vector(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])

            elif instruction.op == CONVOLVE:
                convolve(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == REACTION_DIFFUSION_STEP:
                for i in range(100):
                    reaction_diffusion_step(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], instruction.parameters[0], instruction.parameters[1], instruction.parameters[2], instruction.parameters[3], instruction.parameters[4])
                    array.copy_array(<Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.outs[0]])

            elif instruction.op == DISPLACE:
                # don't copy if we're mutating in place
                if instruction.outs[0] != instruction.ins[0]:
                    self.buffers[instruction.outs[0]] = mesh.copy_mesh((<Mesh>self.buffers[instruction.ins[0]]))
                mesh.displace((<Mesh>self.buffers[instruction.outs[0]]), (<Array>self.buffers[instruction.ins[1]]))
            elif instruction.op == ITERATED_DISPLACE:
                if instruction.outs[0] != instruction.ins[0]:
                    self.buffers[instruction.outs[0]] = mesh.copy_mesh((<Mesh>self.buffers[instruction.ins[0]]))
                mesh.iterated_displace((<Mesh>self.buffers[instruction.outs[0]]), (<Array>self.buffers[instruction.ins[1]]), instruction.parameters[0])

            elif instruction.op == LOOP:
                pass
            elif instruction.op == CONST:
                pass
            elif instruction.op == NOP:
                pass

        # output values
        for (output_node, buffer_i) in self.outputs:
            if (<Data>self.buffers[buffer_i]).tag == ARRAY:
                output_node.output_value((<Array>self.buffers[buffer_i]))
            elif (<Data>self.buffers[buffer_i]).tag == MESH:
                output_node.output_value((<Mesh>self.buffers[buffer_i]))

    def debug(self):
        print('instructions:')
        cdef Instruction instruction
        cdef int i
        for (i, instruction) in enumerate(self.instructions):
            print(str(i) + '. ' + str((instruction.op, instruction.ins, instruction.outs)))

        print('buffers:')
        cdef Data data
        for (i,data) in enumerate(self.buffers):
            print(str(i) + '. ' + str(data.tag))

def create_buffer(buffer_type, value=None):
    cdef Array arr
    cdef Mesh m
    cdef BlenderMesh *blender_mesh
    if buffer_type.tag == types.ARRAY:
        arr = Array(
            max(buffer_type.channels, 1),
            max(buffer_type.x_size, 1), max(buffer_type.y_size, 1), max(buffer_type.z_size, 1),
            max(buffer_type.t_size, 1))
        if value is not None:
            array.from_memoryview(arr, <np.ndarray[float, ndim=5, mode="fortran"]>value)
        else:
            array.clear(arr)
        return arr
    elif buffer_type.tag == types.MESH:
        m = Mesh()
        if value is not None:
            blender_mesh = <BlenderMesh *><uintptr_t>value.as_pointer()
            mesh.allocate(m, blender_mesh.totvert, blender_mesh.totloop, blender_mesh.totpoly)
            mesh.from_blender_mesh(m, blender_mesh)
        return m

cpdef float[:,:,:,:,:] sequence(int start, int end):
    cdef int i
    cdef float[:,:,:,:,:] result = np.ndarray(shape=(1,1,1,1,end-start), dtype=np.float32, order="F")
    for i in range(start, end):
        result[0,0,0,0,i] = <float>i
    return result
