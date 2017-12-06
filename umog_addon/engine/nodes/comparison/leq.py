from ..engine_node import *
from ...engine import types, engine
import bpy

class LessThanOrEqualNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_LessThanOrEqualNode"
    bl_label = "Less Than or Equal Node"

    opcode = engine.LEQ
