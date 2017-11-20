import math
import bpy
from bpy.props import *
from ..utils.debug import *
import random
from ..utils.events import propUpdate

from ..engine import types, engine

class UMOGNodeExecutionProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_NodeExecutionProperties"
    visited = BoolProperty(name = "Visited in Topological Sort", default = False)
    connectedComponent = IntProperty(name = "Connected Component Network of Node",
                                     default = 0)

class UMOGNode(bpy.types.Node):
    bl_width_min = 40
    bl_width_max = 5000

    _IsUMOGNode = True
    _IsInputNode = False
    _IsOutputNode = False

    bl_label = "UMOGNode"

    # unique string for each node; don't change it at all
    identifier = StringProperty(name = "Identifier", default = "")

    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "umog_UMOGNodeTree"

        self.width_hidden = 100
        self.identifier = createIdentifier()

    def init(self, context):
        pass

    def refreshNode(self):
        for socket in self.inputs:
            socket.refreshSocket()
        self.refresh()

    def refreshOnFrameChange(self):
        pass

    def packSockets(self):
        for socket in self.inputs:
            socket.packSocket()
        for socket in self.outputs:
            socket.packSocket()

    # functions subclasses can override
    ######################################

    def update(self):
        pass

    def refresh(self):
        pass

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

    def postBake(self, refholder):
        pass

    def enableUnlinkedHighlight(self):
        self.color = (0.6, 0.4, 0.4)

    def disableUnlinkedHighlight(self):
        self.color = (0.0, 0.0, 0.0)

    @property
    def nodeTree(self):
        return self.id_data

    @property
    def isLinked(self):
        for inputSocket in self.inputs:
            if len(inputSocket.links) > 0:
                return True

        for outputSocket in self.outputs:
            if len(outputSocket.links) > 0:
                return True

        return False

    def newInput(self, idName, name, identifier = None, **kwargs):
        if identifier is None:
            identifier = name
        socket = self.inputs.new(idName, name, identifier + self.nodeTree.getNextUniqueID())
        self._setSocketProperties(socket, kwargs)
        return socket

    def newOutput(self, idName, name, identifier = None, **kwargs):
        if identifier is None:
            identifier = name
        socket = self.outputs.new(idName, name, identifier + self.nodeTree.getNextUniqueID())
        self._setSocketProperties(socket, kwargs)
        return socket

    def _setSocketProperties(self, socket, properties):
        for key, value in properties.items():
            setattr(socket, key, value)

    # engine
    def get_operation(self, input_types):
        return engine.Operation(engine.NOP, [], [], [], [])

    def get_buffer_values(self):
        return []


def createIdentifier():
    identifierLength = 15
    characters = "abcdefghijklmnopqrstuvwxyz" + "0123456789"
    choice = random.SystemRandom().choice
    return "_" + ''.join(choice(characters) for _ in range(identifierLength))


class UMOGOutputNode(UMOGNode):
    _IsOutputNode = True

    def init(self, context):
        super().init(context)

    def output_value(self, value):
        pass

    def write_keyframe(self, refholder, frame):
        pass

class UMOGInputNode(UMOGNode):
    _IsInputNode = True

    def init(self, context):
        super().init(context)

def register():
    # PointerProperties can only be added after the PropertyGroup is registered
    bpy.types.Node.execution = PointerProperty(type = UMOGNodeExecutionProperties)
