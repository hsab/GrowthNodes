from ..umog_node import UMOGNode
import bpy
import numpy as np

class GaussNode(UMOGNode):
    bl_idname = "umog_GaussNode"
    bl_label = "Gaussian Blur"

    gauss_matrix = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])
    
    def init(self, context):
        self.outputs.new("Mat3SocketType", "Output")
        super().init(context)

    def preExecute(self, refholder):
        print('begin preExecute gauss')
        
        self.outputs[0].matrix_ref = refholder.getRefForMatrix(self.gauss_matrix)

    def execute(self, refholder):
        print('begin gauss')
        for elem in self.gauss_matrix:
            print(elem)