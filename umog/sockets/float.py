import bpy
from bpy.types import NodeSocket

class FloatSocket(NodeSocket):
    # Description string
    '''Custom Integer socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'FloatSocketType'
    # Label for nice name display
    bl_label = 'Float Socket'

    objectName = bpy.props.StringProperty()

    float_value = bpy.props.FloatProperty()

    def draw_color(self, context, node):
        return (1, 0, 1, 0.5)

    def init(self, context):
        pass

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)