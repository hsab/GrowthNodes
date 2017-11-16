import bpy
from . import UMOGSocket

class ArraySocket(UMOGSocket):
    bl_idname = 'ArraySocketType'
    bl_label = 'Array Socket'

    def draw_color(self, context, node):
        return (0, 0, 1, 0.5)

    def init(self, context):
        pass

    def draw(self, context, layout, node, text):
        layout.label(text=text)