import bpy
from collections import OrderedDict

# menus from compile branch
menus = OrderedDict([
    ("  ", "separator"),
    ("mesh_menu", {
        "bl_idname": "umog_mesh_menu",
        "bl_label": "Mesh Menu",
        "text": "Mesh",
        "bl_description": "Nodes that deal with meshes",
        "icon": "MESH_UVSPHERE",
        "nodes": [
            ("umog_GetMeshNode", "Get Mesh"),
            ("umog_SetMeshNode", "Set Mesh"),
            ("umog_DisplaceNode", "Displace"),
            ("umog_IteratedDisplaceNode", "Iterated Displace"),
        ]
    }),
    ("sound_menu", {
        "bl_idname": "umog_sound_menu",
        "bl_label": "Sound Menu",
        "text": "Sound",
        "bl_description": "Nodes that operate on Sounds",
        "icon": "SOUND",
        "nodes": [
            ("umog_LoadAudioNode", "Load Audio"),
            ("umog_SaveAudioNode", "Save Audio"),
            ("umog_STFTNode", "Short-Time Fourier Transform")
        ]
    }),
    ("texture_menu", {
        "bl_idname": "umog_texture_menu",
        "bl_label": "Texture Menu",
        "text": "Texture",
        "bl_description": "Lorem Ipsum",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("umog_GetTextureNode", "Get Texture"),
            ("umog_GetVolumetricTextureNode", "Get Volumetric Texture"),
            ("umog_SetTextureNode", "Set Texture"),
            ("umog_SaveTextureNode", "Save Texture"),
            ("umog_LoadTextureNode", "Load Texture(s)"),
        ]
    }),
    (" ", "separator"),
    ("math_menu", {
        "bl_idname": "umog_math_menu",
        "bl_label": "Math Menu",
        "text": "Math",
        "bl_description": "",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("umog_NumberNode", "Number"),
            ("umog_AddNode", "Add"),
            ("umog_SubtractNode", "Subtract"),
            ("umog_MultiplyNode", "Multiply"),
            ("umog_DivideNode", "Divide"),
            ("umog_NegateNode", "Negate"),
            ("umog_PowerNode", "Power"),
            ("umog_ModulusNode", "Modulus"),
            ("umog_TimeSequenceNode", "Time Sequence"),
        ]
    }),
    ("comparison_menu", {
        "bl_idname": "umog_comparison_menu",
        "bl_label": "Comparison Menu",
        "text": "Comparison",
        "bl_description": "",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("umog_EqualNode", "Equal"),
            ("umog_NotEqualNode", "Not Equal"),
            ("umog_LessThanNode", "Less Than"),
            ("umog_GreaterThanNode", "Greater Than"),
            ("umog_LessThanOrEqualNode", "Less Than or Equal"),
            ("umog_GreaterThanOrEqualNode", "Greater Than or Equal"),
        ]
    }),
    ("boolean_menu", {
        "bl_idname": "umog_boolean_menu",
        "bl_label": "Boolean Menu",
        "text": "Boolean",
        "bl_description": "",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("umog_BooleanNode", "Boolean"),
            ("umog_NotNode", "Not"),
            ("umog_AndNode", "And"),
            ("umog_OrNode", "Or"),
            ("umog_XorNode", "Xor"),
        ]
    }),
    ("matrix_menu", {
        "bl_idname": "umog_matrix_menu",
        "bl_label": "Matrix Menu",
        "text": "Matrix",
        "bl_description": "Lorem Ipsum",
        "icon": "MESH_GRID",
        "nodes": [
            ("umog_Matrix3x3Node", "3x3 Matrix"),
            ("umog_MultiplyMatrixMatrixNode", "Matrix * Matrix"),
            ("umog_MultiplyMatrixVectorNode", "Matrix * Vector"),
            ("umog_MatrixInverseNode", "Inverse"),
            ("umog_MatrixTransposeNode", "Transpose"),
            ("umog_MatrixDeterminantNode", "Determinant"),
            ("umog_MatrixNormNode", "Norm"),
            ("umog_GaussNode", "Gaussian Blur"),
            ("umog_LaplaceNode", "Laplacian Filter"),
            ("umog_ConvolveNode", "Convolve"),
        ]
    }),
    ("algorithm_menu", {
        "bl_idname": "umog_algorithm_menu",
        "bl_label": "Algorithm Menu",
        "text": "Algorithm",
        "bl_description": "Lorem Ipsum",
        "icon": "STICKY_UVS_LOC",
        "nodes": [
            ("umog_ReactionDiffusionNode", "Reaction Diffusion"),
            ("umog_ReactionDiffusionBGLNode", "Reaction Diffusion GPU"),
            ("umog_PyGLNode", "3d Reaction Diffusion"),
        ]
    }),
    ("   ", "separator"),
    ("debug_menu", {
        "bl_idname": "umog_debug_menu",
        "bl_label": "Debug Menu",
        "text": "Debug",
        "bl_description": "Nodes for debugging",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("umog_PrintNode", "Print"),
            ("umog_ShowNumberNode", "Show Number"),
        ]
    })
])# yapf: disable

# menus from master branch
# menus = OrderedDict([
#     ("algorithm_menu", {
#         "bl_idname": "umog_algorithm_menu",
#         "bl_label": "Algorithm Menu",
#         "text": "Algorithm",
#         "bl_description": "Lorem Ipsum",
#         "icon": "STICKY_UVS_LOC",
#         "nodes": [
#             #("umog_ReactionDiffusionNode", "Reaction Diffusion Node"),
#             ("umog_ReactionDiffusionBGLNode", "Reaction Diffusion Node"),
#             ("umog_PyGLNode", "3d Reaction Diffusion"),
#             #("umog_ReactionDiffusionNode", "Reaction Diffusion Node"),
#             ("umog_ReactionDiffusionBGLNode", "Reaction Diffusion GPU"),
#             ("umog_ConvolveNode", "Convolve")
#         ]
#     }),
#     (" ", "separator"),
#     ("develop_menu", {
#         "bl_idname": "umog_develop_menu",
#         "bl_label": "Develop Menu",
#         "text": "Develop",
#         "bl_description": "Lorem Ipsum",
#         "icon": "RECOVER_AUTO",
#         "nodes": [
#             ("umog_MotherNode", "Mother Node"),
#             ("umog_ScriptNode", "Script Node")
#         ]
#     }),
#     ("object_menu", {
#         "bl_idname": "umog_object_menu",
#         "bl_label": "Object Menu",
#         "text": "Object",
#         "bl_description": "Lorem Ipsum",
#         "icon": "MESH_CUBE",
#         "nodes": [
#             ("umog_ObjectNode", "Object"),
#             ("umog_ObjectAlternatorNode", "Object Alternator")
#         ]
#     }),
#     ("geometry_menu", {
#         "bl_idname": "umog_geometry_menu",
#         "bl_label": "Geometry Menu",
#         "text": "Geometry",
#         "bl_description": "Lorem Ipsum",
#         "icon": "MESH_UVSPHERE",
#         "nodes": [
#             ("umog_DisplaceNode", "Displace"),
#             ("umog_DissolveDegenerateNode", "Dissolve Degenerate"),
#             ("umog_DissolveLimitedNode", "Dissolve Limited"),
#             ("umog_SubdivideNode", "Subdivide"),
#             ("umog_SharpEdgesNode", "Sharp Edges"),
#             ("umog_SharpFacesNode", "Sharp Faces")
#         ]
#     }),
#     ("  ", "separator"),
#     ("math_menu", {
#         "bl_idname": "umog_math_menu",
#         "bl_label": "Math Menu",
#         "text": "Math",
#         "bl_description": "",
#         "icon": "LINENUMBERS_ON",
#         "nodes": [
#             ("umog_IntegerNode", "Integer"),
#             ("umog_IntegerMathNode", "Integer Math"),
#             ("umog_IntegerCompareNode", "Integer Compare"),
#             ("umog_IntegerFrameNode", "Integer Frame"),
#             ("umog_IntegerSubframeNode", "Integer Subframe")
#         ]
#     }),
#     ("float_menu", {
#         "bl_idname": "umog_float_menu",
#         "bl_label": "Float Menu",
#         "text": "Float",
#         "bl_description": "Lorem Ipsum",
#         "icon": "LINENUMBERS_ON",
#         "nodes": [
#             ("umog_FloatNode", "Float"),
#             ("umog_FloatMathNode", "Float Math"),
#             ("umog_FloatCompareNode", "Float Compare")
#         ]
#     }),
#     ("boolean_menu", {
#         "bl_idname": "umog_boolean_menu",
#         "bl_label": "Boolean Menu",
#         "text": "Boolean",
#         "bl_description": "Lorem Ipsum",
#         "icon": "CLIPUV_DEHLT",
#         "nodes": [
#             ("umog_BooleanNode", "Boolean"),
#             ("umog_BooleanOpshNode", "Boolean Operations")
#         ]
#     }),
#     ("matrix_menu", {
#         "bl_idname": "umog_matrix_menu",
#         "bl_label": "Matrix Menu",
#         "text": "Matrix",
#         "bl_description": "Lorem Ipsum",
#         "icon": "MESH_GRID",
#         "nodes": [
#             ("umog_Mat3Node", "Matrix 3x3 Node"),
#             ("umog_MatrixMathNode", "Matrix Math"),
#             ("umog_GaussNode", "Gaussian Blur"),
#             ("umog_LaplaceNode", "Laplacian Filter"),
#         ]
#     }),
#     ("  ", "separator"),
#     ("texture_menu", {
#         "bl_idname": "umog_texture_menu",
#         "bl_label": "Texture Menu",
#         "text": "Texture",
#         "bl_description": "Lorem Ipsum",
#         "icon": "IMGDISPLAY",
#         "nodes": [
#             ("umog_TextureNode", "Texture"),
#             ("umog_TextureAlternatorNode", "Texture Alternator"),
#             ("umog_SaveTextureNode", "Texture Save")
#         ]
#     }),
#         ("texture3d_menu", {
#         "bl_idname": "umog_texture3d_menu",
#         "bl_label": "Texture 3d Menu",
#         "text": "Texture3",
#         "bl_description": "",
#         "icon": "IMGDISPLAY",
#         "nodes": [
#             ("umog_Texture3ShapeNode", "Shapes"),
#             ("umog_Texture3LatheNode", "Lathe"),
#             ("umog_Texture3SolidGeometryNode", "Solid Geometry"),
#             ("umog_SaveTexture3dNode", "Save Texture Slices"),
#             ("umog_Texture3TransformNode", "Transform"),
#             ("umog_Texture3MeshNode", "Convert To Mesh"),
#         ]
#     }),
#     ("  ", "separator"),
#     ("debug_menu", {
#         "bl_idname": "umog_debug_menu",
#         "bl_label": "Debug Menu",
#         "text": "Debug",
#         "bl_description": "Nodes for debugging",
#         "icon": "IMGDISPLAY",
#         "nodes": [
#             ("umog_PrintNode", "Print"),
#             ("umog_ShowNumberNode", "Show Number"),
#         ]
#     })
# ])# yapf: disable


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
