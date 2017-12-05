import math
import bpy
from bpy.props import *
from ...utils.debug import *
import random
from ...sockets.info import toIdName as toSocketIdName
from ...operators.callbacks import newNodeCallback
from ...operators.dynamic_operators import getInvokeFunctionOperator
from ...utils.events import propUpdate


class UMOGNodeExecutionProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_NodeExecutionProperties"
    visited = BoolProperty(name = "Visited in Topological Sort", default = False)
    connectedComponent = IntProperty(name = "Connected Component Network of Node",
                                     default = 0)


class UMOGNodeDisplayProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_NodeDisplayProperties"
    useCustomColor = BoolProperty(name = "Use Custom Color", default = False)
    customColor = FloatVectorProperty(name = "Custom Color", default = (0.0, 0.0, 0.0),
                                      min = 0, max = 1)
    highlightColor = FloatVectorProperty(name = "Highlight Color",
                                         default = (0.6, 0.4, 0.4), min = 0, max = 1)


class UMOGNode:
    bl_width_min = 40
    bl_width_max = 5000
    _isUMOGNode = True
    _IsUMOGOutputNode = False

    execution = PointerProperty(type = UMOGNodeExecutionProperties)
    display = PointerProperty(type = UMOGNodeDisplayProperties)

    # unique string for each node; don't change it at all
    identifier = StringProperty(name = "Identifier", default = "")

    # used for the listboxes in the sidebar
    activeInputIndex = IntProperty()
    activeOutputIndex = IntProperty()

    # can contain: 'NO_EXECUTION', 'NOT_IN_SUBPROGRAM',
    #              'NO_AUTO_EXECUTION', 'NO_TIMING',
    options = set()

    # can be "NONE", "ALWAYS" or "HIDDEN_ONLY"
    dynamicLabelType = "NONE"

    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "umog_UMOGNodeTree"

    def init(self, context):
        self.display.customColor = self.color
        self.display.useCustomColor = self.use_custom_color

        self.width_hidden = 100
        self.identifier = createIdentifier()
        self.setup()

    def free(self):
        for socket in self.inputs:
            socket.destroy()
        for socket in self.outputs:
            socket.destroy()
        self.destroy()
        print("freed")

    def setup(self):
        self.preCreate()
        self.create()
        self.postCreate()

    def draw_buttons(self, context, layout):
        self.draw(layout)

    def refreshInputs(self):
        for socket in self.inputs:
            socket.refreshSocket()

    def refreshNode(self):
        self.refreshInputs()
        self.preRefresh()
        self.refresh()
        self.postRefresh()

    def refreshOnFrameChange(self):
        pass

    def packSockets(self):
        for socket in self.inputs:
            socket.packSocket()
        for socket in self.outputs:
            socket.packSocket()

    # functions subclasses can override
    ######################################

    def preCreate(self):
        pass

    def create(self):
        pass

    def postCreate(self):
        pass

    def update(self):
        pass

    def preRefresh(self):
        pass

    def refresh(self):
        pass

    def postRefresh(self):
        pass

    def refreshOnFrameChange(self):
        pass

    def draw(self, layout):
        pass

    def destroy(self):
        pass

    def newCallback(self, functionName):
        return newNodeCallback(self, functionName)

    # this will be called when the node is executed by bake meshes
    # will be called each iteration
    def execute(self, refholder):
        pass

    # will be called once before the node will be executed by bake meshes
    # refholder is passed to this so it can register any objects that need it
    def preExecute(self, refholder):
        pass

    # will be called once at the end of each frame
    def postFrame(self, refholder):
        pass

    # will be called once right before bake returns
    def postBake(self, refholder):
        pass

    def socketMoved(self):
        self.socketChanged()

    def customSocketNameChanged(self, socket):
        self.socketChanged()

    def socketRemoved(self):
        self.socketChanged()

    def socketChanged(self):
        """
        Use this function when you don't need
        to know what happened exactly to the sockets
        """
        pass

    def removeSocket(self, socket):
        index = socket.index
        if socket.isOutput:
            if index < self.activeOutputIndex:
                self.activeOutputIndex -= 1
        else:
            if index < self.activeInputIndex:
                self.activeInputIndex -= 1
        socket.sockets.remove(socket)

    def storeCustomColor(self):
        currentColor = self.color
        redIsClose = math.isclose(currentColor[0], self.display.highlightColor[0],
                                  abs_tol = 0.01)
        greenIsClose = math.isclose(currentColor[1], self.display.highlightColor[1],
                                    abs_tol = 0.01)
        blueIsClose = math.isclose(currentColor[2], self.display.highlightColor[2],
                                   abs_tol = 0.01)

        if not redIsClose or not greenIsClose or not blueIsClose:
            self.display.customColor = self.color
            self.display.useCustomColor = self.use_custom_color

    def enableUnlinkedHighlight(self):
        self.storeCustomColor()
        self.use_custom_color = True
        self.color = self.display.highlightColor

    def disableUnlinkedHighlight(self):
        self.use_custom_color = self.display.useCustomColor
        self.color = self.display.customColor

    @property
    def nodeTree(self):
        return self.id_data

    @property
    def hasInputLinks(self):
        for inputSocket in self.inputs:
            if len(inputSocket.links) > 0:
                return True
        return False

    @property
    def hasOutputLinks(self):
        for outputSocket in self.outputs:
            if len(outputSocket.links) > 0:
                return True
        return False

    @property
    def isLinked(self):
        return self.hasOutputLinks or self.hasInputLinks

    @property
    def activeInputSocket(self):
        if len(self.inputs) == 0:
            return None
        return self.inputs[self.activeInputIndex]

    @property
    def activeOutputSocket(self):
        if len(self.outputs) == 0:
            return None
        return self.outputs[self.activeOutputIndex]

    @property
    def sockets(self):
        return list(self.inputs) + list(self.outputs)

    def newInput(self, type, name, identifier = None, alternativeIdentifier = None,
                 **kwargs):
        idName = toSocketIdName(type)
        if idName is None:
            raise ValueError("Socket type does not exist: {}".format(repr(type)))
        if identifier is None:
            identifier = name
        socket = self.inputs.new(idName, name, identifier + self.nodeTree.getNextUniqueID())
        socket.originalName = socket.name
        self._setAlternativeIdentifier(socket, alternativeIdentifier)
        self._setSocketProperties(socket, kwargs)
        return socket

    def newOutput(self, type, name, identifier = None, alternativeIdentifier = None,
                  **kwargs):
        idName = toSocketIdName(type)
        if idName is None:
            raise ValueError("Socket type does not exist: {}".format(repr(type)))
        if identifier is None:
            identifier = name
        socket = self.outputs.new(idName, name, identifier + self.nodeTree.getNextUniqueID())
        socket.originalName = socket.name
        self._setAlternativeIdentifier(socket, alternativeIdentifier)
        self._setSocketProperties(socket, kwargs)
        return socket

    def _setAlternativeIdentifier(self, socket, alternativeIdentifier):
        if isinstance(alternativeIdentifier, str):
            socket.alternativeIdentifiers = [alternativeIdentifier]
        elif isinstance(alternativeIdentifier, (list, tuple, set)):
            socket.alternativeIdentifiers = list(alternativeIdentifier)

    def _setSocketProperties(self, socket, properties):
        for key, value in properties.items():
            setattr(socket, key, value)

    def invokeFunction(self, layout, functionName, text = "", icon = "NONE",
                       description = "", emboss = True, confirm = False, data = None,
                       passEvent = False):
        idName = getInvokeFunctionOperator(description)
        props = layout.operator(idName, text = text, icon = icon, emboss = emboss)
        props.callback = self.newCallback(functionName)
        props.invokeWithData = data is not None
        props.confirm = confirm
        props.data = str(data)
        props.passEvent = passEvent

    def enablePreview(self):
        self.nodeTree.props.TexturePreviewInPanel = False

    def drawPreview(self, layout, texture):
        try:
            if self.select and (len(bpy.context.selected_nodes) == 1):
                if not self.nodeTree.props.TexturePreviewInPanel:
                    layout.template_preview(texture)
                else:
                    self.invokeFunction(layout, "enablePreview",
                        text = "Enable Preview",
                        description = "Disables the preview instance in UMOG panel",
                        icon = "IMAGE_COL")
        except:
            pass


def createIdentifier():
    identifierLength = 15
    characters = "abcdefghijklmnopqrstuvwxyz" + "0123456789"
    choice = random.SystemRandom().choice
    return "_" + ''.join(choice(characters) for _ in range(identifierLength))


def nodeToID(node):
    return (node.id_data.name, node.name)


def isUMOGNode(node):
    return getattr(node, "_isUMOGNode", False)


def register():
    bpy.types.Node.toID = nodeToID
    bpy.types.Node.isUMOGNode = BoolProperty(default = False, get = isUMOGNode)


def unregister():
    del bpy.types.Node.toID
    del bpy.types.Node.isUMOGNode
