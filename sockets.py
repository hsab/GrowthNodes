import bpy
from bpy.types import NodeSocket

################################
# START: Sockets
class GetBaseInputSocket(NodeSocket):
    # Description string
    '''Custom Texture socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'BaseInputSocketType'
    # Label for nice name display
    bl_label = 'Get Input Socket'
    
    objectName = bpy.props.StringProperty()
    
    def init(self, context):
        pass
        
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)


    # Socket color
    def draw_color(self, context, node):
        return (1, 1, 1, 0.5)
    #these will return a reference to the bind point adn index for passing parameters
    def get_bind_point(self):
        pass
    def get_bind_index(self):
        pass
    
class TextureSocket(NodeSocket):
    # Description string
    '''Custom Texture socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'TextureSocketType'
    # Label for nice name display
    bl_label = 'Texture Socket'
    
    objectName = bpy.props.StringProperty()
    
    def init(self, context):
        pass
        
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)


    # Socket color
    def draw_color(self, context, node):
        return (0, 0, 1, 0.5)
    #these will return a reference to the bind point adn index for passing parameters
    def get_bind_point(self):
        return 'texture'
    def get_bind_index(self):
        return 'texture_index'
    
class Mat3Socket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Mat3SocketType'
    # Label for nice name display
    bl_label = 'Mat3 Socket'
    
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
        return (0.0, 0.0, 1.0, 0.5)
# END: Sockets
################################
