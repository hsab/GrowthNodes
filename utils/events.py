import bpy
from .handlers import eventUMOGHandler
from . debug import *
from . nodes import getUMOGNodeTree

@eventUMOGHandler("FILE_LOAD_POST")
def updateOnLoad():
    for area in bpy.context.screen.areas:
        if area.type == "NODE_EDITOR":
            tree = area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                tree.update()

@eventUMOGHandler("FRAME_CHANGE_POST")
def updateOnFrameChange(scene):
    for area in bpy.context.screen.areas:
        if area.type == "NODE_EDITOR":
            tree = area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                tree.updateOnFrameChange()

def propUpdate(self = None, context = None):

    def nodeTreeUpdateFrom(node):
        if node in node.nodeTree.linearizedNodes:
            node.nodeTree.updateFrom(node)


    enableUseFakeUser()
    
    if context is not None:
        #  Property changed from socket
        if hasattr(self, 'isUMOGNodeSocket'):
            if self.isUMOGNodeSocket:
                if not self.socketRecentlyRefreshed:
                    DBG("PROPERTY CHANGED FROM SOCKET:",
                        "Type:   "+self.dataType,
                        "Name:   "+self.name,
                        "Path:   "+self.path_from_id(),
                        trace = True)

                    nodeTreeUpdateFrom(self.node)
                else:
                    self.socketRecentlyRefreshed = False
                    
        # Property changed from node
        elif hasattr(self, 'isUMOGNode'):
            if self.isUMOGNode:
                nodeTreeUpdateFrom(self)

def enableUseFakeUser():
    # Make sure the node trees will not be removed when closing the file.
    for tree in getUMOGNodeTree():
        tree.use_fake_user = True