from ..engine_node import *
from ...engine import types, engine
import bpy

class LessThanNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_LessThanNode"
    bl_label = "Less Than Node"

    opcode = engine.LT
