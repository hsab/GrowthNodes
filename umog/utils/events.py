import bpy
from . debug import *
from bpy.app.handlers import persistent

def propUpdate(self = None, context = None):

    def nodeTreeUpdateFrom(node):
        if node in node.nodeTree.linearizedNodes:
            node.nodeTree.updateFrom(node)

    if context is not None:
        #  Property changed from socket
        if hasattr(self, 'isUMOGNodeSocket'):
            if self.isUMOGNodeSocket:
                if not self.socketRecentlyRefreshed:
                    # DBG("PROPERTY CHANGED FROM SOCKET:",
                    #     "Type:   "+self.dataType,
                    #     "Name:   "+self.name,
                    #     "Path:   "+self.path_from_id(),
                    #     trace = True)

                    nodeTreeUpdateFrom(self.node)
                else:
                    self.socketRecentlyRefreshed = False
                    
        # Property changed from node
        elif hasattr(self, 'isUMOGNode'):
            if self.isUMOGNode:
                nodeTreeUpdateFrom(self)


@persistent
def updateOnLoad(scene):
    for area in bpy.context.screen.areas:
        if area.type == "NODE_EDITOR":
            tree = area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                tree.update()

@persistent
def updateOnFrameChange(scene):
    for area in bpy.context.screen.areas:
        if area.type == "NODE_EDITOR":
            tree = area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                tree.updateOnFrameChange()

def register():
    bpy.app.handlers.load_post.append(updateOnLoad)
    bpy.app.handlers.frame_change_post.append(updateOnFrameChange)

def unregister():
    bpy.app.handlers.load_post.remove(updateOnLoad)
    bpy.app.handlers.frame_change_post.remove(updateOnFrameChange)
