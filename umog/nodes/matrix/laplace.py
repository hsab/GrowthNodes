from ... base_types import UMOGNode
import bpy
import numpy as np

class LaplaceNode(UMOGNode):
    bl_idname = "umog_LaplaceNode"
    bl_label = "Laplace Filter"

    laplace_matrix = np.array([[0.0, -1.0, 0.0], [-1.0, 4.0, -1.0], [0.0, -1.0, 0.0]])
    
    def init(self, context):
        self.outputs.new("Mat3SocketType", "Output")
        super().init(context)

    def preExecute(self, refholder):
        print('begin preExecute laplace')
        
        self.outputs[0].matrix_ref = refholder.getRefForMatrix(self.laplace_matrix)

    def execute(self, refholder):
        print('begin laplace')
        for elem in self.laplace_matrix:
            print(elem)