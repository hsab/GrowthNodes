from ... base_types import UMOGNode
import bpy

class Mat3Node(bpy.types.Node, UMOGNode):
    bl_idname = "umog_Mat3Node"
    bl_label = "Matrix"

    # matrix = bpy.props.FloatVectorProperty(size = 16,subtype='MATRIX', default = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))
    matrix = bpy.props.FloatVectorProperty(size=16, default=(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))

    def init(self, context):
        self.outputs.new("Mat3SocketType", "Output")
        self.inputs.new("Mat3SocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'matrix')

    def execute(self, refholder):
        print('begin matrix')
        for elem in self.matrix:
            print(elem)