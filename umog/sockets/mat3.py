import bpy
from .. base_types import UMOGSocket

class Mat3Socket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Mat3SocketType'
    # Label for nice name display
    bl_label = 'Mat3 Socket'
    dataType = "Mat3"
    allowedInputTypes = ["Mat3"]

    
    objectName = bpy.props.StringProperty()
    
    matrix_ref = bpy.props.IntProperty()
    
    def init(self, context):
        pass

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        #        if self.is_output or self.is_linked:
        #            layout.label(text)
        #        else:
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.4, 0.4, 1.0, 0.5)
