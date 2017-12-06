from ..engine_node import *
from ...engine import types, engine
import bpy

class PowerNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_PowerNode"
    bl_label = "Power Node"

    opcode = engine.POWER
