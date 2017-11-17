import bpy
from bpy.types import NodeTree
from bpy.props import *
from ..utils.debug import *
from collections import defaultdict

from ..engine import engine
import bpy
from bpy.types import NodeTree
from collections import defaultdict


class UMOGNodeTreeProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_NodeTreeProperties"
    unique = BoolProperty(default = False)
    editable = BoolProperty(default = False)
    variable = BoolProperty(default = False)

    def updateTimeInfo(self, context):
        if self.StartFrame >= self.EndFrame:
            self.StartFrame = self.EndFrame - 1
        if self.EndFrame <= self.StartFrame:
            self.EndFrame = self.StartFrame + 1

        res = self.TextureResolution
        isResPowerOfTwo = (res != 0 and ((res & (res - 1)) == 0))

        if not isResPowerOfTwo:
            self.TextureResolution = 2**(self.TextureResolution - 1).bit_length()

    StartFrame = IntProperty(name = "StartFrame", description = "StartFrame", default = 1,
                             min = 1, update = updateTimeInfo)

    EndFrame = IntProperty(name = "EndFrame", description = "EndFrame", default = 2,
                           min = 2, update = updateTimeInfo)

    SubFrames = IntProperty(name = "SubFrames", description = "SubFrames", default = 1,
                            min = 1)

    TextureResolution = IntProperty(name = "TextureResolution",
                                    description = "TextureResolution", default = 256,
                                    min = 64, update = updateTimeInfo)
    
    UniqueIDTracker = IntProperty(default=0)


class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    linearizedNodes = []
    unlinkedNodes = []
    connectedComponents = 0

    updateInProgress = BoolProperty(name = "Is an update in progress?", default = False)

    executeInProgress = BoolProperty(name = "Is an execution in progress?",
                                     default = False)

    properties = PointerProperty(type = UMOGNodeTreeProperties)

    def update(self):
        self.refreshExecutionPolicy()
        self.updateFrom()

    def updateOnFrameChange(self):
        for node in self.nodes:
            node.refreshOnFrameChange()

    def updateFrom(self, node = None):
        if not self.updateInProgress:
            self.updateInProgress = True

            if node is None:
                for node in self.linearizedNodes:
                    node.refreshNode()

                if len(self.linearizedNodes) > 0:
                    DBG("ALL EXECUTABLE NODES REFRESHED:", *self.linearizedNodes,
                        TRACE = False)
            else:
                index = self.linearizedNodes.index(node)
                currentCC = node.execution.connectedComponent
                nodesToBeUpdated = []
                for node in self.linearizedNodes[index:]:
                    if node.execution.connectedComponent == currentCC:
                        nodesToBeUpdated.append(node)

                if len(self.linearizedNodes) > 0:
                    DBG("FOLLOWING EXECUTABLE NODES REFRESHED:", *nodesToBeUpdated,
                        TRACE = False)

                for node in nodesToBeUpdated:
                    node.refreshNode()

            self.updateInProgress = False

    def getNextUniqueID(self):
        temp = self.properties.UniqueIDTracker
        self.properties.UniqueIDTracker = self.properties.UniqueIDTracker + 1
        return "__" + str(temp)

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
                    self.connectedComponentUtil(adjacentNode, connectedComponent)

    def updateNodeColors(self):
        for node in self.unlinkedNodes:
            node.enableUnlinkedHighlight()
        for node in self.linearizedNodes:
            node.disableUnlinkedHighlight()

    def execute(self, refholder):
        self.update()

        for node in self.linearizedNodes:
            node.packSockets()

        for node in self.linearizedNodes:
            node.preExecute(refholder)

        self.executeInProgress = True

        for frame in range(self.properties.StartFrame, self.properties.EndFrame):
            # Update the frame
            scene = bpy.context.scene
            scene.frame_set(frame)

            for sub_frame in range(0, self.properties.SubFrames):
                for node in self.linearizedNodes:
                    node.refreshNode()
                    node.execute(refholder)

            for node in self.linearizedNodes:
                node.postFrame(refholder)

        self.executeInProgress = False

        for node in self.linearizedNodes:
            node.postBake(refholder)

    def run(self):
        print('Executing node tree')

        nodes = self.topological_sort()
        eng = engine.Engine(nodes)
        eng.run()

    # returns [(node, [(node_index, socket_index)])]
    def topological_sort(self):
        permanent = defaultdict(lambda: False)
        temporary = defaultdict(lambda: False)

        nodes = []

        def visit(node):
            if permanent[node.name]:
                return
            if temporary[node.name]:
                raise CyclicNodeGraphError()

            temporary[node.name] = True

            input_indices = []
            for input in node.inputs:
                if len(input.links) == 0:
                    input_indices.append(None)
                else:
                    index = visit(input.links[0].from_node)
                    input_indices.append((index, list(input.links[0].from_node.outputs).index(input.links[0].from_socket)))

            permanent[node.name] = True

            index = len(nodes)
            nodes.append((node, input_indices))
            return index

        for node in self.nodes:
            if node._IsOutputNode:
                visit(node)

        return nodes

class CompilationError(Exception):
    pass

class CyclicNodeGraphError(CompilationError):
    pass
