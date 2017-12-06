import bpy
from . import EngineSocket

class ArraySocket(bpy.types.NodeSocket, EngineSocket):
    bl_idname = 'ArraySocketType'
    bl_label = 'Array Socket'

    def init(self, context):
        pass

    def draw_color(self, context, node):
        return (0, 1, 1, 0.5)
