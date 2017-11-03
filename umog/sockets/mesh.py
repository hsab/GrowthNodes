import bpy
from bpy.types import NodeSocket

class MeshSocket(NodeSocket):
    bl_idname = 'MeshSocketType'
    bl_label = 'Mesh Socket'

    def draw_color(self, context, node):
        return (1, 0, 0, 0.5)

    def init(self, context):
        pass

    def draw(self, context, layout, node, text):
        layout.label(text=text)