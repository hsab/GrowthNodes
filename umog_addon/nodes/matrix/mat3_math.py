from ... base_types import UMOGNode
import bpy
import numpy as np

class MatrixMathNode(UMOGNode):
    bl_idname = "umog_MatrixMathNode"
    bl_label = "UMOG Matrix Math"

    fixed_items = bpy.props.EnumProperty(items=
                                         (('0', '+', 'addition'),
                                          ('1', '-', 'subtraction'),
                                          ('2', '*', 'multiplication'),
                                          ),
                                         name="fixed list")

    def init(self, context):
        self.outputs.new("Mat3SocketType", "MatrixOut")
        self.inputs.new("Mat3SocketType", "Matrix0")
        self.inputs.new("Mat3SocketType", "Matrix1")
        super().init(context)

    def execute(self, refholder):
    
        answer_matrix = np.zeros(16)
    
        if self.fixed_items == '0':
            print("addition")
            answer_matrix = np.add(refholder.matrices[self.inputs[0].links[0].from_socket.matrix_ref],
                                    refholder.matrices[self.inputs[1].links[0].from_socket.matrix_ref])
                                    
        elif self.fixed_items == '1':
            print("subtraction")
            answer_matrix = np.subtract(refholder.matrices[self.inputs[0].links[0].from_socket.matrix_ref],
                                    refholder.matrices[self.inputs[1].links[0].from_socket.matrix_ref])
            
        elif self.fixed_items == '2':
            print("multiplication")
            matrix1 = refholder.matrices[self.inputs[0].links[0].from_socket.matrix_ref]
            matrix2 = refholder.matrices[self.inputs[1].links[0].from_socket.matrix_ref]
            answer_matrix = np.matmul(matrix1, matrix2)
            
        for elem in answer_matrix:
            print(elem)
        
        self.outputs[0].matrix_ref = refholder.getRefForMatrix(answer_matrix) 
            
    def draw_buttons(self, context, layout):
        layout.prop(self, "fixed_items", 'Operation')