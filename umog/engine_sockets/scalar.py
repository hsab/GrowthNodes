import bpy
from . import EngineSocket

class ScalarSocket(bpy.types.NodeSocket, EngineSocket):
    bl_idname = 'ScalarSocketType'
    bl_label = 'Scalar Socket'

    def init(self, context):
        pass

    def draw_color(self, context, node):
        return (0, 0, 1, 0.5)
