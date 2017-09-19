import bpy
from bpy.props import *
import random
from ... sockets.info import toIdName as toSocketIdName
from ... operators.callbacks import newNodeCallback
from ... operators.dynamic_operators import getInvokeFunctionOperator
from ... utils.nodes import getAnimationNodeTrees, iterAnimationNodes

class UMOGNode:
    bl_width_min = 40
    bl_width_max = 5000
    _isUMOGNode = True

    # unique string for each node; don't change it at all
    identifier = StringProperty(name = "Identifier", default = "")
    inInvalidNetwork = BoolProperty(name = "In Invalid Network", default = False)
    useNetworkColor = BoolProperty(name = "Use Network Color", default = True)

    # used for the listboxes in the sidebar
    activeInputIndex = IntProperty()
    activeOutputIndex = IntProperty()

    searchTags = []
    onlySearchTags = False
    # can contain: 'NO_EXECUTION', 'NOT_IN_SUBPROGRAM',
    #              'NO_AUTO_EXECUTION', 'NO_TIMING',
    options = set()

    # can be "NONE", "ALWAYS" or "HIDDEN_ONLY"
    dynamicLabelType = "NONE"

    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "umog_UMOGNodeTree"

    # functions subclasses can override
    ######################################

    def setup(self):
        pass

    def preCreate(self):
        pass

    def postCreate(self):
        pass

    def draw(self, layout):
        pass

    def draw_buttons(self, context, layout):
        if self.inInvalidNetwork: layout.label("Invalid Network", icon = "ERROR")
        self.draw(layout)

    def init(self, context):
        self.width_hidden = 100
        self.identifier = createIdentifier()
        self.setup()
        if self.isRefreshable:
            self.refresh() 
    
    # Update and Refresh
    ####################################################

    def refresh(self, context = None):
        if not self.isRefreshable:
            raise Exception("node is not refreshable")

        self._refresh()


    def _refresh(self):
        self._clear()
        self._create()

    def _clear(self):
        pass

    def _create(self):
        self.preCreate()
        self.create()
        self.postCreate()

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
        index = socket.getIndex(self)
        if socket.isOutput:
            if index < self.activeOutputIndex: self.activeOutputIndex -= 1
        else:
            if index < self.activeInputIndex: self.activeInputIndex -= 1
        socket.sockets.remove(socket)

    @property
    def nodeTree(self):
        return self.id_data

    @property
    def activeInputSocket(self):
        if len(self.inputs) == 0: return None
        return self.inputs[self.activeInputIndex]

    @property
    def activeOutputSocket(self):
        if len(self.outputs) == 0: return None
        return self.outputs[self.activeOutputIndex]

    @property
    def sockets(self):
        return list(self.inputs) + list(self.outputs)

    @property
    def isRefreshable(self):
        return hasattr(self, "create")

    def getInputSocketVariables(self):
        return {socket.identifier : socket.identifier for socket in self.inputs}

    def getOutputSocketVariables(self):
        return {socket.identifier : socket.identifier for socket in self.outputs}

    def newInput(self, type, name, identifier = None, alternativeIdentifier = None, **kwargs):
        idName = toSocketIdName(type)
        if idName is None:
            raise ValueError("Socket type does not exist: {}".format(repr(type)))
        if identifier is None: identifier = name
        socket = self.inputs.new(idName, name, identifier)
        self._setAlternativeIdentifier(socket, alternativeIdentifier)
        self._setSocketProperties(socket, kwargs)
        return socket

    def newOutput(self, type, name, identifier = None, alternativeIdentifier = None, **kwargs):
        idName = toSocketIdName(type)
        if idName is None:
            raise ValueError("Socket type does not exist: {}".format(repr(type)))
        if identifier is None: identifier = name
        socket = self.outputs.new(idName, name, identifier)
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
                       description = "", emboss = True, confirm = False,
                       data = None, passEvent = False):
        idName = getInvokeFunctionOperator(description)
        props = layout.operator(idName, text = text, icon = icon, emboss = emboss)
        props.callback = self.newCallback(functionName)
        props.invokeWithData = data is not None
        props.confirm = confirm
        props.data = str(data)
        props.passEvent = passEvent

    def invokeSelector(self, layout, selectorType, functionName,
                       text = "", icon = "NONE", description = "", emboss = True, **kwargs):
        data, executionName = self._getInvokeSelectorData(selectorType, functionName, kwargs)
        self.invokeFunction(layout, executionName,
            text = text, icon = icon, description = description,
            emboss = emboss, data = data)

    def _getInvokeSelectorData(self, selector, function, kwargs):
        if selector == "DATA_TYPE":
            dataTypes = kwargs.get("dataTypes", "ALL")
            return function + "," + dataTypes, "_selector_DATA_TYPE"
        elif selector == "PATH":
            return function, "_selector_PATH"
        elif selector == "ID_KEY":
            return function, "_selector_ID_KEY"
        elif selector == "AREA":
            return function, "_selector_AREA"
        else:
            raise Exception("invalid selector type")

def createIdentifier():
    identifierLength = 15
    characters = "abcdefghijklmnopqrstuvwxyz" + "0123456789"
    choice = random.SystemRandom().choice
    return "_" + ''.join(choice(characters) for _ in range(identifierLength))