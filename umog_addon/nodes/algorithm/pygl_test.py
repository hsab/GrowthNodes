'''
Based on code from
Author: leovt (Leonhard Vogt)
License: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007
Example code for using glsl and vertex buffer objects with pyglet
'''
from ..output_node import UMOGOutputNode
from ... events import bgl_helper

import pyglet
from pyglet import gl
import ctypes

import threading
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()
from ...events import events

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


#class ControledRender(pyglet.window.Window):
    #def __init__(self, frames):
        #super(main, self).__init__(512, 512, fullscreen = False)
        #self.frames = frames
        
    #def on_draw(self):
        #self.render()

    #def on_close(self):
        #self.alive = 0

    #def render(self):
        #self.clear()

        #self.flip() # This updates the screen, very much important.
        
    
    #def run(self):
        #for i in range(self.frames):
            #self.render()

            ## -----------> This is key <----------
            ## This is what replaces pyglet.app.run()
            ## but is required for the GUI to not freeze.
            ## Basically it flushes the event pool that otherwise
            ## fill up and block the buffers and hangs stuff.
            #event = self.dispatch_events()

class PyGLNode(UMOGOutputNode):
    bl_idname = "PyGLNode"
    bl_label = "Reaction Diffusion Node"

    steps = bpy.props.IntProperty( default=2)

    def init(self, context):
        super().init(context)

    def draw_buttons(self, context, layout):
        pass
        
    def update(self):
        pass


        

    def execute(self, refholder):
        try:
            #threading.start_new_thread( self.OffScreenRender, (self) )
            t = threading.Thread(target=OffScreenRender, args=(self.steps,))
            t.start()
            t.join()
        except:
            print("thread start failed")
        
        
                    
        tr = bpy.context.scene.TextureResolution
        print("begining execution " + str(tr))
        #render_vertexbuffer = gl.GLuint(0)
        #render_vao = gl.GLuint(0)
        #render_program = 0
        
        #copy_vertexbuffer = gl.GLuint(0)
        #copy_vao = gl.GLuint(0)
        #copy_program = 0

        #framebuffer = gl.GLuint(0)
        #rendered_texture = gl.GLuint(0)
        
        #window = pyglet.window.Window()
        
        
        #print('OpenGL Version {}'.format(window.context.get_info().get_version()))
        #cr = ControledRender(self.steps)
        #cr.run()
        #cr = None


def OffScreenRender(steps):
    class ControledRender(pyglet.window.Window):
        def __init__(self, frames):
            super(ControledRender, self).__init__(512, 512, fullscreen = False, visible=False)
            self.frames = frames
            
        def on_draw(self):
            self.render()

        def on_close(self):
            self.alive = 0

        def render(self):
            self.clear()

            self.flip() # This updates the screen, very much important.
            
        
        def run(self):
            for i in range(self.frames):
                self.render()

                # -----------> This is key <----------
                # This is what replaces pyglet.app.run()
                # but is required for the GUI to not freeze.
                # Basically it flushes the event pool that otherwise
                # fill up and block the buffers and hangs stuff.
                event = self.dispatch_events()
                
    cr = ControledRender(steps)
    cr.run()
    cr.close()
    #print(dir(cr))
    cr = None

def postBake(self, refholder):
        #TODO clean up the shader stuff
        pass
    
