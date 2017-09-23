from ... base_types import UMOGNode
from ... events import bgl_helper
import bpy
import bgl
import copy
import numpy as np
import pyximport
pyximport.install()
from ...events import events

class ReactionDiffusionBGLNode(UMOGNode):
    bl_idname = "umog_ReactionDiffusionBGLNode"
    bl_label = "Reaction Diffusion Node"

    feed = bpy.props.FloatProperty(default=0.055)
    kill = bpy.props.FloatProperty(default=0.062)
    Da = bpy.props.FloatProperty(default=1.0)
    Db = bpy.props.FloatProperty(default=0.5)
    dt = bpy.props.FloatProperty(default=1.0)
    steps = bpy.props.IntProperty(default=500)
    channels = bpy.props.EnumProperty(items=
        (('0', 'R', 'Just do the reaction on one channel'),
         ('1', 'RGB', 'Do the reaction on all color channels'),
        ),
        name="channels")
    
    
    temp_texture_prefix = "__umog_internal_"
    
    vertex_source = """
    #version 130
    in vec4 a_position;
    varying vec2 vTexCoord;
    void main() {
    vTexCoord = 0.5*(a_position.xy + vec2(1,1));
        gl_Position = a_position;
    }
    """
    fragment_source = """
    #version 130
    out vec4 color;
    varying vec2 vTexCoord;
    uniform sampler2D myTexture;
    void main() {
    //color = vec4(1,0.5,0,1);
    color =vec4(0.1, 0.1,0,0) +texture2D(myTexture, vTexCoord);
    }
    """

    def init(self, context):
        self.outputs.new("TextureSocketType", "A'")
        self.outputs.new("TextureSocketType", "B'")
        self.inputs.new("TextureSocketType", "A")
        self.inputs.new("TextureSocketType", "B")
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
        tr = bpy.context.scene.TextureResolution
        print("begining execution " + str(tr))
        # compute A'
        mask = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])
        Ap = refholder.np2dtextures[self.outputs[0].texture_index]
        A = refholder.np2dtextures[self.inputs[0].links[0].from_socket.texture_index]

        Bp = refholder.np2dtextures[self.outputs[1].texture_index]
        B = refholder.np2dtextures[self.inputs[1].links[0].from_socket.texture_index]
        
        bgl.glGetIntegerv(bgl.GL_CURRENT_PROGRAM, refholder.execution_scratch[self.name]["prev_program"])
        bgl.glUseProgram(refholder.execution_scratch[self.name]["program"])
        
        #set any uniforms needed
        
        bgl.glDisable(bgl.GL_SCISSOR_TEST)
        bgl.glViewport(0, 0, tr, tr)
        
        bgl.glMatrixMode(bgl.GL_MODELVIEW)
        bgl.glPushMatrix()
        bgl.glLoadIdentity()

        bgl.glMatrixMode(bgl.GL_PROJECTION)
        bgl.glPushMatrix()
        bgl.glLoadIdentity()
        bgl.gluOrtho2D(0, 1, 0, 1)
        
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        
        channels = []
        if self.channels == '0':
            channels = [0]
        elif self.channels == '1':
            channels = [0,1,2]
        
        for j in channels:
            refholder.np2dtextures[refholder.execution_scratch[self.name]["handle"]][:,:,0] = A[:,:,j]
            refholder.np2dtextures[refholder.execution_scratch[self.name]["handle"]][:,:,1] = B[:,:,j]
            
            refholder.handleToImage(refholder.execution_scratch[self.name]["handle"],
                                    refholder.execution_scratch[self.name]["image"])
            
            refholder.execution_scratch[self.name]["image"].gl_load(0, bgl.GL_NEAREST, bgl.GL_NEAREST)
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, refholder.execution_scratch[self.name]["image"].bindcode[0])
            
            for i in range(self.steps):
                bgl.glClearDepth(1.0)
                bgl.glClearColor(0.0, 0.0, 0.0, 0.0)
                bgl.glClear(
                    bgl.GL_COLOR_BUFFER_BIT |
                    bgl.GL_DEPTH_BUFFER_BIT
                )
                
                bgl.glBegin(bgl.GL_TRIANGLES)

                bgl.glColor3f(1.0, 1.0, 1.0)
                bgl.glTexCoord2f(0.0, 0.0)
                bgl.glVertex2f(-1.0, -1.0)
                bgl.glTexCoord2f(1.0, 0.0)
                bgl.glVertex2f(1.0, -1.0)
                bgl.glTexCoord2f(1.0, 1.0)
                bgl.glVertex2f(1.0, 1.0)

                bgl.glColor3f(1.0, 1.0, 1.0)
                bgl.glTexCoord2f(0.0, 0.0)
                bgl.glVertex2f(-1.0, -1.0)
                bgl.glTexCoord2f(1.0, 1.0)
                bgl.glVertex2f(1.0, 1.0)
                bgl.glTexCoord2f(0.0, 1.0)
                bgl.glVertex2f(-1.0, 1.0)
                bgl.glEnd()
                
                bgl.glCopyTexImage2D(
                    bgl.GL_TEXTURE_2D, #target
                    0, #level
                    bgl.GL_RGBA, #internalformat
                    0, #x
                    0, #y
                    tr,
                    tr,
                    0 #border
                    )
                
                #glFlush glFinish or none here?
                bgl.glFinish()
        
            bgl.glReadPixels(0, 0, tr, tr , bgl.GL_RGBA, bgl.GL_FLOAT, refholder.execution_scratch[self.name]["buffer"])
            refholder.execution_scratch[self.name]["image"].pixels = refholder.execution_scratch[self.name]["buffer"][:]
            #write the image channel
            
            refholder.imageToHandle(refholder.execution_scratch[self.name]["image"],
                refholder.execution_scratch[self.name]["handle"])
            Ap[:,:,j] = refholder.np2dtextures[refholder.execution_scratch[self.name]["handle"]][:,:,0]
            Bp[:,:,j] = refholder.np2dtextures[refholder.execution_scratch[self.name]["handle"]][:,:,1]
            refholder.execution_scratch[self.name]["image"].gl_free()
        
        
        #restore the state so blender wont break
        bgl.glEnable(bgl.GL_SCISSOR_TEST)
        bgl.glUseProgram(refholder.execution_scratch[self.name]["prev_program"][0])
        bgl.glActiveTexture(bgl.GL_TEXTURE0)

    def preExecute(self, refholder):
        self.outputs[0].texture_index = refholder.createRefForTexture2d()
        self.outputs[1].texture_index = refholder.createRefForTexture2d()
        refholder.execution_scratch[self.name] = {}
        refholder.execution_scratch[self.name]["image"] = bpy.data.images.new(self.temp_texture_prefix + self.name, width=bpy.context.scene.TextureResolution,
                                    height=bpy.context.scene.TextureResolution)
        refholder.execution_scratch[self.name]["handle"] = refholder.createRefForTexture2d() 
        vertex_shader = bgl_helper.createShader(bgl.GL_VERTEX_SHADER, self.vertex_source)
        fragment_shader = bgl_helper.createShader(bgl.GL_FRAGMENT_SHADER,
                                                  self.fragment_source)
        refholder.execution_scratch[self.name]["program"] = bgl_helper.createProgram(vertex_shader, fragment_shader)
        refholder.execution_scratch[self.name]["prev_program"] = bgl.Buffer(bgl.GL_INT, [1])
        refholder.execution_scratch[self.name]["buffer"] = bgl.Buffer(bgl.GL_FLOAT, (bpy.context.scene.TextureResolution ** 2) * 4)
        
def postBake(self, refholder):
        bpy.data.images.remove(refholder.execution_scratch[self.name]["image"])
        #TODO clean up the shader stuff
        pass
    
def render(self):
    pass
