from ... base_types import UMOGNode
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()
from ...events import events

class ReactionDiffusionNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ReactionDiffusionNode"
    bl_label = "Reaction Diffusion Node"

    feed = bpy.props.FloatProperty(default=0.055)
    kill = bpy.props.FloatProperty(default=0.062)
    Da = bpy.props.FloatProperty(default=1.0)
    Db = bpy.props.FloatProperty(default=0.5)
    dt = bpy.props.FloatProperty(default=1.0)

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
