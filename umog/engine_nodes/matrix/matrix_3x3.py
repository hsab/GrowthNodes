from ..engine_node import *
from ...engine import types, engine
import bpy
import numpy as np

class Matrix3x3Node(bpy.types.Node, EngineNode):
    bl_idname = "engine_Matrix3x3Node"
    bl_label = "3x3 Matrix"

    row1 = bpy.props.FloatVectorProperty(size=3, default=(1, 0, 0))
    row2 = bpy.props.FloatVectorProperty(size=3, default=(0, 1, 0))
    row3 = bpy.props.FloatVectorProperty(size=3, default=(0, 0, 1))

    def init(self, context):
        self.outputs.new("ArraySocketType", "Output")
        self.width = 250
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'row1', text='')
        layout.prop(self, 'row2', text='')
        layout.prop(self, 'row3', text='')

    def get_operation(self, input_types):
        return engine.Operation(
            engine.CONST,
            [types.Array(0,3,3,0,0,0)],
            [types.Array(0,3,3,0,0,0)],
            [])

    def get_default_value(self, index, argument_type):
        return np.column_stack((np.array(self.row1, dtype=np.float32, order="F"), np.array(self.row2, dtype=np.float32, order="F"), np.array(self.row3, dtype=np.float32, order="F"))).reshape((1,3,3,1,1))

    def update(self):
        pass
