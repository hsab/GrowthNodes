import bpy
from bpy.types import NodeSocket

class IntegerSocket(NodeSocket):
    # Description string
    '''Custom Integer socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'IntegerSocketType'
    # Label for nice name display
    bl_label = 'Integer Socket'

    objectName = bpy.props.StringProperty()

    integer_value = bpy.props.IntProperty()

    def init(self, context):
        pass

    def draw_color(self, context, node):
        return (0, 1, 1, 0.5)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)