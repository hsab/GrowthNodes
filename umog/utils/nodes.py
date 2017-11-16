import bpy

def newNodeAtCursor(type):
    bpy.ops.node.add_and_link_node(type = type)
    return bpy.context.space_data.node_tree.nodes[-1]

def idToSocket(socketID):
    node = bpy.data.node_groups[socketID[0][0]].nodes[socketID[0][1]]
    identifier = socketID[2]
    sockets = node.outputs if socketID[1] else node.inputs
    for socket in sockets:
        if socket.identifier == identifier: return socket

def idToNode(nodeID):
    return bpy.data.node_groups[nodeID[0]].nodes[nodeID[1]]

def getUMOGNodeTree(skipLinkedTrees = True):
    umg_NodeTree = []
    for nodeTree in bpy.data.node_groups:
        if nodeTree.bl_idname != "umog_UMOGNodeTree": continue
        if skipLinkedTrees and nodeTree.library is not None: continue
        umg_NodeTree.append(nodeTree)
    return umg_NodeTree

def iterSubclassesWithAttribute(cls, attribute):
    for subcls in cls.__subclasses__():
        if hasattr(subcls, attribute):
            yield subcls
        else:
            yield from iterSubclassesWithAttribute(subcls, attribute)
