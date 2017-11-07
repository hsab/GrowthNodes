import bpy
from collections import OrderedDict

menus = OrderedDict([
    ("algorithm_menu", {
        "bl_idname": "umog_algorithm_menu",
        "bl_label": "Algorithm Menu",
        "text": "Algorithm",
        "bl_description": "Lorem Ipsum",
        "icon": "STICKY_UVS_LOC",
        "nodes": [
            #("umog_ReactionDiffusionNode", "Reaction Diffusion Node"),
            ("umog_ReactionDiffusionBGLNode", "Reaction Diffusion Node"),
            ("umog_PyGLNode", "3d Reaction Diffusion"),
            #("umog_ReactionDiffusionNode", "Reaction Diffusion Node"),
            ("umog_ReactionDiffusionBGLNode", "Reaction Diffusion GPU"),
            ("umog_ConvolveNode", "Convolve")
        ]
    }),
    (" ", "separator"),
    ("develop_menu", {
        "bl_idname": "umog_develop_menu",
        "bl_label": "Develop Menu",
        "text": "Develop",
        "bl_description": "Lorem Ipsum",
        "icon": "RECOVER_AUTO",
        "nodes": [
            ("umog_MotherNode", "Mother Node"),
            ("umog_ScriptNode", "Script Node")
        ]
    }),
    ("object_menu", {
        "bl_idname": "umog_object_menu",
        "bl_label": "Object Menu",
        "text": "Object",
        "bl_description": "Lorem Ipsum",
        "icon": "MESH_CUBE",
        "nodes": [
            ("umog_ObjectNode", "Object"),
            ("umog_ObjectAlternatorNode", "Object Alternator")
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
            ("umog_DisplaceNode", "Displace"),
            ("umog_DissolveDegenerateNode", "Dissolve Degenerate"),
            ("umog_DissolveLimitedNode", "Dissolve Limited"),
            ("umog_SubdivideNode", "Subdivide"),
            ("umog_SharpEdgesNode", "Sharp Edges"),
            ("umog_SharpFacesNode", "Sharp Faces")
        ]
    }),
    ("  ", "separator"),
    ("integer_menu", {
        "bl_idname": "umog_integer_menu",
        "bl_label": "Integer Menu",
        "text": "Integer",
        "bl_description": "Nodes that operate on integers",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("umog_IntegerNode", "Integer"),
            ("umog_IntegerMathNode", "Integer Math"),
            ("umog_IntegerCompareNode", "Integer Compare"),
            ("umog_IntegerFrameNode", "Integer Frame"),
            ("umog_IntegerSubframeNode", "Integer Subframe")
        ]
    }),
    ("float_menu", {
        "bl_idname": "umog_float_menu",
        "bl_label": "Float Menu",
        "text": "Float",
        "bl_description": "Lorem Ipsum",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("umog_FloatNode", "Float"),
            ("umog_FloatMathNode", "Float Math"),
            ("umog_FloatCompareNode", "Float Compare")
        ]
    }),
    ("boolean_menu", {
        "bl_idname": "umog_boolean_menu",
        "bl_label": "Boolean Menu",
        "text": "Boolean",
        "bl_description": "Lorem Ipsum",
        "icon": "CLIPUV_DEHLT",
        "nodes": [
            ("umog_BooleanNode", "Boolean"),
            ("umog_BooleanOpshNode", "Boolean Operations")
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
            ("umog_TextureNode", "Texture"),
            ("umog_TextureColorsNode", "Texture Colors"),
            ("umog_TextureSettingsNode", "Texture Settings"),
            ("umog_TextureAlternatorNode", "Texture Alternator"),
            ("umog_SaveTextureNode", "Texture Save")
        ]
    }),
        ("texture3d_menu", {
        "bl_idname": "umog_texture3d_menu",
        "bl_label": "Texture 3d Menu",
        "text": "Texture3",
        "bl_description": "",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("umog_Texture3ShapeNode", "Shapes"),
            ("umog_Texture3LatheNode", "Lathe"),
            ("umog_Texture3SolidGeometryNode", "Solid Geometry"),
            ("umog_SaveTexture3dNode", "Save Texture Slices"),
            ("umog_Texture3TransformNode", "Transform"),
            ("umog_Texture3MeshNode", "Convert To Mesh"),
        ]
    })
])# yapf: disable

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
                (bpy.types.Menu, ),
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
            layout.menu(menu["bl_idname"], text = menu["text"], icon = menu["icon"])
        else:
            layout.separator()


def insertNode(layout, type, text, settings = {}, icon = "NONE"):
    operator = layout.operator("node.add_node", text = text, icon = icon)
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
