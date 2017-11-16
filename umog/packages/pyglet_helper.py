from . import pyglet
from .pyglet import gl
import ctypes

def compile_shader(shader_type, shader_source):
    '''
    Compile a shader and print error messages.
    '''
    shader_name = gl.glCreateShader(shader_type)
    src_buffer = ctypes.create_string_buffer(shader_source)
    buf_pointer = ctypes.cast(ctypes.pointer(ctypes.pointer(src_buffer)), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
    length = ctypes.c_int(len(shader_source) + 1)
    gl.glShaderSource(shader_name, 1, buf_pointer, ctypes.byref(length))
    gl.glCompileShader(shader_name)

    # test if compilation is succesful and print status messages
    success = gl.GLint(0)
    gl.glGetShaderiv(shader_name, gl.GL_COMPILE_STATUS, ctypes.byref(success))

    length = gl.GLint(0)
    gl.glGetShaderiv(shader_name, gl.GL_INFO_LOG_LENGTH, ctypes.byref(length))
    log_buffer = ctypes.create_string_buffer(length.value)
    gl.glGetShaderInfoLog(shader_name, length, None, log_buffer)

    for line in log_buffer.value[:length.value].decode('ascii').splitlines():
        print('GLSL: ' + line)

    assert success, 'Compiling of the shader failed.'

    return shader_name


def link_program(program):
    ''' link a glsl program and print error messages.'''
    gl.glLinkProgram(program)

    length = gl.GLint(0)
    gl.glGetProgramiv(program, gl.GL_INFO_LOG_LENGTH, ctypes.byref(length))
    log_buffer = ctypes.create_string_buffer(length.value)
    gl.glGetProgramInfoLog(program, length, None, log_buffer)

    for line in log_buffer.value[:length.value].decode('ascii').splitlines():
        print('GLSL: ' + line)
        
