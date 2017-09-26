import bpy
from bpy.types import NodeTree
from .. utils.debug import *
from .. utils.handlers import eventUMOGHandler

from collections import defaultdict

class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    linearizedNodes = []
    unlinkedNodes = []

    def update(self):
        self.refreshExecutionPolicy()
        self.updateFrom()

    def updateFrom(self, node = None):
        if node is None:
            DBG("ALL EXECUTABLE NODES REFRESHED:", *self.linearizedNodes, TRACE = False)
            for node in self.linearizedNodes:
                node.refresh()
        else:
            index = self.linearizedNodes.index(node)
            subgraph = node.sortSubgraph
            DBG_list = []
            for node in self.linearizedNodes[index:]:
                if node.sortSubgraph == subgraph:
                    DBG_list.append(node)
                    node.refresh()
            DBG("FOLLOWING EXECUTABLE NODES REFRESHED:", *DBG_list, TRACE = False)

    def refreshExecutionPolicy(self):
        self.topologicalSort()
        self.updateNodeColors()

    def execute(self, refholder, start_frame, end_frame, sub_frames, write_keyframes=False):
        print('Executing node tree')

        nodes = self.topological_sort()
        
        for node in nodes:
            node.preExecute(refholder)
            if write_keyframes and node._IsUMOGOutputNode:
                node.write_keyframe(refholder, start_frame)

        for frame in range(start_frame + 1, end_frame + 1):
            for sub_frame in range(0, sub_frames):
                for node in nodes:
                    node.execute(refholder)

            for node in nodes:
                node.postFrame(refholder)
                if write_keyframes and node._IsUMOGOutputNode:
                    node.write_keyframe(refholder, frame)

        for node in nodes:
            node.postBake(refholder)

    def updateNodeColors(self):
        for node in self.unlinkedNodes:
            node.enableUnlinkedHighlight()
        for node in self.linearizedNodes:
            node.disableUnlinkedHighlight()

    # A recursive function used by topologicalSort
    def topologicalSortUtil(self, node, subgraph):
        # Mark the current node as visited.
        node.sortVisited = True
        node.sortSubgraph = subgraph
        # Recur for all the nodes adjacent to this node
        for socket in node.outputs:
            connectedNodes = socket.getConnectedNodes
            for adjacentNode in connectedNodes:
                if adjacentNode.sortVisited == False:
                    self.topologicalSortUtil(adjacentNode, subgraph)
                else:
                    node.sortSubgraph = adjacentNode.sortSubgraph

        # Push current vertex to stack which stores result
        self.linearizedNodes.insert(0,node)

    # The function to do Topological Sort. It uses recursive 
    # topologicalSortUtil()
    def topologicalSort(self):
        del self.linearizedNodes[:]
        del self.unlinkedNodes[:]
        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        subgraph = 1
        for node in self.nodes:
            if node.hasLinks is False:
                node.sortSubgraph = 0
                self.unlinkedNodes.append(node)
            elif node.sortVisited is False:
                self.topologicalSortUtil(node, subgraph)
                subgraph += 1

        for node in self.nodes:
            node.sortVisited = False

    def topological_sort(self):
        stack = []
        nodes = []
        visited = defaultdict(lambda: False)

        # initialize stack with output nodes
        for node in self.nodes:
            if node._IsUMOGOutputNode:
                stack.append(node)
                nodes.append(node)
                visited[node.name] = True

        # perform a breadth-first traversal of the node graph
        while len(stack) > 0:
            node = stack.pop()
            for input in node.inputs:
                for link in input.links:
                    if not visited[link.from_node.name]:
                        stack.append(link.from_node)
                        nodes.append(link.from_node)
                        visited[link.from_node.name] = True

        return nodes

@eventUMOGHandler("FILE_LOAD_POST")
def updateOnLoad():
    for area in bpy.context.screen.areas:
        if area.type == "NODE_EDITOR":
            tree = area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                tree.refreshExecutionPolicy()