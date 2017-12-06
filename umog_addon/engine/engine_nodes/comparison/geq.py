from ..engine_node import *
from ...engine import types, engine
import bpy

class GreaterThanOrEqualNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_GreaterThanOrEqualNode"
    bl_label = "Greater Than or Equal Node"

    opcode = engine.GEQ
