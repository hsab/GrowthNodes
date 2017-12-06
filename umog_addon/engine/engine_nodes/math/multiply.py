from ..engine_node import *
from ...engine import types, engine
import bpy

class MultiplyNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_MultiplyNode"
    bl_label = "Multiply Node"

    opcode = engine.MULTIPLY
