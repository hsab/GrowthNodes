import bpy
from bpy.props import *
from . operators.callbacks import executeCallback

def register():
    bpy.types.Context.getActiveUMOGNodeTree = getActiveUMOGNodeTree
    bpy.types.Operator.umog_executeCallback = _executeCallback
    # bpy.types.Mesh.an = PointerProperty(type = MeshProperties)
    # bpy.types.Object.an = PointerProperty(type = ObjectProperties)
    # bpy.types.ID.an_data = PointerProperty(type = IDProperties)

def unregister():
    del bpy.types.Context.getActiveUMOGNodeTree
    del bpy.types.Operator.umog_executeCallback
    del bpy.types.Mesh.an
    del bpy.types.Object.an
    del bpy.types.ID.umog_data

def getActiveUMOGNodeTree(context):
    if context.area.type == "NODE_EDITOR":
        tree = context.space_data.node_tree
        if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
            return tree

def _executeCallback(operator, callback, *args, **kwargs):
    executeCallback(callback, *args, **kwargs)