import bpy
from bpy.props import *

def register():
    bpy.types.Context.getActiveUMOGNodeTree = getActiveUMOGNodeTree

def unregister():
    del bpy.types.Context.getActiveUMOGNodeTree
    del bpy.types.Mesh.an
    del bpy.types.Object.an
    del bpy.types.ID.umog_data

def getActiveUMOGNodeTree(context):
    if context.area.type == "NODE_EDITOR":
        tree = context.space_data.node_tree
        if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
            return tree
