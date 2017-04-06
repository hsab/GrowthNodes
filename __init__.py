bl_info = {
    "name": "UMOG",
    "author": "Hirad Sabaghian, Micah Johnston, Marsh Poulson, Jacob Luke",
    "version": (0, 0, 2),
    "blender": (2, 78, 0),
    "location": "Node Editor > UMOG",
    "description": "Mesh Manipulation Tools",
    "warning": "prealpha",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy
import sys

bpy.types.Scene.StartFrame = bpy.props.IntProperty(
    name = "StartFrame", 
    description = "StartFrame",
    default = 1,
    min = 1)

bpy.types.Scene.EndFrame = bpy.props.IntProperty(
    name = "EndFrame", 
    description = "EndFrame",
    default = 2,
    min = 2)

bpy.types.Scene.SubFrames = bpy.props.IntProperty(
    name = "SubFrames", 
    description = "SubFrames",
    default = 1,
    min = 1)

class MyCustomSocket(bpy.types.NodeSocket):
    # Description string
    '''Custom node socket type'''
    bl_idname = 'CustomSocketType'
    # Label for nice name display
    bl_label = 'Custom Node Socket'
    # Socket color
    bl_color = (1.0, 0.4, 0.216, 0.5)
    
    def draw(self, context, layout, node, x):
        layout.label(self.name)

    def draw_color(self, context, node):
        return (1,1,1,1)

class HelloWorldPanel(bpy.types.Panel):
    bl_idname = "panel.panel3"
    bl_label = "UMOG"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"

    def draw(self, context):
        self.layout.operator("umog.bake_meshes", icon='RENDER_RESULT', text="Bake Mesh(es)")
        self.layout.prop(bpy.context.scene, 'StartFrame')
        self.layout.prop(bpy.context.scene, 'EndFrame')
        self.layout.prop(bpy.context.scene, 'SubFrames')

class UMOGNode(bpy.types.Node):
    bl_width_min = 10
    bl_width_max = 5000

    _IsUMOGNode = True
    
    bl_label = "UMOGNode"
    
    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "umog_UMOGNodeTree"
    
    def init(self, context):
        print('umog node base init')
			
class UMOGReferenceHolder:
    def __init__(self):
        self.references = {}
        
    def getRef(self, key):
        return references[key]
    
    def addRef(self, key, obj):
        references[key] = obj

class addCubeSample(bpy.types.Operator):
    bl_idname = 'mesh.add_cube_sample'
    bl_label = 'Add Cube'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {"FINISHED"}
    
class bakeMeshes(bpy.types.Operator):
    bl_idname = 'umog.bake_meshes'
    bl_label = 'Bake Mesh(es)'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        print(bpy.context.active_node)
        print(bpy.context.selected_nodes)
        bpy.context.active_node.execute()
        return {"FINISHED"}
			
class UMOGMeshInputNode(UMOGNode):
    bl_idname = "umog_MeshInputNode"
    bl_label = "UMOG Mesh Input Node"

    def init(self,context):
        print('initializing umog node')
        self.inputs.new("CustomSocketType", "My Input")
        self.outputs.new("CustomSocketType", "My Output")
        super().init(context)

class UMOGNoiseGenerationNode(UMOGNode):
    bl_idname = "umog_NoiseGenerationNode"
    bl_label = "UMOG Noise Generation Node"
    
    def init(self, context):
        print('initializing umog noise node')
        self.inputs.new("NodeSocketInt", "X")
        self.inputs.new("NodeSocketInt", "Y")
        self.inputs.new("NodeSocketInt", "Z")
        self.outputs.new("NodeSocketInt", "Output")
        super().init(context)

class PrintNode(UMOGNode):
    bl_idname = "umog_PrintNode"
    bl_label = "Print Node"
    
    def init(self, context):
        print('initializing umog print node')
        self.inputs.new("NodeSocketString", "Print String")
        super().init(context)

    def execute(self):
        """if self.inputs['Print String'].is_linked:
            input_String = "NOTHING ENTERED"
        else:
            input_String = self.inputs['Print String']
            
        print(input_String)"""
        print("THIS PRINT WORKS")

class UMOGNodeTree(bpy.types.NodeTree):
    """
    UMOG Node Tree

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"
    
    def __init__(self):
        self.refs = UMOGReferenceHolder()
        #if the current scene has parameters do nothing otherwise adde the global start and end frames
        print('initializing umog node tree')
        super().__init__()
        
    def execute(self):
        print('executing node tree');
        

def drawMenu(self, context):
    if context.space_data.tree_type != "umog_UMOGNodeTree": return
    
    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"
    layout.menu("umog_mesh_menu", text="Mesh", icon = "MESH_DATA")
# from animation nodes
def insertNode(layout, type, text, settings = {}, icon = "NONE"):
    operator = layout.operator("node.add_node", text = text, icon = icon)
    operator.type = type
    operator.use_transform = True
    for name, value in settings.items():
            item = operator.settings.add()
            item.name = name
            item.value = value
    return operator
	
#todo create the menu class
class UMOGMeshMenu(bpy.types.Menu):
    bl_idname = "umog_mesh_menu"
    bl_label = "Mesh Menu"
    
    def draw(self, context):
            layout = self.layout
            insertNode(layout, "umog_MeshInputNode", "Input Mesh")
            insertNode(layout, "umog_PrintNode", "Print")
            insertNode(layout, "umog_NoiseGenerationNode", "Noise Generator")

def register():
    print("begin resitration")
    # see for types to register https://docs.blender.org/api/2.78b/bpy.utils.html?highlight=register_class#bpy.utils.register_class
    bpy.types.NODE_MT_add.append(drawMenu)
    bpy.utils.register_class(HelloWorldPanel)
    bpy.utils.register_class(UMOGNodeTree)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(UMOGNodeTree)
    bpy.utils.unregister_module(__name__)
	
