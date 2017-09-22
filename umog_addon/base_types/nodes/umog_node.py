import bpy
from bpy.props import *
from ... utils.debug import *
import random
from ... sockets.info import toIdName as toSocketIdName
from ... operators.callbacks import newNodeCallback
from ... operators.dynamic_operators import getInvokeFunctionOperator

class UMOGNode:
    bl_width_min = 40
    bl_width_max = 5000
    _isUMOGNode = True
    _IsUMOGOutputNode = False
    # unique string for each node; don't change it at all
    identifier = StringProperty(name = "Identifier", default = "")
    inInvalidNetwork = BoolProperty(name = "In Invalid Network", default = False)

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

    # functions subclasses can override
    ######################################

    def setup(self):
        pass

    # def preCreate(self):
    #     pass

    # def postCreate(self):
    #     pass

    def draw(self, layout):
        pass

    def draw_buttons(self, context, layout):
        if self.inInvalidNetwork: layout.label("Invalid Network", icon = "ERROR")
        self.draw(layout)

    def init(self, context):
        self.width_hidden = 100
        self.identifier = createIdentifier()
        self.setup()

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

def createIdentifier():
    identifierLength = 15
    characters = "abcdefghijklmnopqrstuvwxyz" + "0123456789"
    choice = random.SystemRandom().choice
    return "_" + ''.join(choice(characters) for _ in range(identifierLength))

def nodeToID(node):
    return (node.id_data.name, node.name)

def register():
    bpy.types.Node.toID = nodeToID