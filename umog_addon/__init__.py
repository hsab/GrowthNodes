import bpy
from bpy.types import NodeTree

class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    def execute(self, refholder):
        print('Executing node tree')

from collections import OrderedDict

menus = OrderedDict([
    ("algorithm_menu", {
        "bl_idname": "umog_algorithm_menu",
        "bl_label": "Algorithm Menu",
        "text": "Algorithm",
        "bl_description": "Lorem Ipsum",
        "icon": "STICKY_UVS_LOC",
        "nodes": [
            ("umog_ReactionDiffusionNode", "Reaction Diffusion Node"),
            ("umog_ConvolveNode", "Convolve")
        ]
    }),
    (" ", "separator"),
    ("object_menu", {
        "bl_idname": "umog_object_menu",
        "bl_label": "Object Menu",
        "text": "Object",
        "bl_description": "Lorem Ipsum",
        "icon": "OUTLINER_OB_GROUP_INSTANCE",
        "nodes": [
            ("", "")
        ]
    }),
    ("bmesh_menu", {
        "bl_idname": "umog_bmesh_menu",
        "bl_label": "Bmesh Menu",
        "text": "Bmesh",
        "bl_description": "Lorem Ipsum",
        "icon": "SURFACE_NSPHERE",
        "nodes": [
            ("umog_BMeshNode", "Bmesh Node"),
            ("umog_BMeshCurlNode", "Bmesh Curl Node")
        ]
    }),
    ("geometry_menu", {
        "bl_idname": "umog_geometry_menu",
        "bl_label": "Geometry Menu",
        "text": "Geometry",
        "bl_description": "Lorem Ipsum",
        "icon": "MESH_UVSPHERE",
        "nodes": [
            ("umog_SculptNode", "Sculpt Dynamic Node"),
            ("umog_SculptNDNode", "Sculpt Static Node"),
            ("umog_DisplaceNode", "Displace Node")
        ]
    }),
    ("  ", "separator"),
    ("integer_menu", {
        "bl_idname": "umog_integer_menu",
        "bl_label": "Integer Menu",
        "text": "Integer",
        "bl_description": "Lorem Ipsum",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("umog_IntegerNode", "Integer"),
            ("umog_IntegerFrameNode", "Integer Frame"),
            ("umog_IntegerSubframeNode", "Integer Subframe"),
            ("umog_IntegerMathNode", "Integer Math")
        ]
    }),
    ("matrix_menu", {
        "bl_idname": "umog_matrix_menu",
        "bl_label": "Matrix Menu",
        "text": "Matrix",
        "bl_description": "Lorem Ipsum",
        "icon": "MESH_GRID",
        "nodes": [
            ("umog_Mat3Node", "Matrix 3x3 Node"),
            ("umog_MatrixMathNode", "Matrix Math"),
            ("umog_GaussNode", "Gaussian Blur"),
            ("umog_LaplaceNode", "Laplacian Filter")
        ]
    }),
    ("  ", "separator"),
    ("texture_menu", {
        "bl_idname": "umog_texture_menu",
        "bl_label": "Texture Menu",
        "text": "Texture",
        "bl_description": "Lorem Ipsum",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("umog_GetTextureNode", "Get Texture"),
            ("umog_SetTextureNode", "Set Texture"),
            ("umog_SaveTextureNode", "Save Texture"),
            ("umog_LoadTextureNode", "Load Texture(s)"),
            ("umog_TextureAlternatorNode", "Texture Alternator")
            
        ]
    })
])

def UMOGCreateMenus():
    for key, value in menus.items():
        if value is not "separator":
            menu = value

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
    for key, value in menus.items():
        menu = value
        if menu is not "separator":
            layout.menu(menu["bl_idname"], text=menu["text"], icon=menu["icon"])
        else:
            layout.separator()

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

