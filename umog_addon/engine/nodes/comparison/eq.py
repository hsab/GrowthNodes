from ..engine_node import *
from ...engine import types, engine
import bpy

class EqualNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_EqualNode"
    bl_label = "Equal Node"

    opcode = engine.EQ
