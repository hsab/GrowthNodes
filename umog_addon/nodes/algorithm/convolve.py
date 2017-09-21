from ..umog_node import UMOGNode
import numpy as np
import pyximport
pyximport.install()
from ...events import events

class ConvolveNode(UMOGNode):
    bl_idname = "umog_ConvolveNode"
    bl_label = "Convolve Node"

    def init(self, context):
        self.outputs.new("TextureSocketType", "out")
        self.inputs.new("TextureSocketType", "in")
        super().init(context)

    def draw_buttons(self, context, layout):
        pass

    def update(self):
        pass

    def execute(self, refholder):
        # compute A'
        print("convolve node")
        mask = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])
        A = refholder.np2dtextures[self.inputs[0].links[0].from_socket.texture_index]
        Ap = refholder.np2dtextures[self.outputs[0].texture_index]
        events.convolve2d(A, mask, Ap)

        print(" convolve min, max " + str(np.amin(Ap)) + "," + str(np.amax(Ap)))

    def preExecute(self, refholder):
        self.outputs[0].texture_index = refholder.createRefForTexture2d()