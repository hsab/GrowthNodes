import bpy
from bpy.types import NodeTree
from bpy.props import *
from .. utils.debug import *
from .. utils.handlers import eventUMOGHandler
from collections import defaultdict


class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    linearizedNodes = []
    unlinkedNodes = []
    connectedComponents = 0

    def updateTimeInfo(self, context):
        if self.StartFrame >= self.EndFrame:
            self.StartFrame = self.EndFrame - 1
        if self.EndFrame <= self.StartFrame:
            self.EndFrame = self.StartFrame + 1

        res = self.TextureResolution
        isResPowerOfTwo = (res != 0 and ((res & (res - 1)) == 0))

        if not isResPowerOfTwo:
            self.TextureResolution = 2**(self.TextureResolution -
                                         1).bit_length()

    bakeCount = IntProperty(
        name="BakeCount",
        description="BakeCount",
        default=1,
        min=1,
        update=updateTimeInfo)

    StartFrame = IntProperty(
        name="StartFrame",
        description="StartFrame",
        default=1,
        min=1,
        update=updateTimeInfo)

    EndFrame = IntProperty(
        name="EndFrame",
        description="EndFrame",
        default=2,
        min=2,
        update=updateTimeInfo)

    SubFrames = IntProperty(
        name="SubFrames",
        description="SubFrames",
        default=1,
        min=1)

    TextureResolution = IntProperty(
        name="TextureResolution",
        description="TextureResolution",
        default=256,
        min=64,
        update=updateTimeInfo)

    updateInProgress = BoolProperty(
        name="Is an update in progress?", default=False)

    def update(self):
        self.refreshExecutionPolicy()
        self.updateFrom()

    def updateOnFrameChange(self):
        for node in self.nodes:
            try:
                node.refreshOnFrameChange()
            except:
                pass

    def updateFrom(self, node=None):
        if not self.updateInProgress:
            print(self.connectedComponents)
            self.updateInProgress = True

            if node is None:
                for node in self.linearizedNodes:
                    node.refreshNode()

                if len(self.linearizedNodes) > 0:
                    DBG("ALL EXECUTABLE NODES REFRESHED:",
                        *self.linearizedNodes, TRACE=False)
            else:
                index = self.linearizedNodes.index(node)
                currentCC = node.execution.connectedComponent
                nodesToBeUpdated = []
                for node in self.linearizedNodes[index:]:
                    if node.execution.connectedComponent == currentCC:
                        nodesToBeUpdated.append(node)

                if len(self.linearizedNodes) > 0:
                    DBG("FOLLOWING EXECUTABLE NODES REFRESHED:",
                        *nodesToBeUpdated, TRACE=False)

                for node in nodesToBeUpdated:
                    node.refreshNode()

            self.updateInProgress = False

    def updateUnlinkedNodesSocketNames(self):
        for node in self.unlinkedNodes:
            for socket in node.sockets:
                socket.reverseName()

    def refreshExecutionPolicy(self):
        self.markUnvisited()
        self.connectedComponent()
        self.markUnvisited()
        self.topologicalSort()
        self.markUnvisited()
        self.updateNodeColors()

    def markUnvisited(self):
        for node in self.nodes:
            node.execution.visited = False

    def topologicalSort(self):
        del self.linearizedNodes[:]
        del self.unlinkedNodes[:]

        for node in self.nodes:
            if node.isLinked is False:
                self.unlinkedNodes.append(node)
            elif node.execution.visited is False:
                self.topologicalSortUtil(node)

    def topologicalSortUtil(self, node):
        node.execution.visited = True

        for socket in node.outputs:
            connectedNodes = socket.getConnectedNodes
            for adjacentNode in connectedNodes:
                if adjacentNode.execution.visited == False:
                    self.topologicalSortUtil(adjacentNode)

        self.linearizedNodes.insert(0, node)

    def connectedComponent(self):
        connectedComponent = 1
        for node in self.nodes:
            if node.isLinked is False:
                node.execution.connectedComponent = -1
            elif node.execution.visited is False:
                self.connectedComponentUtil(node, connectedComponent)
                connectedComponent += 1

        self.connectedComponents = connectedComponent

    def connectedComponentUtil(self, node, connectedComponent):
        node.execution.visited = True
        node.execution.connectedComponent = connectedComponent

        for socket in node.sockets:
            connectedNodes = socket.getConnectedNodes
            for adjacentNode in connectedNodes:
                if adjacentNode.execution.visited == False:
                    self.connectedComponentUtil(
                        adjacentNode, connectedComponent)

    def updateNodeColors(self):
        for node in self.unlinkedNodes:
            node.enableUnlinkedHighlight()
        for node in self.linearizedNodes:
            node.disableUnlinkedHighlight()

    def execute(self, refholder):

        nodes = self.topological_sort()

        # for node in nodes:
        # node.preExecute(refholder)
        # if write_keyframes and node._IsUMOGOutputNode:
        # node.write_keyframe(refholder, start_frame)

        # TODO: fix draw, possible different execution mechanism
        # TODO: separate refresh and execute
        # TODO:
        for frame in range(self.StartFrame, self.EndFrame):
            bpy.context.scene.frame_current = frame
            for sub_frame in range(0, self.SubFrames):
                for node in nodes:
                    node.refreshNode()
                    node.execute(refholder)

        self.bakeCount = self.bakeCount + 1
        # for node in nodes:
        #     node.postFrame(refholder)
        #     if write_keyframes and node._IsUMOGOutputNode:
        #         node.write_keyframe(refholder, frame)

        # for node in nodes:
        #     node.postBake(refholder)

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
