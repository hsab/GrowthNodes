import bpy
from .handlers import eventUMOGHandler
from . debug import *
@eventUMOGHandler("FILE_LOAD_POST")
def updateOnLoad():
    for area in bpy.context.screen.areas:
        if area.type == "NODE_EDITOR":
            tree = area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                tree.refreshExecutionPolicy()

def propUpdate(self = None, context = None):

    def nodeTreeUpdateFrom(node):
        if node in node.nodeTree.linearizedNodes:
            node.nodeTree.updateFrom(node)

    if context is not None:
        #  Property changed from socket
        if hasattr(self, 'isUMOGNodeSocket'):
            if self.isUMOGNodeSocket:
                if not self.wasRecentlyRefreshed:
                    DBG("PROPERTY CHANGED FROM SOCKET:",
                        "Type:   "+self.dataType,
                        "Name:   "+self.name,
                        "Path:   "+self.path_from_id(),
                        trace = True)

                    self.isDataModified = True
                    nodeTreeUpdateFrom(self.node)
                else:
                    self.wasRecentlyRefreshed = False
                    
        # Property changed from node
        elif hasattr(self, 'isUMOGNode'):
            if self.isUMOGNode:
                nodeTreeUpdateFrom(self.node)
