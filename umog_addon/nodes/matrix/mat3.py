from ... base_types import UMOGNode
import bpy
import numpy as np

class Mat3Node(bpy.types.Node, UMOGNode):
    bl_idname = "umog_Mat3Node"
    bl_label = "Matrix"

    matrix = bpy.props.FloatVectorProperty(size=16, default=(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))
    
    def init(self, context):
        self.outputs.new("Mat3SocketType", "Output")
        self.newInput("Float", "Alpha", "alpha", value = 1.0)
        self.newOutput("Float", "Test", "text")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'matrix')

    def preExecute(self, refholder):
        print('begin preExecute mat3')
        new_matrix = np.zeros(16)
        i = 0
        for elem in self.matrix:
            new_matrix[i] = elem
            i += 1
        new_matrix = new_matrix.reshape((4,4))
        self.outputs[0].matrix_ref = refholder.getRefForMatrix(new_matrix)

    def execute(self, refholder):
        print('begin matrix')
        for elem in self.matrix:
            print(elem)