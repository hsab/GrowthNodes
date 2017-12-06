import numpy as np
import sys

def trace(frame, event, arg):
    print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
    return trace


def Dummy(steps, in_buffer, out_buffer):
    print("dummy")
    return True

def OffScreenRender(args, test=False):
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
            from ....packages.pyglet import gl
            import ctypes
            import numpy as np
    except:
        print("imports failed")
        return
            
    #print("start of osr, for " + str(steps))
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
        uniform sampler3D A;
        uniform sampler3D B;
        
        uniform float threshold;
        
        
        void main() {
        
        float oldA = texture3D(A, vTexCoord).r;				
        float oldB = texture3D(B, vTexCoord).r;	
        if(abs(oldA -oldB) < threshold)
        {
            color = 1.0;
        }
        else
        {
            color = 0.0;
        }
        

        }
        """
        
        fragment_source_intersection = b"""
        #version 330
        out float color;
        varying vec3 vTexCoord;
        uniform sampler3D A;
        uniform sampler3D B;
        
        uniform float threshold;
        
        
        void main() {
        
        float oldA = texture3D(A, vTexCoord).r;				
        float oldB = texture3D(B, vTexCoord).r;	
        if((oldA > threshold) && (oldB > threshold))
        {
            color = mix(oldA,oldB, 0.5);
        }
        else
        {
            color = 0.0;
        }
        

        }
        """
        
        fragment_source_union = b"""
        #version 330
        out float color;
        varying vec3 vTexCoord;
        uniform sampler3D A;
        uniform sampler3D B;
        
        uniform float threshold;
        
        
        void main() {
        
        float oldA = texture3D(A, vTexCoord).r;				
        float oldB = texture3D(B, vTexCoord).r;	

        color = max(oldA,oldB);
        

        }
        """
        
        fragment_source_difference = b"""
        #version 330
        out float color;
        varying vec3 vTexCoord;
        uniform sampler3D A;
        uniform sampler3D B;
        
        uniform float threshold;
        
        
        void main() {
        
        float oldA = texture3D(A, vTexCoord).r;				
        float oldB = texture3D(B, vTexCoord).r;	

        if(oldB > threshold)
        {
            color = 0.0;
        }
        else
        {
            color = oldA;
        }
        }
        """
        
        def setupShaders(self):
            self.programA = gl.glCreateProgram()
            gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_VERTEX_SHADER, self.vertex_source))
            if args["operation"] == "similar":
                gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_a))
            elif args["operation"] == "intersect":
                gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_intersection))
            elif args["operation"] == "union":
                gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_union))
            elif args["operation"] == "difference":
                gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_difference))
            else:
                print("not a valid operation")
            pyglet_helper.link_program(self.programA)
            
        def setupFBOandTextures(self):
            self.framebufferA0 = (gl.GLuint * self.dimz)()
            
            self.A0_tex = gl.GLuint(0)
            self.A1_tex = gl.GLuint(0)
            self.B0_tex = gl.GLuint(0)
            
            self.draw_buffersA0 = (gl.GLenum * self.dimz)(gl.GL_COLOR_ATTACHMENT0)
            self.draw_buffersB0 = (gl.GLenum * self.dimz)(gl.GL_COLOR_ATTACHMENT0)
            
            gl.glGenFramebuffers(self.dimz, self.framebufferA0)
            
            gl.glGenTextures(1, ctypes.byref(self.A0_tex))
            gl.glGenTextures(1, ctypes.byref(self.A1_tex))
            gl.glGenTextures(1, ctypes.byref(self.B0_tex))
            
            
            #create textures
            #A
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A0_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, self.dimx, self.dimy, self.dimz, 0, gl.GL_RED, gl.GL_FLOAT, self.Ap)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            gl.glActiveTexture(gl.GL_TEXTURE1)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A1_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, self.dimx, self.dimy, self.dimz, 0, gl.GL_RED, gl.GL_FLOAT, 0)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            #B
            gl.glActiveTexture(gl.GL_TEXTURE2)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.B0_tex)
            gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, gl.GL_RED, self.dimx, self.dimy, self.dimz, 0, gl.GL_RED, gl.GL_FLOAT, self.Bp)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            
            #A
            for i in range(self.dimz):
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA0[i])
                gl.glFramebufferTexture3D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_3D, self.A1_tex, 0, i)
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
            
            self.tex_pos_A = gl.glGetUniformLocation(self.programA, b"A")
            self.tex_pos_B = gl.glGetUniformLocation(self.programA, b"B")
            self.threshold_pos = gl.glGetUniformLocation(self.programA, b"threshold")
            self.step_pos_A  = gl.glGetUniformLocation(self.programA, b"step")
            self.slice_pos_A  = gl.glGetUniformLocation(self.programA, b"slice")
            self.checkUniformLocation(self.tex_pos_A)
            self.checkUniformLocation(self.tex_pos_B)
            self.checkUniformLocation(self.threshold_pos)
            self.checkUniformLocation(self.step_pos_A)
            self.checkUniformLocation(self.slice_pos_A)

            gl.glUniform1f(self.threshold_pos, args["threshold"])
            #may need changed for nonsquare textures
            gl.glUniform1f(self.step_pos_A, 1/self.dimx)
            
            gl.glViewport(0,0,self.dimx,self.dimy)
            #self.clear()
            
        def cleanUP(self):
            a = (gl.GLfloat * (self.dimx*self.dimy*self.dimz))()
            #need a new way to read out pixels
            #gl.glReadPixels(0, 0, self.dimx, self.dimy , gl.GL_RGBA, gl.GL_FLOAT, b)
            #gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebufferA1);
            #gl.glReadPixels(0, 0, self.dimx, self.dimy , gl.GL_RGBA, gl.GL_FLOAT, a)
            gl.glBindTexture(gl.GL_TEXTURE_3D, self.A1_tex)
            gl.glGetTexImage(gl.GL_TEXTURE_3D, 0, gl.GL_RED, gl.GL_FLOAT, a)
            
            
            #self.flip() # This updates the screen, very much important.
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0);
            
            bufA = np.frombuffer(a, dtype=np.float32)
            
            bufA = bufA.reshape(args["A"].shape)

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
            gl.glUniform1i(self.tex_pos_A, 0)
            gl.glUniform1i(self.tex_pos_B, 2)
            for i in range(self.dimz):
                gl.glUniform1i(self.slice_pos_A, i)
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
    temps["A"] = np.random.rand(256, 256, 256)
    temps["B"] = np.random.rand(256, 256, 256)
    temps["operation"] = "difference"
    temps["threshold"] = 0.5
    OffScreenRender(temps, test=True)
    
    end = time.time()
    print("the 3d reaction diffusion took " + str(end-start))
    
