from ... base_types import UMOGNode
import bpy
import numpy as np

class GaussNode(UMOGNode):
    bl_idname = "umog_GaussNode"
    bl_label = "Gaussian Blur"

    gauss_matrix = np.array([[0.00000067, 0.00002292, 0.00019117, 0.00038771, 0.00019117, 0.00002292, 0.00000067],
    [0.00002292,0.00078634,0.00655965,0.01330373,0.00655965,0.00078633,0.00002292],
    [0.00019117,0.00655965,0.05472157,0.11098164,0.05472157,0.00655965,0.00019117],
    [0.00038771,0.01330373,0.11098164,0.22508352,0.11098164,0.01330373,0.00038771],
    [0.00019117,0.00655965,0.05472157,0.11098164,0.05472157,0.00655965,0.00019117],
    [0.00002292,0.00078633,0.00655965,0.01330373,0.00655965,0.00078633,0.00002292],
    [0.00000067,0.00002292,0.00019117,0.00038771,0.00019117,0.00002292,0.00000067]])
    
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