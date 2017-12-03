import bpy
from . import UMOGSocket

class ArraySocket(bpy.types.NodeSocket, UMOGSocket):
    bl_idname = 'ArraySocketType'
    bl_label = 'Array Socket'

    def init(self, context):
        pass

    def draw_color(self, context, node):
        return (0, 1, 1, 0.5)
