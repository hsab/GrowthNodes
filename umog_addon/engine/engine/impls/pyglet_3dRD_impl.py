import numpy as np
import sys
import os

def trace(frame, event, arg):
    print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
    return trace


def Dummy(steps, in_buffer, out_buffer):
    print("dummy")
    return True

def OffScreenRender(steps, args, test=False):
    cpath = os.path.dirname(os.path.realpath(__file__))
    print(cpath)
    cpath = os.path.split(cpath)[0]
    cpath = os.path.split(cpath)[0]
    cpath = os.path.join(cpath, "packages")
    print(cpath)
    if cpath not in sys.path:
        sys.path.append(cpath)
    try:
        if test:
            import pyglet
            from pyglet import gl
            import ctypes
            import pyglet_helper
            import numpy as np
        else:
            from ... packages import pyglet_helper
            from ... packages import osr_runner
            from ... packages import pyglet
            from ...packages.pyglet import gl
            import ctypes
            import numpy as np
    except:
        print("imports failed")
        return
            
    print("start of osr, for " + str(steps))
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
        out vec4 color;
        varying vec3 vTexCoord;
        uniform sampler3D A;
        uniform sampler3D B;
        
        uniform float step;

        uniform float dA;
        uniform float dB;

        float distance = 1.5;
        uniform float timestep;

        uniform float k;
        uniform float f;
        
        
        void main() {
        
        vec4 oldA = texture3D(A, vTexCoord);				
        vec4 oldB = texture3D(B, vTexCoord);	

        // [rad] Compute approximation of Laplacian for both V and U.
        vec4 otherA = -6.0 * oldA;
        vec4 otherB = -6.0 * oldB;

        otherA += texture3D(A, vTexCoord + vec3(-step, 0,0));
        otherA += texture3D(A, vTexCoord + vec3(step, 0,0));
        otherA += texture3D(A, vTexCoord + vec3(0, -step,0));
        otherA += texture3D(A, vTexCoord + vec3(0, step,0));
        otherA += texture3D(A, vTexCoord + vec3(0, 0, -step));
        otherA += texture3D(A, vTexCoord + vec3(0, 0,  step));

        otherB += texture3D(B, vTexCoord + vec3(-step, 0,0));
        otherB += texture3D(B, vTexCoord + vec3(step, 0,0));
        otherB += texture3D(B, vTexCoord + vec3(0, -step,0));
        otherB += texture3D(B, vTexCoord + vec3(0, step,0));
        otherB += texture3D(B, vTexCoord + vec3(0, 0, -step));
        otherB += texture3D(B, vTexCoord + vec3(0, 0,  step));

        float distance_squared = distance * distance * distance;
        
        // [rad] Compute greyscott equations.
        vec4 newA = dA * otherA / distance_squared - oldA * oldB * oldB + f * (1.0 - oldA);
        vec4 newB = dB * otherB / distance_squared + oldA * oldB * oldB - (f + k ) * oldB;

        vec4 scaledA = oldA + newA * timestep;
        //vec4 scaledB = oldB + newB * timestep;

        color = vec4(clamp(scaledA, vec4(0,0,0,0), vec4(1,1,1,1)).rgb, 1.0);
        
        //color =vec4(0.1, 0.1,0,0) +texture2D(myTexture, vTexCoord);
        //color = vec4(0.5, 0.75, 1.0, 1.0);
        }
        """
        
        fragment_source_b = b"""
        #version 330
        out vec4 color;
        varying vec3 vTexCoord;
        uniform sampler3D A;
        uniform sampler3D B;
        
        uniform float step;

        uniform float dA;
        uniform float dB;

        float distance = 1.5;
        uniform float timestep;

        uniform float k;
        uniform float f;
        uniform int slice;
        
        void main() {
        
        vec4 oldA = texture3D(A, vTexCoord);				
        vec4 oldB = texture3D(B, vTexCoord);	

        // [rad] Compute approximation of Laplacian for both V and U.
        vec4 otherA = -6.0 * oldA;
        vec4 otherB = -6.0 * oldB;

        otherA += texture3D(A, vTexCoord + vec3(-step, 0,0));
        otherA += texture3D(A, vTexCoord + vec3(step, 0,0));
        otherA += texture3D(A, vTexCoord + vec3(0, -step,0));
        otherA += texture3D(A, vTexCoord + vec3(0, step,0));
        otherA += texture3D(A, vTexCoord + vec3(0, 0, -step));
        otherA += texture3D(A, vTexCoord + vec3(0, 0,  step));

        otherB += texture3D(B, vTexCoord + vec3(-step, 0,0));
        otherB += texture3D(B, vTexCoord + vec3(step, 0,0));
        otherB += texture3D(B, vTexCoord + vec3(0, -step,0));
        otherB += texture3D(B, vTexCoord + vec3(0, step,0));
        otherB += texture3D(B, vTexCoord + vec3(0, 0, -step));
        otherB += texture3D(B, vTexCoord + vec3(0, 0,  step));

        float distance_squared = distance * distance * distance;
        
        // [rad] Compute greyscott equations.
        vec4 newA = dA * otherA / distance_squared - oldA * oldB * oldB + f * (1.0 - oldA);
        vec4 newB = dB * otherB / distance_squared + oldA * oldB * oldB - (f + k ) * oldB;

        vec4 scaledA = oldA + newA * timestep;
        vec4 scaledB = oldB + newB * timestep;

        color = vec4(clamp(scaledB, vec4(0,0,0,0), vec4(1,1,1,1)).rgb, 1.0);
        
        //color =vec4(0.1, 0.1,0,0) +texture2D(myTexture, vTexCoord);
        //color = vec4(0.5, 0.75, 1.0, 1.0);
        }
        """
        
        def setupShaders(self):
            self.programA = gl.glCreateProgram()
            gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_VERTEX_SHADER, self.vertex_source))
            gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_a))
            pyglet_helper.link_program(self.programA)
            
            self.programB = gl.glCreateProgram()
            gl.glAttachShader(self.programB, pyglet_helper.compile_shader(gl.GL_VERTEX_SHADER, self.vertex_source))
            gl.glAttachShader(self.programB, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_b))
            pyglet_helper.link_program(self.programB)
            
        def setupFBOandTextures(self):
            self.framebufferA0 = (gl.GLuint * self.dimz)()
            self.framebufferA1 = (gl.GLuint * self.dimz)()
            self.framebufferB0 = (gl.GLuint * self.dimz)()
            self.framebufferB1 = (gl.GLuint * self.dimz)()
            
            self.A0_tex = gl.GLuint(0)
            self.A1_tex = gl.GLuint(0)
            self.B0_tex = gl.GLuint(0)
            self.B1_tex = gl.GLuint(0)
            
            self.draw_buffersA0 = (gl.GLenum * self.dimz)(gl.GL_COLOR_ATTACHMENT0)
            self.draw_buffersA1 = (gl.GLenum * self.dimz)(gl.GL_COLOR_ATTACHMENT0)
            self.draw_buffersB0 = (gl.GLenum * self.dimz)(gl.GL_COLOR_ATTACHMENT0)
            self.draw_buffersB1 = (gl.GLenum * self.dimz)(gl.GL_COLOR_ATTACHMENT0)
            
            #gl.glGenFramebuffers(self.dimz, ctypes.byref(self.framebufferA0))
            #gl.glGenFramebuffers(self.dimz, ctypes.byref(self.framebufferA1))
            #gl.glGenFramebuffers(self.dimz, ctypes.byref(self.framebufferB0))
            #gl.glGenFramebuffers(self.dimz, ctypes.byref(self.framebufferB1))
            gl.glGenFramebuffers(self.dimz, self.framebufferA0)
            gl.glGenFramebuffers(self.dimz, self.framebufferA1)
            gl.glGenFramebuffers(self.dimz, self.framebufferB0)
            gl.glGenFramebuffers(self.dimz, self.framebufferB1)
            
            gl.glGenTextures(1, ctypes.byref(self.A0_tex))
            gl.glGenTextures(1, ctypes.byref(self.A1_tex))
            gl.glGenTextures(1, ctypes.byref(self.B0_tex))
            gl.glGenTextures(1, ctypes.byref(self.B1_tex))
            
            
            #create textures
            #A
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A0_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, self.dimx, self.dimy, self.dimz, 0, gl.GL_RED, gl.GL_FLOAT, self.Ap)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            gl.glActiveTexture(gl.GL_TEXTURE1)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A1_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, self.dimx, self.dimy, self.dimz, 0, gl.GL_RED, gl.GL_FLOAT, self.Ap)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            #B
            gl.glActiveTexture(gl.GL_TEXTURE2)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.B0_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, self.dimx, self.dimy, self.dimz, 0, gl.GL_RED, gl.GL_FLOAT, self.Bp)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            gl.glActiveTexture(gl.GL_TEXTURE3)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.B1_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, self.dimx, self.dimy, self.dimz, 0, gl.GL_RED, gl.GL_FLOAT, self.Bp)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            #A
            for i in range(self.dimz):
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA0[i])
                gl.glFramebufferTexture3D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_3D, self.A0_tex, 0, i)
                assert(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE)
                
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA1[i])
                gl.glFramebufferTexture3D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_3D, self.A1_tex, 0, i)
                assert(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE)
                
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferB0[i])
                gl.glFramebufferTexture3D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_3D, self.B0_tex, 0, i)
                assert(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE)
                
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferB1[i])
                gl.glFramebufferTexture3D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_3D, self.B1_tex, 0, i)
                assert(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE)
                
            #gl.glDrawBuffers(1, self.draw_buffersA0[i])
            #gl.glDrawBuffers(1, self.draw_buffersA0)
        
        def __init__(self, frames):
            #consider bumping opengl version if apple supports it
            #amdgpu-mesa currently supports up to 4.5
            super(ControledRender, self).__init__(512, 512, fullscreen = False, config=gl.Config(major_version=4, minor_version=1), visible=False)
            print(self.context.get_info().get_version())
            
            self.frames = frames
            self.vertex_buffer = gl.GLuint(0)
            self.vao = gl.GLuint(0)
            #self.prev_program = (gl.GLint * 1)()
            
            
            self.dimx = args["A"].shape[0]
            self.dimy = args["A"].shape[1]
            self.dimz = args["A"].shape[2]
            
            
            
            A = args["A"].astype(np.float32)
            #print("A shape " + str(A.shape))
            #print(str(A.dtype))
            #print(A)
            
            B = args["B"].astype(np.float32)
            
            #self.dp = self.tdata.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
            self.Ap = A.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
            self.Bp = B.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
            
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
            
            self.tex_pos_A_A = gl.glGetUniformLocation(self.programA, b"A")
            self.tex_pos_A_B = gl.glGetUniformLocation(self.programA, b"B")
            self.feed_pos_A  = gl.glGetUniformLocation(self.programA, b"f")
            self.kill_pos_A  = gl.glGetUniformLocation(self.programA, b"k")
            self.dA_pos_A    = gl.glGetUniformLocation(self.programA, b"dA")
            self.dB_pos_A    = gl.glGetUniformLocation(self.programA, b"dB")
            self.dt_pos_A    = gl.glGetUniformLocation(self.programA, b"timestep")
            self.step_pos_A  = gl.glGetUniformLocation(self.programA, b"step")
            self.slice_pos_A  = gl.glGetUniformLocation(self.programA, b"slice")
            self.checkUniformLocation(self.tex_pos_A_A)
            self.checkUniformLocation(self.tex_pos_A_B)
            self.checkUniformLocation(self.feed_pos_A)
            self.checkUniformLocation(self.kill_pos_A)
            self.checkUniformLocation(self.dA_pos_A)
            self.checkUniformLocation(self.dB_pos_A)
            self.checkUniformLocation(self.step_pos_A)
            self.checkUniformLocation(self.slice_pos_A)
            gl.glUniform1f(self.feed_pos_A, args["feed"])
            gl.glUniform1f(self.kill_pos_A, args["kill"])
            gl.glUniform1f(self.dA_pos_A, args["dA"])
            gl.glUniform1f(self.dB_pos_A, args["dB"])
            gl.glUniform1f(self.dt_pos_A, args["dt"])
            #may need changed for nonsquare textures
            gl.glUniform1f(self.step_pos_A, 1/self.dimx)
            
            
            gl.glUseProgram(self.programB)
            self.pos_posB = gl.glGetAttribLocation(self.programB, ctypes.create_string_buffer(b"a_position"))
            assert(self.pos_posB >= 0)
            gl.glEnableVertexAttribArray(self.pos_posB)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
            gl.glVertexAttribPointer(self.pos_posB, 2, gl.GL_FLOAT, False, 0, 0)
            
            self.tex_pos_B_A = gl.glGetUniformLocation(self.programB, b"A")
            self.tex_pos_B_B = gl.glGetUniformLocation(self.programB, b"B")
            self.feed_pos_B  = gl.glGetUniformLocation(self.programB, b"f")
            self.kill_pos_B  = gl.glGetUniformLocation(self.programB, b"k")
            self.dA_pos_B    = gl.glGetUniformLocation(self.programB, b"dA")
            self.dB_pos_B    = gl.glGetUniformLocation(self.programB, b"dB")
            self.dt_pos_B    = gl.glGetUniformLocation(self.programB, b"timestep")
            self.step_pos_B  = gl.glGetUniformLocation(self.programB, b"step")
            self.slice_pos_B  = gl.glGetUniformLocation(self.programB, b"slice")
            self.checkUniformLocation(self.tex_pos_B_A)
            self.checkUniformLocation(self.tex_pos_B_B)
            self.checkUniformLocation(self.feed_pos_B)
            self.checkUniformLocation(self.kill_pos_B)
            self.checkUniformLocation(self.dA_pos_B)
            self.checkUniformLocation(self.dB_pos_B)
            self.checkUniformLocation(self.step_pos_B)
            self.checkUniformLocation(self.slice_pos_B)
            gl.glUniform1f(self.feed_pos_B, args["feed"])
            gl.glUniform1f(self.kill_pos_B, args["kill"])
            gl.glUniform1f(self.dA_pos_B, args["dA"])
            gl.glUniform1f(self.dB_pos_B, args["dB"])
            gl.glUniform1f(self.dt_pos_B, args["dt"])
            #may need changed for nonsquare textures
            gl.glUniform1f(self.step_pos_B, 1/self.dimx)
            
            gl.glViewport(0,0,self.dimx,self.dimy)
            #self.clear()
            
        def cleanUP(self):
            a = (gl.GLint * (self.dimx*self.dimy*self.dimz))()
            b = (gl.GLint * (self.dimx*self.dimy*self.dimz))()
            #need a new way to read out pixels
            #gl.glReadPixels(0, 0, self.dimx, self.dimy , gl.GL_RGBA, gl.GL_FLOAT, b)
            #gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA1);
            #gl.glReadPixels(0, 0, self.dimx, self.dimy , gl.GL_RGBA, gl.GL_FLOAT, a)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A1_tex)
            gl.glGetTexImage(gl.GL_TEXTURE_3D, 0, gl.GL_RED, gl.GL_FLOAT, a)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.B1_tex)
            gl.glGetTexImage(gl.GL_TEXTURE_3D, 0, gl.GL_RED, gl.GL_FLOAT, b)
            
            
            #self.flip() # This updates the screen, very much important.
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0);
            
            bufA = np.frombuffer(a, dtype=np.float32)
            bufB = np.frombuffer(b, dtype=np.float32)
            
            bufA = bufA.reshape(args["A"].shape)
            bufB = bufB.reshape(args["B"].shape)
            
            #consider casting to float64
            args["Bout"] = bufB
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
            gl.glUniform1i(self.tex_pos_A_A, 1)
            gl.glUniform1i(self.tex_pos_A_B, 3)
            for i in range(self.dimz):
                gl.glUniform1i(self.slice_pos_A, i)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA0[i])
                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
            
            gl.glUseProgram(self.programB)
            gl.glUniform1i(self.tex_pos_B_A, 1)
            gl.glUniform1i(self.tex_pos_B_B, 3)
            for i in range(self.dimz):
                gl.glUniform1i(self.slice_pos_B, i)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferB0[i])
                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
            
            gl.glUseProgram(self.programA)
            gl.glUniform1i(self.tex_pos_A_A, 0)
            gl.glUniform1i(self.tex_pos_A_B, 2)
            for i in range(self.dimz):
                gl.glUniform1i(self.slice_pos_A, i)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA1[i])
                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
            
            gl.glUseProgram(self.programB)
            gl.glUniform1i(self.tex_pos_B_A, 0)
            gl.glUniform1i(self.tex_pos_B_B, 2)
            for i in range(self.dimz):
                gl.glUniform1i(self.slice_pos_B, i)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferB1[i])
                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)

            
        
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
    osr_runner.runner(cr)
    #del cr
    #cr = None
    print("end of osr")
    
if __name__ == "__main__":
    #sys.settrace(trace)
    import time
    start = time.time()
    
    temps = {}
    temps["A"] = np.random.rand(256, 256, 256)
    temps["B"] = np.random.rand(256, 256, 256)
    temps["feed"] = 0.05
    temps["kill"] = 0.05
    temps["dA"] = 1.0
    temps["dB"] = 0.5
    temps["dt"] = 0.2
    OffScreenRender(6000,temps, test=True)
    
    end = time.time()
    print("the 3d reaction diffusion took " + str(end-start))
    
