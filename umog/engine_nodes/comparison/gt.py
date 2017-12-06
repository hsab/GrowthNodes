from ..engine_node import *
from ...engine import types, engine
import bpy

class GreaterThanNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_GreaterThanNode"
    bl_label = "Greater Than Node"

    opcode = engine.GT
