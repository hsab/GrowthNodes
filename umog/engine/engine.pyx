import numpy as np
cimport numpy as np
from numpy import linalg as la

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
from mesh cimport Mesh, MeshSequence, BlenderMesh
cimport array
from array cimport Array

from collections import namedtuple
from enum import Enum

from . import reaction_diffusion_gpu

# operation

Operation = namedtuple('Operation', ['opcode', 'argument_types', 'output_types', 'parameters'])

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

            instruction = Instruction()
            instruction.op = operation.opcode
            for (i, parameter) in enumerate(operation.parameters):
                instruction.parameters[i] = parameter

            # hook up arguments
            buffer_indices = []
            for (argument_i, argument_type) in enumerate(operation.argument_types):
                if argument_i < len(input_types) and input_types[argument_i].tag != types.NONE:
                    instruction.ins[argument_i] = indices[inputs[argument_i]]
                else:
                    self.buffers.append(create_buffer(argument_type, node.get_default_value(argument_i, argument_type)))
                    buffer_types.append(argument_type)
                    buffer_indices.append(index)
                    instruction.ins[argument_i] = index
                    index += 1

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

    cpdef run(self):
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

            elif instruction.op == MATRIX_TRANSPOSE:
                matrix_transpose(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == MATRIX_NORM_FRO:
                matrix_norm_fro(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == MATRIX_NORM_1:
                matrix_norm_1(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == MATRIX_NORM_2:
                matrix_norm_2(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == MATRIX_NORM_INF:
                matrix_norm_inf(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == MATRIX_INVERSE:
                matrix_inverse(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == MATRIX_DETERMINANT:
                matrix_determinant(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]])
            elif instruction.op == MULTIPLY_MATRIX_MATRIX:
                multiply_matrix_matrix(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == MULTIPLY_MATRIX_VECTOR:
                multiply_matrix_vector(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])

            elif instruction.op == CONVOLVE:
                convolve(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.ins[1]])
            elif instruction.op == REACTION_DIFFUSION_STEP:
                options = <Array>self.buffers[instruction.ins[1]]
                for i in range(instruction.parameters[0]):
                    reaction_diffusion_step(<Array>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[0]], options.array[0,0,0,0,0], options.array[1,0,0,0,0], options.array[2,0,0,0,0], options.array[3,0,0,0,0], options.array[4,0,0,0,0])
                    array.copy_array(<Array>self.buffers[instruction.ins[0]], <Array>self.buffers[instruction.outs[0]])

            elif instruction.op == DISPLACE:
                # don't copy if we're mutating in place
                if instruction.outs[0] != instruction.ins[0]:
                    self.buffers[instruction.outs[0]] = mesh.copy_mesh((<Mesh>self.buffers[instruction.ins[0]]))
                mesh.displace((<Mesh>self.buffers[instruction.outs[0]]), (<Array>self.buffers[instruction.ins[1]]))
            elif instruction.op == DISPLACE_SEQUENCE:
                pass
            elif instruction.op == ITERATED_DISPLACE:
                self.buffers[instruction.outs[0]].frames[0] = mesh.copy_mesh((<Mesh>self.buffers[instruction.ins[0]]))
                mesh.iterated_displace(<Mesh>self.buffers[instruction.outs[0]], <Array>self.buffers[instruction.ins[1]])

            elif instruction.op == LOOP:
                pass
            elif instruction.op == CONST:
                pass
            elif instruction.op == NOP:
                pass
            
            elif instruction.op == REACTION_DIFFUSION_GPU_STEP:
                options = <Array>self.buffers[instruction.ins[2]]
                reaction_diffusion_gpu.reaction_diffusion_gpu(
                    <Array>self.buffers[instruction.outs[0]],
                    <Array>self.buffers[instruction.outs[1]],
                    <Array>self.buffers[instruction.ins[0]], 
                    <Array>self.buffers[instruction.ins[1]],
                    options.array[0,0,0,0,0], 
                    options.array[1,0,0,0,0], 
                    options.array[2,0,0,0,0], 
                    options.array[3,0,0,0,0], 
                    options.array[4,0,0,0,0],
                    options.array[5,0,0,0,0]
                    )
                
            elif instruction.op == LATHE_GPU:
                reaction_diffusion_gpu.lathe_gpu(
                    <Array>self.buffers[instruction.outs[0]],
                    <Array>self.buffers[instruction.ins[0]],
                    instruction.parameters[0]
                    )
            elif instruction.op == SHAPE_GPU:
                options = <Array>self.buffers[instruction.ins[1]]
                reaction_diffusion_gpu.pre_def_3dtexture(
                    <Array>self.buffers[instruction.outs[0]],
                    options.array[0,0,0,0,0], 
                    options.array[1,0,0,0,0],
                    int(instruction.parameters[1]),
                    instruction.parameters[0]
                    )
            elif instruction.op == SOLID_GEOMETRY_GPU:
                options = <Array>self.buffers[instruction.ins[2]]
                reaction_diffusion_gpu.solid_geometry(
                    <Array>self.buffers[instruction.outs[0]],
                    <Array>self.buffers[instruction.ins[0]],
                    <Array>self.buffers[instruction.ins[1]],
                    instruction.parameters[0],
                    options.array[0,0,0,0,0]
                    )
            elif instruction.op == MUX_CHANNELS:
                reaction_diffusion_gpu.mux_channels(
                    <Array>self.buffers[instruction.outs[0]],
                    <Array>self.buffers[instruction.ins[0]],
                    [
                        instruction.parameters[0],
                        instruction.parameters[1],
                        instruction.parameters[2],
                        instruction.parameters[3],
                    ]
                    )
            elif instruction.op == REACTION_DIFFUSION_VOXEL_GPU:
                options = <Array>self.buffers[instruction.ins[2]]
                reaction_diffusion_gpu.reaction_diffusion_3d_gpu(
                    <Array>self.buffers[instruction.outs[0]],
                    <Array>self.buffers[instruction.outs[1]],
                    <Array>self.buffers[instruction.ins[0]], 
                    <Array>self.buffers[instruction.ins[1]],
                    options.array[0,0,0,0,0], 
                    options.array[1,0,0,0,0], 
                    options.array[2,0,0,0,0], 
                    options.array[3,0,0,0,0], 
                    options.array[4,0,0,0,0],
                    options.array[5,0,0,0,0]
                    )
            elif instruction.op == TRANSFORM_GPU:
                options = <Array>self.buffers[instruction.ins[1]]
                reaction_diffusion_gpu.transformation(
                    <Array>self.buffers[instruction.outs[0]],
                    <Array>self.buffers[instruction.ins[0]], 
                    options, 
                    )

                

        # output values
        for (output_node, buffer_i) in self.outputs:
            if (<Data>self.buffers[buffer_i]).tag == ARRAY:
                output_node.output_value((<Array>self.buffers[buffer_i]))
            elif (<Data>self.buffers[buffer_i]).tag == MESH:
                output_node.output_value((<Mesh>self.buffers[buffer_i]))
            elif (<Data>self.buffers[buffer_i]).tag == MESH_SEQUENCE:
                output_node.output_value((<MeshSequence>self.buffers[buffer_i]))

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
    cdef MeshSequence ms
    cdef BlenderMesh *blender_mesh
    if buffer_type.tag == types.ARRAY:
        arr = Array(
            max(buffer_type.channels, 1),
            max(buffer_type.x_size, 1), max(buffer_type.y_size, 1), max(buffer_type.z_size, 1),
            max(buffer_type.t_size, 1))
        if isinstance(value, np.ndarray):
            array.from_memoryview(arr, <np.ndarray[float, ndim=5, mode="fortran"]>value)
        elif isinstance(value, bpy.types.Texture):
            array.from_blender_texture(arr, value)
        else:
            array.clear(arr)
        return arr
    elif buffer_type.tag == types.MESH:
        m = Mesh()
        if value is not None:
            blender_mesh = <BlenderMesh *><uintptr_t>value.as_pointer()
            mesh.from_blender_mesh(m, blender_mesh)

        if buffer_type.t_size > 0:
            ms = MeshSequence(buffer_type.t_size)
            ms.frames[0] = m
            return ms
        else:
            return m

cpdef float[:,:,:,:,:] sequence(int start, int end):
    cdef int i
    cdef float[:,:,:,:,:] result = np.ndarray(shape=(1,1,1,1,end-start), dtype=np.float32, order="F")
    for i in range(start, end):
        result[0,0,0,0,i] = <float>i
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_determinant(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = np.asarray(a.array[0, : , :, 0, t])
        out.array[0, 0, 0, 0, t] = la.det(input)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_inverse(Array out, Array a):
    cdef float[:,:] input
    cdef float[:,:] output
    for t in range(out.array.shape[4]):
        input = np.asarray(a.array[0, : , :, 0, t])
        if la.det(input) != 0:
            output = la.inv(input)
            out.array[0, :, :, 0, t] = output
        else:
            out.array = a.array

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_fro(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = np.asarray(a.array[0, : , :, 0, t])
        out.array[0, 0, 0, 0, t] = la.norm(input, 'fro')

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_1(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = np.asarray(a.array[0, : , :, 0, t])
        out.array[0, 0, 0, 0, t] = la.norm(input,1)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_2(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = np.asarray(a.array[0, : , :, 0, t])
        out.array[0, 0, 0, 0, t] = la.norm(input, 2)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void matrix_norm_inf(Array out, Array a):
    cdef np.ndarray[float, ndim=2, mode="fortran"] input
    for t in range(out.array.shape[4]):
        input = np.asarray(a.array[0, : , :, 0, t])
        out.array[0, 0, 0, 0, t] = la.norm(input, np.inf)

