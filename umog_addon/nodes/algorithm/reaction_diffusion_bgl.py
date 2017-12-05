import bpy
import bgl
import copy
import numpy as np
from ... base_types import UMOGNode
from ... events import bgl_helper
import pyximport
pyximport.install()
from ...events import events

class UMOGReactionDiffusionData(dict):
    bl_idname = "umog_ReactionDiffusionData"

    def __init__(self):
        pass

class ReactionDiffusionBGLNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ReactionDiffusionBGLNode"
    bl_label = "2D Reaction Diffusion"

    assignedType = "Texture2"
    rdData = UMOGReactionDiffusionData()


    feed = bpy.props.FloatProperty(default=0.014, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    kill = bpy.props.FloatProperty(default=0.046, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    Da = bpy.props.FloatProperty(default=0.2, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    Db = bpy.props.FloatProperty(default=0.09, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    dt = bpy.props.FloatProperty(default=0.3, soft_min=0.0, soft_max=1.0, step=1, precision=4)
    steps = bpy.props.IntProperty(default=500, min=1, step=500)
    channels = bpy.props.EnumProperty(items=
        (('0', 'R', 'Just do the reaction on one channel'),
         ('1', 'RGB', 'Do the reaction on all color channels'),
        ),
        name="Channels")
    
    
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

    def create(self):
        self.newInput(self.assignedType, "A").isPacked = True
        self.newInput(self.assignedType, "B").isPacked = True
        self.newInput("Float", "Feed", value=0.055, minValue = 0.0, maxValue = 1.0).isPacked = True
        self.newInput("Float", "Kill", value=0.062, minValue = 0.0, maxValue = 1.0).isPacked = True
        self.newInput("Float", "A Rate", value=1.0, minValue = 0.0, maxValue = 1.0).isPacked = True
        self.newInput("Float", "B Rate", value=0.5, minValue = 0.0, maxValue = 1.0).isPacked = True
        self.newInput("Float", "Delta Time", value=1.0, minValue = 0.0, maxValue = 1.0).isPacked = True
        self.newInput("Integer", "Steps", value=1, minValue = 1).isPacked = True
        self.newOutput(self.assignedType, "A'").isPacked = True
        self.newOutput(self.assignedType, "B'").isPacked = True
        self.newOutput(self.assignedType, "Combined").isPacked = True

    def draw(self, layout):
        layout.prop(self, "channels", "Channels")

        
    def refresh(self):
        pass

    def execute(self, refholder):
        # pass
        tr = self.nodeTree.properties.TextureResolution
        print("begining execution " + str(tr))
        # compute A'
        mask = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])
        # Input data pixels
        A = self.inputs[0].getPixels()
        B = self.inputs[1].getPixels()
        
        # print(A)

        bgl.glGetIntegerv(bgl.GL_CURRENT_PROGRAM, self.rdData[self.name]["prev_program"])
        bgl.glUseProgram(self.rdData[self.name]["program"])
        
        #set any uniforms needed
        bgl.glUniform1f(self.rdData[self.name]["feed_loc"], self.inputs[2].value)
        bgl.glUniform1f(self.rdData[self.name]["kill_loc"], self.inputs[3].value)
        bgl.glUniform1f(self.rdData[self.name]["da_loc"], self.inputs[4].value)
        bgl.glUniform1f(self.rdData[self.name]["db_loc"], self.inputs[5].value)
        bgl.glUniform1f(self.rdData[self.name]["dt_loc"], self.inputs[6].value)
        bgl.glUniform1f(self.rdData[self.name]["step_loc"], 1/tr)
        
        
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
            self.rdData[self.name]["npArray"][:,:,0] = A[:,:,j]
            self.rdData[self.name]["npArray"][:,:,1] = B[:,:,j]
            
            # Caution: Interfacing with Cython requires toList()
            self.rdData[self.name]["image"].pixels = self.rdData[self.name]["npArray"].flatten()

            
            self.rdData[self.name]["image"].gl_load(0, bgl.GL_LINEAR, bgl.GL_LINEAR)

            bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.rdData[self.name]["image"].bindcode[0])
            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_S, bgl.GL_REPEAT)
            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_T, bgl.GL_REPEAT)
            
            for i in range(self.inputs[7].value):
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
        
            bgl.glReadPixels(0, 0, tr, tr , bgl.GL_RGBA, bgl.GL_FLOAT, self.rdData[self.name]["buffer"])
            self.rdData[self.name]["image"].pixels = self.rdData[self.name]["buffer"][:]
            #write the image channel
            npImage = np.asarray(self.rdData[self.name]["image"].pixels, dtype = "float")
            self.rdData[self.name]["npArray"] = npImage.reshape(tr, tr, self.rdData[self.name]["image"].channels)

            self.outputs[0].setPackedImageFromChannels(self.rdData[self.name]["npArray"][:,:,0], j, flatten = True)
            self.outputs[1].setPackedImageFromChannels(self.rdData[self.name]["npArray"][:,:,1], j,flatten = True)
            self.outputs[2].setPackedImageFromPixels(self.rdData[self.name]["npArray"])
            
            self.inputs[0].setPackedImageFromChannels(self.rdData[self.name]["npArray"][:,:,0], j,flatten = True)
            self.inputs[1].setPackedImageFromChannels(self.rdData[self.name]["npArray"][:,:,1], j,flatten = True)
            
            # ================================= Test bed
            # self.outputs[0].getTexture().image.copy()
            # self.outputs[1].getTexture().image.copy()
            # self.outputs[2].getTexture().image.copy()

            # nparr = np.asarray(self.outputs[0].getTexture().image.pixels, dtype="float")
            # nparr = nparr.reshape(tr, tr, 4)
            # print(nparr)
            
            self.rdData[self.name]["image"].gl_free()
        
        
        #restore the state so blender wont break
        bgl.glEnable(bgl.GL_SCISSOR_TEST)
        bgl.glUseProgram(self.rdData[self.name]["prev_program"][0])
        bgl.glActiveTexture(bgl.GL_TEXTURE0)

    # TODO: Handle refholder!
    def preExecute(self, refholder):
        # pass
        self.rdData[self.name] = {}

        D = bpy.data
        textureName = self.nodeTree.name + " - " + self.identifier
        resolution = self.nodeTree.properties.TextureResolution
        if textureName in D.images:
            D.images.remove(D.images[textureName])

        image  = bpy.data.images.new(textureName, width=resolution, height=resolution)

        self.rdData[self.name]["image"] = image
        npImage = np.asarray(image.pixels, dtype = "float")
        self.rdData[self.name]["npArray"] = npImage.reshape(resolution, resolution, image.channels)

        vertex_shader = bgl_helper.createShader(bgl.GL_VERTEX_SHADER, self.vertex_source)
        fragment_shader = bgl_helper.createShader(bgl.GL_FRAGMENT_SHADER,
                                                  self.fragment_source)
        self.rdData[self.name]["program"] = bgl_helper.createProgram(vertex_shader, fragment_shader)
        self.rdData[self.name]["prev_program"] = bgl.Buffer(bgl.GL_INT, [1])
        self.rdData[self.name]["buffer"] = bgl.Buffer(bgl.GL_FLOAT, (resolution ** 2) * 4)
        
        program = self.rdData[self.name]["program"]
        
        self.rdData[self.name]["dt_loc"] = bgl.glGetUniformLocation(program, "timestep")
        self.rdData[self.name]["step_loc"] = bgl.glGetUniformLocation(program, "step")
        self.rdData[self.name]["da_loc"] = bgl.glGetUniformLocation(program, "du")
        self.rdData[self.name]["db_loc"] = bgl.glGetUniformLocation(program, "dv")
        self.rdData[self.name]["kill_loc"] = bgl.glGetUniformLocation(program, "k")
        self.rdData[self.name]["feed_loc"] = bgl.glGetUniformLocation(program, "f")
        
        
def postBake(self, refholder):
        pass
    
def render(self):
    pass