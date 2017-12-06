from ... base_types import UMOGNode
import numpy as np
import bpy
import pyximport
pyximport.install()
from ...events import events


class ConvolveNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ConvolveNode"
    bl_label = "Convolve Node"

    def init(self, context):
        self.outputs.new("TextureSocketType", "out")
        self.inputs.new("TextureSocketType", "Texture Input")
        self.inputs.new("Mat3SocketType", "Matrix Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        pass

    def execute(self, refholder):
        # compute A'
        print("convolve node")
        mask = refholder.matrices[self.inputs[1].links[0].from_socket.matrix_ref]
        A = refholder.np2dtextures[self.inputs[0].links[0].from_socket.texture_index]
        Ap = refholder.np2dtextures[self.outputs[0].texture_index]
        events.convolve2d(A, mask, Ap)

        print(" convolve min, max " + str(np.amin(Ap)) + "," + str(np.amax(Ap)))

    def preExecute(self, refholder):
        self.outputs[0].texture_index = refholder.createRefForTexture2d()