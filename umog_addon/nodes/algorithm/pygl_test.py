'''
Based on code from
Author: leovt (Leonhard Vogt)
License: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007
Example code for using glsl and vertex buffer objects with pyglet
'''
from ..output_node import UMOGOutputNode
from ... events import pyglet_helper

import pyglet
from pyglet import gl
import ctypes

import threading
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()


class PyGLNode(UMOGOutputNode):
    bl_idname = "PyGLNode"
    bl_label = "3d Reaction Diffusion Node"

    feed = bpy.props.FloatProperty(default=0.014, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    kill = bpy.props.FloatProperty(default=0.046, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    Da = bpy.props.FloatProperty(default=0.2, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    Db = bpy.props.FloatProperty(default=0.09, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    dt = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    steps = bpy.props.IntProperty(default=2, min=1, step=500)
    channels = bpy.props.EnumProperty(items=
        (('0', 'R', 'Just do the reaction on one channel'),
         ('1', 'RGB', 'Do the reaction on all color channels'),
        ),
        name="channels")

    def init(self, context):
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "feed", "Feed")
        layout.prop(self, "kill", "Kill")
        layout.prop(self, "Da", "Da")
        layout.prop(self, "Db", "Db")
        layout.prop(self, "dt", "dt")
        layout.prop(self, "steps", "steps")
        layout.prop(self, "channels", "channels")
        
    def update(self):
        pass


        

    def execute(self, refholder):
        try:
            #start a new thread to avoid poluting blender's opengl context
            t = threading.Thread(target=OffScreenRender, args=(self.steps,))
            t.start()
            t.join()
            print("OpenglRender done")
        except:
            print("thread start failed")


def OffScreenRender(steps):
    class ControledRender(pyglet.window.Window):
        vertex_source = b"""
        #version 330
        attribute vec2 a_position;
        varying vec2 vTexCoord;
        void main() {
        vTexCoord = 0.5*(a_position.xy + vec2(1,1));
        gl_Position = vec4(a_position, 0.0, 1.0);
        }
        """
        
        fragment_source = b"""
        #version 330
        out vec4 color;
        varying vec2 vTexCoord;
        uniform sampler2D myTexture;
        
        uniform float step;

        uniform float du;
        uniform float dv;

        float distance = 1.5;
        uniform float timestep;

        uniform float k;
        uniform float f;
        
        void main() {
        
        float oldU = texture2D(myTexture, vTexCoord).r;				
        float oldV = texture2D(myTexture, vTexCoord).g;	

        // [rad] Compute approximation of Laplacian for both V and U.
        float otherU = -4.0 * oldU;
        float otherV = -4.0 * oldV;

        otherU += texture2D(myTexture, vTexCoord + vec2(-step, 0)).r;
        otherU += texture2D(myTexture, vTexCoord + vec2(step, 0)).r;
        otherU += texture2D(myTexture, vTexCoord + vec2(0, -step)).r;
        otherU += texture2D(myTexture, vTexCoord + vec2(0, step)).r;

        otherV += texture2D(myTexture, vTexCoord + vec2(-step, 0)).g;
        otherV += texture2D(myTexture, vTexCoord + vec2(step, 0)).g;
        otherV += texture2D(myTexture, vTexCoord + vec2(0, -step)).g;
        otherV += texture2D(myTexture, vTexCoord + vec2(0, step)).g;

        float distance_squared = distance * distance;
        
        // [rad] Compute greyscott equations.
        float newU = du * otherU / distance_squared - oldU * oldV * oldV + f * (1.0 - oldU);
        float newV = dv * otherV / distance_squared + oldU * oldV * oldV - (f + k ) * oldV;

        float scaledU = oldU + newU * timestep;
        float scaledV = oldV + newV * timestep;

        color = vec4(clamp(scaledU, 0.0, 1.0), clamp(scaledV, 0.0, 1.0), clamp(newU, 0.0, 1.0), 1.0);
        
        //color =vec4(0.1, 0.1,0,0) +texture2D(myTexture, vTexCoord);
        }
        """
        
        def __init__(self, frames):
            #consider bumping opengl version if apple supports it
            #amdgpu-mesa currently supports up to 4.5
            super(ControledRender, self).__init__(512, 512, fullscreen = False, config=gl.Config(major_version=4, minor_version=1), visible=False)
            print(self.context.get_info().get_version())
            
            self.frames = frames
            self.vertex_buffer = gl.GLuint(0)
            self.vao = gl.GLuint(0)
            self.framebuffer = gl.GLuint(0)
            self.temp_tex = gl.GLuint(0)
            self.dim = 512
            
            gl.glGenFramebuffers(1, ctypes.byref(self.framebuffer))
            gl.glGenTextures(1, ctypes.byref(self.temp_tex))
            
            gl.glGenFramebuffers(1, ctypes.byref(self.framebuffer))
            gl.glGenTextures(1, ctypes.byref(self.temp_tex))

            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)

            # Set up the texture as the target for color output
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.temp_tex)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.dim, self.dim, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, 0)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self.temp_tex, 0)

            self.draw_buffers = (gl.GLenum * 1)(gl.GL_COLOR_ATTACHMENT0)
            gl.glDrawBuffers(1, self.draw_buffers)

            assert gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE
            
            self.program = gl.glCreateProgram()
            gl.glAttachShader(self.program, pyglet_helper.compile_shader(gl.GL_VERTEX_SHADER, self.vertex_source))
            gl.glAttachShader(self.program, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source))
            pyglet_helper.link_program(self.program)
            
            
            data = [-1.0, -1.0,
                    1.0, -1.0,
                    1.0, 1.0,
                     
                    -1.0, -1.0,
                    1.0, 1.0,
                    -1.0, 1.0]
             
             
            dataGl = (gl.GLfloat * len(data))(*data)
            
            gl.glGenBuffers(1, ctypes.byref(self.vertex_buffer))
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
            gl.glBufferData(gl.GL_ARRAY_BUFFER, len(dataGl)*4, dataGl, gl.GL_STATIC_DRAW)
            
            gl.glGenVertexArrays(1, ctypes.byref(self.vao))
            gl.glBindVertexArray(self.vao)
            
            pos_pos = gl.glGetAttribLocation(self.program, ctypes.create_string_buffer(b"a_position"))
            assert(pos_pos >= 0)
            gl.glEnableVertexAttribArray(pos_pos)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
            gl.glVertexAttribPointer(pos_pos, 2, gl.GL_FLOAT, False, 0, 0)
            
        def cleanUP(self):
            pass
        
        def on_draw(self):
            self.render()

        def on_close(self):
            self.alive = 0

        def render(self):
            self.clear()
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer);
            gl.glViewport(0,0,self.dim,self.dim)
            
            #gl.glClearColor(0, 0, 0, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
            
            self.flip() # This updates the screen, very much important.
            
        
        def run(self):
            for i in range(self.frames):
                self.render()

                # -----------> This is key <----------
                # This is what replaces pyglet.app.run()
                # but is required for the GUI to not freeze.
                # Basically it flushes the event pool that otherwise
                # fill up and block the buffers and hangs stuff.
                #event = self.dispatch_events()
                
    cr = ControledRender(steps)
    cr.run()
    cr.close()
    cr.cleanUP()
    #print(dir(cr))
    del cr
    cr = None
    
