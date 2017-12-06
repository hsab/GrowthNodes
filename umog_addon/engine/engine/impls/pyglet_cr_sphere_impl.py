import numpy as np
import sys
import os
import importlib
import traceback

def trace(frame, event, arg):
    print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
    return trace


def Dummy(steps, in_buffer, out_buffer):
    print("dummy")
    return True

def OffScreenRender( args, test=False):
    try:
        if test:
            import pyglet
            from pyglet import gl
            import ctypes
            import pyglet_helper
            import numpy as np
        else:
            from .... packages import osr_runner
            osr_runner.path_changer()
            from .... packages import pyglet_helper            
            from .... packages import pyglet
            from ....packages.pyglet import gl
            import ctypes
            import numpy as np
    except:
        print("imports failed")
        traceback.print_exc()
        return
            
    print("start of osr, for generation")
    class ControledRender(pyglet.window.Window):
        vertex_source = b"""
        #version 330
        attribute vec2 a_position;
        varying vec3 vTexCoord;
        uniform int slice;
        uniform float step;
        void main() {
        vTexCoord = vec3(0.5*(a_position.xy + vec2(1,1)), step * slice);
        gl_Position = vec4(a_position, 0.0, 1.0);
        }
        """
        
        fragment_source_a = b"""
        #version 330
        out float color;
        varying vec3 vTexCoord;

        uniform float radius;
        uniform vec3 center;
        
        
        void main() {
        
        if(distance(vTexCoord, center) < radius)
        {
            color = 1.0;
        }
        else
        {
            color = 0.0;
        }
        }
        """
        
        fragment_source_cylinder = b"""
        #version 330
        out float color;
        varying vec3 vTexCoord;

        uniform float radius;
        uniform float height;
        
        
        void main() {
        
        if((distance(vTexCoord.xy, vec2(0.5, 0.5)) < radius) && (vTexCoord.z < height))
        {
            color = 1.0;
        }
        else
        {
            color = 0.0;
        }
        }
        """
        
        def setupShaders(self):
            self.programA = gl.glCreateProgram()
            gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_VERTEX_SHADER, self.vertex_source))
            if args["shape"] == "sphere":
                gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_a))
            elif args["shape"] == "cylinder":
                gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_cylinder))
            pyglet_helper.link_program(self.programA)
            
        def setupFBOandTextures(self):
            self.framebufferA0 = (gl.GLuint * args["resolution"])()
            
            self.A0_tex = gl.GLuint(0)
            
            self.draw_buffersA0 = (gl.GLenum * args["resolution"])(gl.GL_COLOR_ATTACHMENT0)
            
            gl.glGenFramebuffers(args["resolution"], self.framebufferA0)
            
            gl.glGenTextures(1, ctypes.byref(self.A0_tex))
            
            #create textures
            #A
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A0_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, args["resolution"], args["resolution"], args["resolution"], 0, gl.GL_RED, gl.GL_FLOAT, 0)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            
            #A
            for i in range(args["resolution"]):
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA0[i])
                gl.glFramebufferTexture3D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_3D, self.A0_tex, 0, i)
                assert(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE)
                
                
            #gl.glDrawBuffers(1, self.draw_buffersA0[i])
            #gl.glDrawBuffers(1, self.draw_buffersA0)
        
        def __init__(self):
            #consider bumping opengl version if apple supports it
            #amdgpu-mesa currently supports up to 4.5
            super(ControledRender, self).__init__(512, 512, fullscreen = False, config=gl.Config(major_version=4, minor_version=1), visible=False)
            print(self.context.get_info().get_version())
            
            self.vertex_buffer = gl.GLuint(0)
            self.vao = gl.GLuint(0)
            #self.prev_program = (gl.GLint * 1)()
            
            
            self.setupFBOandTextures()
            
            self.setupShaders()
            
            
            
            
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
            gl.glUseProgram(self.programA)
            self.pos_posA = gl.glGetAttribLocation(self.programA, ctypes.create_string_buffer(b"a_position"))
            assert(self.pos_posA >= 0)
            gl.glEnableVertexAttribArray(self.pos_posA)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
            gl.glVertexAttribPointer(self.pos_posA, 2, gl.GL_FLOAT, False, 0, 0)
            
            if args["shape"] == "sphere":
                self.radius_pos = gl.glGetUniformLocation(self.programA, b"radius")
                self.center_pos = gl.glGetUniformLocation(self.programA, b"center")
                self.checkUniformLocation(self.radius_pos)
                self.checkUniformLocation(self.center_pos)
                gl.glUniform1f(self.radius_pos, args["radius"])
                gl.glUniform3f(self.center_pos, args["center"][0], args["center"][1], args["center"][2])
            elif args["shape"] == "cylinder":
                self.radius_pos = gl.glGetUniformLocation(self.programA, b"radius")
                self.height_pos = gl.glGetUniformLocation(self.programA, b"height")
                self.checkUniformLocation(self.radius_pos)
                self.checkUniformLocation(self.height_pos)
                gl.glUniform1f(self.radius_pos, args["radius"])
                gl.glUniform1f(self.height_pos, args["height"])
                
            self.slice_pos  = gl.glGetUniformLocation(self.programA, b"slice")
            self.step_pos  = gl.glGetUniformLocation(self.programA, b"step")
            
            self.checkUniformLocation(self.slice_pos)
            
            gl.glUniform1f(self.step_pos, 1/args["resolution"])
            #may need changed for nonsquare textures
            
            gl.glViewport(0,0,args["resolution"],args["resolution"])
            #self.clear()
            
        def cleanUP(self):
            a = (gl.GLfloat * (args["resolution"] ** 3))()
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A0_tex)
            gl.glGetTexImage(gl.GL_TEXTURE_3D, 0, gl.GL_RED, gl.GL_FLOAT, a)

            
            
            #self.flip() # This updates the screen, very much important.
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0);
            
            bufA = np.frombuffer(a, dtype=np.float32)
            
            bufA = bufA.reshape((args["resolution"], args["resolution"], args["resolution"]))
            
            #consider casting to float64
            args["Aout"] = bufA
        
        def checkUniformLocation(self,val):
            assert(val != gl.GL_INVALID_VALUE)
            assert(val != gl.GL_INVALID_OPERATION)
        
        def on_draw(self):
            self.render()

        def on_close(self):
            self.alive = 0

        def render(self):
            gl.glUseProgram(self.programA)
            for i in range(args["resolution"]):
                gl.glUniform1i(self.slice_pos, i)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA0[i])
                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)

            
        
        def run(self):
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze.
            # Basically it flushes the event pool that otherwise
            # fill up and block the buffers and hangs stuff.
            event = self.dispatch_events()
    cr = ControledRender()       
    osr_runner.runner(cr)
    #del cr
    #cr = None
    print("end of osr")
    
if __name__ == "__main__":
    #sys.settrace(trace)
    import time
    start = time.time()
    
    temps = {}
    temps["shape"] = "sphere"
    #temps["radius"] = 0.2
    ##just needs to be indexable not necissarily a tuple
    temps["center"] = (0.5,0.5, 0.5)
    #OffScreenRender(temps, test=True)
    
    #temps["shape"] = "cylinder"
    temps["radius"] = 0.3
    temps["height"] = 1.0
    temps["resolution"] = 256
    OffScreenRender(temps, test=True)
    print(temps["Aout"])
    end = time.time()
    print("the 3d reaction diffusion took " + str(end-start))
    
