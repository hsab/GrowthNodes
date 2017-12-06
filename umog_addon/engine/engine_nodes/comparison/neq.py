from ..engine_node import *
from ...engine import types, engine
import bpy

class NotEqualNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_NotEqualNode"
    bl_label = "Not Equal Node"

    opcode = engine.NEQ
