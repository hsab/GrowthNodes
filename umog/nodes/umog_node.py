import math
import bpy
from bpy.props import *
import random
import numpy as np

from ..engine import types, engine

class UMOGNode:
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

    def newInput(self, idName, name):
        socket = self.inputs.new(idName, name, identifier + self.nodeTree.getNextUniqueID())
        return socket

    # engine
    def get_operation(self, input_types):
        return engine.Operation(engine.NOP, [], [], [])

    def get_default_value(self, index, argument_type):
        return None

class UMOGOutputNode(UMOGNode):
    _IsOutputNode = True

    def init(self, context):
        super().init(context)

    def output_value(self, value):
        pass

class UMOGInputNode(UMOGNode):
    _IsInputNode = True

    def init(self, context):
        super().init(context)

class UMOGBinaryScalarNode(UMOGNode):
    default_a = FloatProperty(default=0.0)
    default_b = FloatProperty(default=0.0)

    opcode = engine.NOP

    def init(self, context):
        a = self.inputs.new("ScalarSocketType", "a")
        a.property_path = "default_a"
        b = self.inputs.new("ScalarSocketType", "b")
        b.property_path = "default_b"

        self.outputs.new("ScalarSocketType", "out")

        super().init(context)

    def get_operation(self, input_types):
        if input_types[0].tag == types.NONE:
            a = types.Array(0,0,0,0,0,0)
        else:
            a = input_types[0]

        if input_types[1].tag == types.NONE:
            b = types.Array(0,0,0,0,0,0)
        else:
            b = input_types[1]

        output_types = types.binary_scalar(a, b)
        argument_types = [a, b]

        return engine.Operation(
            self.opcode,
            argument_types,
            output_types,
            [])

    def get_default_value(self, index, argument_type):
        if index == 0:
            value = self.default_a
        else:
            value = self.default_b

        return np.array([value], dtype=np.float32, order="F").reshape((1,1,1,1,1))
