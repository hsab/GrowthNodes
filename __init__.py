bl_info = {
    "name": "UMOG",
    "author": "Hirad Sabaghian, Micah Johnston, Marsh Poulson, Jacob Luke",
    "version": (0, 1, 0),
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
from bpy.types import NodeTree, Node, NodeSocket
import mathutils




#begining of code for debugging
#https://wiki.blender.org/index.php/Dev:Doc/Tools/Debugging/Python_Eclipse
#make this match your current installation
try:
    PYDEV_SOURCE_DIR = "/usr/lib/eclipse/plugins/org.python.pydev_5.6.0.201703221358/pysrc"
    import sys
    if PYDEV_SOURCE_DIR not in sys.path:
        sys.path.append(PYDEV_SOURCE_DIR)
    import pydevd
    print("debugging enabled")
except:
    print("no debugging enabled")
#end code for debugging

#will create a breakpoint
#pydevd.settrace()

#the lcoation of this may need changed depending on which file you want to debug
from . import properties, panel, sockets, nodes, operators



class UMOGNodeTree(bpy.types.NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"
        
    def execute(self, refholder):
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
            insertNode(layout, "umog_GetTextureNode", "Texture")
            insertNode(layout, "umog_NoiseGenerationNode", "Noise Generator")
            insertNode(layout, "umog_Mat3Node", "Matrix 3x3")
            insertNode(layout, "umog_SculptNode", "Sculpt Node")
            insertNode(layout, "umog_ModifierNode", "Modifier Node")
            insertNode(layout, "umog_BMeshNode", "BMesh Node")
            insertNode(layout, "umog_BMeshCurlNode", "BMesh Curl Node")
            insertNode(layout, "umog_SculptNDNode", "Sculpt ND Node")

def register():
    print("begin resitration")
    # see for types to register https://docs.blender.org/api/2.78b/bpy.utils.html?highlight=register_class#bpy.utils.register_class
    bpy.types.NODE_MT_add.append(drawMenu)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)
    bpy.utils.unregister_module(__name__)
    
