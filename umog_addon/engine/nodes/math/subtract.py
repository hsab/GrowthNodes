from ..engine_node import *
from ...engine import types, engine
import bpy

class SubtractNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_SubtractNode"
    bl_label = "Subtract Node"

    opcode = engine.SUBTRACT
