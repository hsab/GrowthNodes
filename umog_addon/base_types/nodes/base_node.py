import bpy
from ... sockets.info import toIdName as toSocketIdName

class UMOGNode:

    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "umog_UMOGNodeTree"

    def init(self, context):
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

    # will be called once right before bake returns
    def postBake(self, refholder):
        pass

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