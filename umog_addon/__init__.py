import bpy
import sys
from bpy.types import NodeTree, Node, NodeSocket
import mathutils

# begining of code for debugging
# https://wiki.blender.org/index.php/Dev:Doc/Tools/Debugging/Python_Eclipse
# make this match your current installation
# try:
#     PYDEV_SOURCE_DIR = "/usr/lib/eclipse/dropins/pydev/plugins/org.python.pydev_5.8.0.201706061859/pysrc"
#     import sys
#     if PYDEV_SOURCE_DIR not in sys.path:
#         sys.path.append(PYDEV_SOURCE_DIR)
#     import pydevd
#     print("debugging enabled")
# except:
#     print("no debugging enabled")
# end code for debugging

# will create a breakpoint
# pydevd.settrace()

# the lcoation of this may need changed depending on which file you want to debug
from . import properties, panel, sockets, nodes, operators


class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    def execute(self, refholder):
        print('Executing node tree')


menus = {
    "mesh_menu": {
        "bl_idname": "umog_mesh_menu",
        "bl_label": "Mesh Menu",
        "text": "Mesh",
        "bl_description": "Lorem Ipsum",
        "icon": "MESH_DATA",
        "nodes": [
            ("umog_SculptNode", "Sculpt Dynamic Node"),
            ("umog_SculptNDNode", "Sculpt Static Node"),
            ("umog_DisplaceNode", "Displace Node")
        ]
    },
    "texture_menu": {
        "bl_idname": "umog_texture_menu",
        "bl_label": "Texture Menu",
        "text": "Texture",
        "bl_description": "Lorem Ipsum",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("umog_GetTextureNode", "Get Texture"),
            ("umog_SetTextureNode", "Set Texture"),
            ("umog_SaveTextureNode", "Save Texture"),
            ("umog_TextureAlternatorNode", "Texture Alternator")
        ]
    },
    "object_menu": {
        "bl_idname": "umog_object_menu",
        "bl_label": "Object Menu",
        "text": "Object",
        "bl_description": "Lorem Ipsum",
        "icon": "OBJECT_DATAMODE",
        "nodes": [
            ("", "")
        ]
    },
    "math_menu": {
        "bl_idname": "umog_math_menu",
        "bl_label": "Math Menu",
        "text": "Math",
        "bl_description": "Lorem Ipsum",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("umog_IntegerNode", "Integer"),
            ("umog_IntegerFrameNode", "Integer Frame"),
            ("umog_IntegerSubframeNode", "Integer Subframe"),
            ("umog_IntegerMathNode", "Integer Math")
        ]
    },
    "algorithm_menu": {
        "bl_idname": "umog_algorithm_menu",
        "bl_label": "Algorithm Menu",
        "text": "Algorithm",
        "bl_description": "Lorem Ipsum",
        "icon": "STICKY_UVS_LOC",
        "nodes": [
            ("umog_ReactionDiffusionNode", "Reaction Diffusion Node")
        ]
    }
}


def UMOGCreateMenus():
    for key in menus:
        menu = menus[key]

        def draw(self, context):
            layout = self.layout
            for node in self.menu["nodes"]:
                insertNode(layout, node[0], node[1])

        menu_class = type(
            "UMOGMenu%s" % menu["text"],
            (bpy.types.Menu,),
            {
                "menu": menu,
                "bl_idname": menu["bl_idname"],
                "bl_label": menu["bl_label"],
                "bl_description": menu["bl_description"],
                "draw": draw
            },
        )
        bpy.utils.register_class(menu_class)


UMOGCreateMenus()


def drawMenu(self, context):
    if context.space_data.tree_type != "umog_UMOGNodeTree": return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"
    for key in menus:
        menu = menus[key]
        layout.menu(menu["bl_idname"], text=menu["text"], icon=menu["icon"])


# from animation nodes
def insertNode(layout, type, text, settings={}, icon="NONE"):
    operator = layout.operator("node.add_node", text=text, icon=icon)
    operator.type = type
    operator.use_transform = True
    for name, value in settings.items():
        item = operator.settings.add()
        item.name = name
        item.value = value
    return operator


def register():
    bpy.types.NODE_MT_add.append(drawMenu)


def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)

