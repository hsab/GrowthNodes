import bpy
from ..engine import types, engine
from collections import namedtuple
from enum import Enum

class UMOGNode(bpy.types.Node):
    bl_width_min = 10
    bl_width_max = 5000

    _IsUMOGNode = True
    _IsInputNode = False
    _IsOutputNode = False

    bl_label = "UMOGNode"

    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "umog_UMOGNodeTree"

    def init(self, context):
        pass

    def get_operation(self):
        return Operation(engine.NOP, [], [], [], [])

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

class UMOGOutputNode(UMOGNode):
    _IsOutputNode = True

    def init(self, context):
        super().init(context)

    def write_keyframe(self, refholder, frame):
        pass

class UMOGInputNode(UMOGNode):
    _IsInputNode = True

    def init(self, context):
        super().init(context)

Operation = namedtuple('Operation', ['opcode', 'input_types', 'output_types', 'buffer_types', 'arguments'])
class ArgumentType(Enum):
    SOCKET = 0
    BUFFER = 1
Argument = namedtuple('Argument', ['type', 'index'])
