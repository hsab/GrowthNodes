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
    //color = vec4(0,1,0,1);
    color = texture2D(myTexture, vTexCoord);
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

    def update(self):
        pass

    def execute(self, refholder):
        # compute A'
        mask = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])
        Ap = refholder.np2dtextures[self.outputs[0].texture_index]
        A = refholder.np2dtextures[self.inputs[0].links[0].from_socket.texture_index]
        A *= refholder.execution_scratch[self.name]["Ap_scale"]
        A += refholder.execution_scratch[self.name]["Ap_offset"]
        LA = copy.deepcopy(A)
        events.convolve2d(Ap, mask, LA)

        Bp = refholder.np2dtextures[self.outputs[1].texture_index]
        B = refholder.np2dtextures[self.inputs[1].links[0].from_socket.texture_index]
        B *= refholder.execution_scratch[self.name]["Bp_scale"]
        B += refholder.execution_scratch[self.name]["Bp_offset"]
        LB = copy.deepcopy(B)
        events.convolve2d(Bp, mask, LB)

        events.ReactionDiffusion2d(A, Ap, LA, B, Bp, LB, mask, self.Da, self.Db, self.feed, self.kill, self.dt)
        
        refholder.execution_scratch[self.name]["Ap_offset"] = np.amin(Ap)
        refholder.execution_scratch[self.name]["Ap_scale"] = np.amax(Ap) - np.amin(Ap)
        refholder.execution_scratch[self.name]["Bp_offset"] = np.amin(Bp)
        refholder.execution_scratch[self.name]["Bp_scale"] = np.amax(Bp) - np.amin(Bp)
        
        Ap -= refholder.execution_scratch[self.name]["Ap_offset"]
        Ap /= refholder.execution_scratch[self.name]["Ap_scale"]
        Bp -= refholder.execution_scratch[self.name]["Bp_offset"]
        Bp /= refholder.execution_scratch[self.name]["Bp_scale"]
        

    def preExecute(self, refholder):
        self.outputs[0].texture_index = refholder.createRefForTexture2d()
        self.outputs[1].texture_index = refholder.createRefForTexture2d()
        refholder.execution_scratch[self.name] = {}
        refholder.execution_scratch[self.name]["Ap_offset"] = 0.0
        refholder.execution_scratch[self.name]["Ap_scale"] = 1.0
        refholder.execution_scratch[self.name]["Bp_offset"] = 0.0
        refholder.execution_scratch[self.name]["Bp_scale"] = 1.0
        refholder.execution_scratch[self.name]["imageA"] = bpy.data.images.new(self.temp_texture_prefix + self.name, width=bpy.context.scene.TextureResolution,
                                    height=bpy.context.scene.TextureResolution)
        refholder.execution_scratch[self.name]["imageB"] = bpy.data.images.new(self.temp_texture_prefix + self.name, width=bpy.context.scene.TextureResolution,
                                    height=bpy.context.scene.TextureResolution)
        vertex_shader = bgl_helper.createShader(bgl.GL_VERTEX_SHADER, self.vertex_source)
        fragment_shader = bgl_helper.createShader(bgl.GL_FRAGMENT_SHADER,
                                                  self.fragment_source)
        refholder.execution_scratch[self.name]["program"] = bgl_helper.createProgram(vertex_shader, fragment_shader)
        refholder.execution_scratch[self.name]["prev_program"] = bgl.Buffer(bgl.GL_INT, [1])
        
def postBake(self, refholder):
        bpy.data.images.remove(refholder.execution_scratch[self.name]["imageA"])
        bpy.data.images.remove(refholder.execution_scratch[self.name]["imageB"])
        #TODO clean up the shader stuff
        pass
    
def render(self):
    
