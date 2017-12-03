from ..umog_node import *
from ...engine import types, engine
import bpy

class PowerNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_PowerNode"
    bl_label = "Power Node"

    opcode = engine.POWER
