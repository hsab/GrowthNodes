import bpy
from . import EngineSocket

class MeshSocket(bpy.types.NodeSocket, EngineSocket):
    bl_idname = 'MeshSocketType'
    bl_label = 'Mesh Socket'

    def init(self, context):
        pass

    def draw_color(self, context, node):
        return (1, 0, 0, 0.5)
