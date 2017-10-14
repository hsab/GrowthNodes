def Dummy(steps, in_buffer, out_buffer):
    print("dummy")
    return True

def OffScreenRender(steps, args, test=False):
    try:
        if test:
            import pyglet
            from pyglet import gl
            import ctypes
            import pyglet_helper
            import numpy as np
        else:
            from ... events import pyglet_helper
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
        varying vec2 vTexCoord;
        void main() {
        vTexCoord = 0.5*(a_position.xy + vec2(1,1));
        gl_Position = vec4(a_position, 0.0, 1.0);
        }
        """
        
        fragment_source_a = b"""
        #version 330
        out vec4 color;
        varying vec2 vTexCoord;
        uniform sampler2D A;
        uniform sampler2D B;
        
        uniform float step;

        uniform float dA;
        uniform float dB;

        float distance = 1.5;
        uniform float timestep;

        uniform float k;
        uniform float f;
        
        void main() {
        
        vec4 oldA = texture2D(A, vTexCoord);				
        vec4 oldB = texture2D(B, vTexCoord);	

        // [rad] Compute approximation of Laplacian for both V and U.
        vec4 otherA = -4.0 * oldA;
        vec4 otherB = -4.0 * oldB;

        otherA += texture2D(A, vTexCoord + vec2(-step, 0));
        otherA += texture2D(A, vTexCoord + vec2(step, 0));
        otherA += texture2D(A, vTexCoord + vec2(0, -step));
        otherA += texture2D(A, vTexCoord + vec2(0, step));

        otherB += texture2D(B, vTexCoord + vec2(-step, 0));
        otherB += texture2D(B, vTexCoord + vec2(step, 0));
        otherB += texture2D(B, vTexCoord + vec2(0, -step));
        otherB += texture2D(B, vTexCoord + vec2(0, step));

        float distance_squared = distance * distance;
        
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
        varying vec2 vTexCoord;
        uniform sampler2D A;
        uniform sampler2D B;
        
        uniform float step;

        uniform float dA;
        uniform float dB;

        float distance = 1.5;
        uniform float timestep;

        uniform float k;
        uniform float f;
        
        void main() {
        
        vec4 oldA = texture2D(A, vTexCoord);				
        vec4 oldB = texture2D(B, vTexCoord);	

        // [rad] Compute approximation of Laplacian for both V and U.
        vec4 otherA = -4.0 * oldA;
        vec4 otherB = -4.0 * oldB;

        otherA += texture2D(A, vTexCoord + vec2(-step, 0));
        otherA += texture2D(A, vTexCoord + vec2(step, 0));
        otherA += texture2D(A, vTexCoord + vec2(0, -step));
        otherA += texture2D(A, vTexCoord + vec2(0, step));

        otherB += texture2D(B, vTexCoord + vec2(-step, 0));
        otherB += texture2D(B, vTexCoord + vec2(step, 0));
        otherB += texture2D(B, vTexCoord + vec2(0, -step));
        otherB += texture2D(B, vTexCoord + vec2(0, step));

        float distance_squared = distance * distance;
        
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
        
        def __init__(self, frames):
            #consider bumping opengl version if apple supports it
            #amdgpu-mesa currently supports up to 4.5
            super(ControledRender, self).__init__(512, 512, fullscreen = False, config=gl.Config(major_version=4, minor_version=1), visible=False)
            print(self.context.get_info().get_version())
            
            self.frames = frames
            self.vertex_buffer = gl.GLuint(0)
            self.vao = gl.GLuint(0)
            self.framebuffer = gl.GLuint(0)
            self.framebuffer0 = gl.GLuint(0)
            self.temp_tex = gl.GLuint(0)
            self.temp_tex0 = gl.GLuint(0)
            #self.prev_program = (gl.GLint * 1)()
            
            
            self.dimx = args["A"].shape[0]
            self.dimy = args["A"].shape[1]
            
            
            
            A = args["A"].astype(np.float32)
            print("A shape " + str(A.shape))
            print(str(A.dtype))
            print(A)
            
            B = args["B"].astype(np.float32)
            
            #self.dp = self.tdata.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
            self.dp = A.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
            
            gl.glGenFramebuffers(1, ctypes.byref(self.framebuffer))
            gl.glGenFramebuffers(1, ctypes.byref(self.framebuffer0))
            gl.glGenTextures(1, ctypes.byref(self.temp_tex))
            gl.glGenTextures(1, ctypes.byref(self.temp_tex0))
            

            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.temp_tex0)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.dimx, self.dimy, 0, gl.GL_RGBA, gl.GL_FLOAT, self.dp)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self.temp_tex0, 0)
            self.draw_buffers0 = (gl.GLenum * 1)(gl.GL_COLOR_ATTACHMENT0)
            gl.glDrawBuffers(1, self.draw_buffers0)

            assert gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE
            
            
            gl.glActiveTexture(gl.GL_TEXTURE1)
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)
            # Set up the texture as the target for color output
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.temp_tex)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.dimx, self.dimy, 0, gl.GL_RGBA, gl.GL_FLOAT, self.dp)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self.temp_tex, 0)

            self.draw_buffers = (gl.GLenum * 1)(gl.GL_COLOR_ATTACHMENT0)
            gl.glDrawBuffers(1, self.draw_buffers)

            assert gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE
            
            self.programA = gl.glCreateProgram()
            gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_VERTEX_SHADER, self.vertex_source))
            gl.glAttachShader(self.programA, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_a))
            pyglet_helper.link_program(self.programA)
            
            self.programB = gl.glCreateProgram()
            gl.glAttachShader(self.programB, pyglet_helper.compile_shader(gl.GL_VERTEX_SHADER, self.vertex_source))
            gl.glAttachShader(self.programB, pyglet_helper.compile_shader(gl.GL_FRAGMENT_SHADER, self.fragment_source_b))
            pyglet_helper.link_program(self.programB)
            
            
            gl.glUseProgram(self.programA)
            
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
            
            self.pos_pos = gl.glGetAttribLocation(self.programA, ctypes.create_string_buffer(b"a_position"))
            assert(self.pos_pos >= 0)
            gl.glEnableVertexAttribArray(self.pos_pos)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
            gl.glVertexAttribPointer(self.pos_pos, 2, gl.GL_FLOAT, False, 0, 0)
            
            self.tex_pos = gl.glGetUniformLocation(self.programA, b"myTexture")
            
            gl.glViewport(0,0,self.dimx,self.dimy)
            #self.clear()
            
        def cleanUP(self):
            a = (gl.GLint * (self.dimx*self.dimy*4))()
            gl.glReadPixels(0, 0, self.dimx, self.dimy , gl.GL_RGBA, gl.GL_FLOAT, a)
            #self.flip() # This updates the screen, very much important.
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0);
            
            
            buf = np.frombuffer(a, dtype=np.float32)
            #consider casting to float64
            args["Aout"] = buf
        
        def on_draw(self):
            self.render()

        def on_close(self):
            self.alive = 0

        def render(self):
            gl.glUniform1i(self.tex_pos, 1)
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer0);
            
            gl.glClearColor(0, 0, 0, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)

            gl.glUniform1i(self.tex_pos, 0)
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer);
            
            
            gl.glClearColor(0, 0, 0, 1.0)
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
    cr.run()
    cr.cleanUP()
    cr.close()
    #del cr
    #cr = None
    print("end of osr")
    
if __name__ == "__main__":
    curr = {}
    curr["buffer"] = {}
    OffScreenRender(4,curr, test=True)
