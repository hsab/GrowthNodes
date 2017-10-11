import bpy
import bgl

def createShader(shader_type, shader_source):
    shader = bgl.glCreateShader(shader_type)
    bgl.glShaderSource(shader, shader_source)
    bgl.glCompileShader(shader)
    success = bgl.Buffer(bgl.GL_INT, [1])
    bgl.glGetShaderiv(shader, bgl.GL_COMPILE_STATUS, success)
    if (success[0] == bgl.GL_TRUE):
        print("shader compiled")
        return shader
    bgl.glGetShaderiv(shader, bgl.GL_INFO_LOG_LENGTH, success);
    success[0] = success[0] + 1
    log = bgl.Buffer(bgl.GL_BYTE, [success[0]])
    start = bgl.Buffer(bgl.GL_INT, [1])
    start[0] =0
    bgl.glGetShaderInfoLog(shader, success[0]+1,start, log)
    py_log = log[:]
    py_log_str = ""
    for c in py_log:
        py_log_str += str(chr(c))
    print(str(py_log_str))
    bgl.glDeleteShader(shader)
    
def createProgram(vertexShader, fragmentShader):
    program = bgl.glCreateProgram()
    bgl.glAttachShader(program, vertexShader)
    bgl.glAttachShader(program, fragmentShader)
    bgl.glLinkProgram(program)
    success = bgl.Buffer(bgl.GL_INT, [1])
    bgl.glGetProgramiv(program, bgl.GL_LINK_STATUS, success)
    #var success = gl.getProgramParameter(program, gl.LINK_STATUS);
    if (success[0] == bgl.GL_TRUE):
        print("shader link success")
        return program

    print("shader program linking failed")
    
    bgl.glGetProgramiv(program, bgl.GL_INFO_LOG_LENGTH, success)
    start = bgl.Buffer(bgl.GL_INT, [1])
    start[0] =0
    log = bgl.Buffer(bgl.GL_BYTE, [success[0]])
    bgl.glGetProgramInfoLog(program, success[0], start, log)
    py_log = log[:]
    py_log_str = ""
    for c in py_log:
        py_log_str += str(chr(c))
    print(str(py_log_str))
    bgl.glDeleteProgram(program)