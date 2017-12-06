import bpy
from collections import OrderedDict

# menus from compile branch
menus = OrderedDict([
    ("algorithm_menu", {
        "bl_idname": "engine_algorithm_menu",
        "bl_label": "Algorithm Menu",
        "text": "Algorithm",
        "bl_description": "Lorem Ipsum",
        "icon": "STICKY_UVS_LOC",
        "nodes": [
            ("engine_ReactionDiffusionNode", "Reaction Diffusion"),
            ("engine_ReactionDiffusionGPUNode", "Reaction Diffusion GPU"),
            ("engine_ReactionDiffusionVoxelGPUNode", "Voxel Reaction Diffusion"),
        ]
    }),
    (" ", "separator"),
    ("mesh_menu", {
        "bl_idname": "engine_mesh_menu",
        "bl_label": "Mesh Menu",
        "text": "Mesh",
        "bl_description": "Nodes that deal with meshes",
        "icon": "MESH_UVSPHERE",
        "nodes": [
            ("engine_GetMeshNode", "Get Mesh"),
            ("engine_SetMeshNode", "Set Mesh"),
            ("engine_DisplaceNode", "Displace"),
            ("engine_IteratedDisplaceNode", "Iterated Displace"),
        ]
    }),
    ("texture_menu", {
        "bl_idname": "engine_texture_menu",
        "bl_label": "Texture Menu",
        "text": "Texture",
        "bl_description": "Lorem Ipsum",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("engine_GetTextureNode", "Get Texture"),
            ("engine_GetVolumetricTextureNode", "Get Volumetric Texture"),
            ("engine_SetTextureNode", "Set Texture"),
            ("engine_SaveTextureNode", "Save Texture"),
            ("engine_LoadTextureNode", "Load Texture(s)"),
            ("engine_Texture_Muxer_Node", "Mux Channels"),
        ]
    }),
    ("  ", "separator"),
    ("math_menu", {
        "bl_idname": "engine_math_menu",
        "bl_label": "Math Menu",
        "text": "Math",
        "bl_description": "",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("engine_NumberNode", "Number"),
            ("engine_AddNode", "Add"),
            ("engine_SubtractNode", "Subtract"),
            ("engine_MultiplyNode", "Multiply"),
            ("engine_DivideNode", "Divide"),
            ("engine_NegateNode", "Negate"),
            ("engine_PowerNode", "Power"),
            ("engine_ModulusNode", "Modulus"),
            ("engine_TimeSequenceNode", "Time Sequence"),
        ]
    }),
    ("comparison_menu", {
        "bl_idname": "engine_comparison_menu",
        "bl_label": "Comparison Menu",
        "text": "Comparison",
        "bl_description": "",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("engine_EqualNode", "Equal"),
            ("engine_NotEqualNode", "Not Equal"),
            ("engine_LessThanNode", "Less Than"),
            ("engine_GreaterThanNode", "Greater Than"),
            ("engine_LessThanOrEqualNode", "Less Than or Equal"),
            ("engine_GreaterThanOrEqualNode", "Greater Than or Equal"),
        ]
    }),
    ("boolean_menu", {
        "bl_idname": "engine_boolean_menu",
        "bl_label": "Boolean Menu",
        "text": "Boolean",
        "bl_description": "",
        "icon": "LINENUMBERS_ON",
        "nodes": [
            ("engine_BooleanNode", "Boolean"),
            ("engine_NotNode", "Not"),
            ("engine_AndNode", "And"),
            ("engine_OrNode", "Or"),
            ("engine_XorNode", "Xor"),
        ]
    }),
    ("matrix_menu", {
        "bl_idname": "engine_matrix_menu",
        "bl_label": "Matrix Menu",
        "text": "Matrix",
        "bl_description": "Lorem Ipsum",
        "icon": "MESH_GRID",
        "nodes": [
            ("engine_Matrix3x3Node", "3x3 Matrix"),
            ("engine_MultiplyMatrixMatrixNode", "Matrix * Matrix"),
            ("engine_MultiplyMatrixVectorNode", "Matrix * Vector"),
            ("engine_GaussNode", "Gaussian Blur"),
            ("engine_LaplaceNode", "Laplacian Filter"),
            ("engine_ConvolveNode", "Convolve"),
        ]
    }),
    ("texture3d_menu", {
        "bl_idname": "engine_texture3d_menu",
        "bl_label": "Voxel Menu",
        "text": "Voxel",
        "bl_description": "",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("engine_Texture3ShapeNode", "Shapes"),
            ("engine_Texture3LatheNode", "Lathe"),
            ("engine_Texture3SolidGeometryNode", "Solid Geometry"),
            ("engine_SaveTexture3dNode", "Save Texture Slices"),
            ("engine_Texture3TransformNode", "Transform"),
            ("engine_Texture3MeshNode", "Convert To Mesh"),
        ]
    }),
        
    ("   ", "separator"),
    ("debug_menu", {
        "bl_idname": "engine_debug_menu",
        "bl_label": "Debug Menu",
        "text": "Debug",
        "bl_description": "Nodes for debugging",
        "icon": "IMGDISPLAY",
        "nodes": [
            ("engine_PrintNode", "Print"),
            ("engine_ShowNumberNode", "Show Number"),
        ]
    })
])# yapf: disable

def EngineCreateMenus():
    for key, value in menus.items():
        if value is not "separator":
            menu = value

            def draw(self, context):
                layout = self.layout
                for node in self.menu["nodes"]:
                    insertNode(layout, node[0], node[1])

            menu_class = type(
                "EngineMenu%s" % menu["text"],
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


EngineCreateMenus()


def drawMenu(self, context):
    if context.space_data.tree_type != "engine_EngineNodeTree": return

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
