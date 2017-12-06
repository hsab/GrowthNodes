import bpy
from bpy.types import NodeTree
from bpy.props import *
from ..utils.debug import *
from ..utils.handlers import eventUMOGHandler
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

    bakeCount = IntProperty(name = "Bake ID", description = "Bake count", default = 1,
                            min = 1, update = updateTimeInfo)

    StartFrame = IntProperty(name = "Start", description = "Frame on which the simulation starts", default = 1,
                             min = 1, update = updateTimeInfo)

    EndFrame = IntProperty(name = "End", description = "Frame on which the simulation stops", default = 2,
                           min = 2, update = updateTimeInfo)

    Substeps = IntProperty(name = "Substeps", description = "Substeps", default = 1,
                            min = 1)

    TextureResolution = IntProperty(name = "Texture Resolution",
                                    description = "Base resolution for saving and creating new textures", default = 256,
                                    min = 64, update = updateTimeInfo)
    
    ShowFrameSettings = BoolProperty(name="Toggle Frame Settings", default = True)

    UniqueIDTracker = IntProperty(default=0)

    TexturePreviewInPanel = BoolProperty(name="Toggle Frame Settings", default = False, description="Disables the preview instance in UMOG panel")
    
    ToggleTextureSettings = BoolProperty(name="Toggle Texture", default = False, description="Toggle Texture Settings")

    ToggleTextureList = BoolProperty(name="Toggle Texture List", default = True, description="Toggle Texture List")
    ToggleColorSettings = BoolProperty(name="Toggle Color", default = False, description="Toggle Color Settings")
    ToggleRampSettings = BoolProperty(name="Toggle Ramp", default = False, description="Toggle Ramp Settings")

    ToggleObjectList = BoolProperty(name="Toggle Object List", default = True, description="Toggle Object List")
    ToggleVertexGroupList = BoolProperty(name="Toggle Vertex Group List", default = False, description="Toggle Vertex Group List")
    ToggleShapeKeyList = BoolProperty(name="Toggle Shapekey List", default = False, description="Toggle Shapekey List")


class CustomProp(bpy.types.PropertyGroup):
    name = StringProperty()
    id = IntProperty()
    texture = StringProperty()

class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "FORCE_TURBULENCE"

    linearizedNodes = []
    unlinkedNodes = []
    connectedComponents = 0

    updateInProgress = BoolProperty(name = "Is an update in progress?", default = False)

    executeInProgress = BoolProperty(name = "Is an execution in progress?",
                                     default = False)

    properties = PointerProperty(type = UMOGNodeTreeProperties)


    @property
    def props(self):
        return self.properties

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

            self.populateReferences()

    def populateReferences(self):
        self.textures.clear()
        self.objects.clear()
        referencedTextures = set()
        referencedObjects = set()
        for node in self.linearizedNodes:
            for socket in node.sockets:
                if socket.dataType == "Texture2" and socket.value != "":
                    referencedTextures.add(socket.value)
                if socket.dataType == "Object" and socket.value != "":
                    referencedObjects.add(socket.value)
        for texture in referencedTextures:
            item = self.textures.add()
            item.id = len(self.textures)
            item.name = texture
            self.textures_index = (len(self.textures)-1)
        
        for object in referencedObjects:
            item = self.objects.add()
            item.id = len(self.objects)
            item.name = object
            self.object_index = (len(self.objects)-1)

    def areLinksValid(self):
        returnVal = True
        for link in self.links:
            fromSocket = link.from_socket
            toSocket = link.to_socket
            allAllowed = "All" in toSocket.allowedInputTypes
            typeAllowed = fromSocket.dataType in toSocket.allowedInputTypes
            if allAllowed or typeAllowed:
                link.is_valid = True
            else:
                link.is_valid = False
                returnVal = False
        return returnVal

    def updateUnlinkedNodesSocketNames(self):
        for node in self.unlinkedNodes:
            for socket in node.sockets:
                socket.reverseName()
                
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

    def deselectAll(self):
        for n in self.nodes:
            n.select = False

    def viewNode(self, node):
        self.deselectAll()
        node.select = True
        node.enableUnlinkedHighlight()
        bpy.ops.node.view_selected()

    def raisePopup(self, type, msg):
        bpy.ops.umog.popup('INVOKE_DEFAULT', errType = type, errMsg=msg)

    def raiseAndView(self, node, msg):
        self.raisePopup('ERROR', msg + " " + node.name)
        self.viewNode(node)

    def execute(self, refholder, animate = False):
        if self.areLinksValid():
            self.update()

            for node in self.linearizedNodes:
                try: node.packSockets()
                except Exception as e:
                    self.raiseAndView(node, 'Failed to pack data for node')
                    return

            for node in self.linearizedNodes:
                try: node.preExecute(refholder)
                except Exception as e:
                    self.raiseAndView(node, 'Pre-execution failed for node')
                    return

            self.executeInProgress = True

            for frame in range(self.properties.StartFrame, self.properties.EndFrame):
                # Update the frame
                scene = bpy.context.scene
                scene.frame_set(frame)

                for sub_frame in range(0, self.properties.Substeps):
                    for node in self.linearizedNodes:
                        try: node.refreshNode()
                        except Exception as e:
                            self.raiseAndView(node, 'Unable to refresh node')
                            return
                        
                        try: node.execute(refholder)
                        except Exception as e:
                            self.raiseAndView(node, 'Unable to execute node')
                            return

                for node in self.linearizedNodes:
                    try: node.postFrame(refholder)
                    except Exception as e:
                        self.raiseAndView(node, 'Post-execution failed for node')
                        return

            self.executeInProgress = False

            for node in self.linearizedNodes:
                try: node.postBake(refholder)
                except Exception as e:
                    self.raiseAndView(node, 'Post-bake failed for node')
                    return

            self.properties.bakeCount = self.properties.bakeCount + 1
        else:
            self.raisePopup('ERROR', "Node-tree contains links with mismatched types. These are highlighted in red.")

class UMOGUIListProperty(bpy.types.PropertyGroup):
    name = StringProperty()
    id = IntProperty()

# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------

def register():
    bpy.types.NodeTree.textures = CollectionProperty(type=UMOGUIListProperty)
    bpy.types.NodeTree.textures_index = IntProperty()
    bpy.types.NodeTree.objects = CollectionProperty(type=UMOGUIListProperty)
    bpy.types.NodeTree.objects_index = IntProperty()

def unregister():
    del bpy.types.NodeTree.textures
    del bpy.types.NodeTree.textures_index
    del bpy.types.NodeTree.objects
    del bpy.types.NodeTree.objects_index