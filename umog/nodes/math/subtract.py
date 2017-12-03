from ..umog_node import *
from ...engine import types, engine
import bpy

class SubtractNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_SubtractNode"
    bl_label = "Subtract Node"

    opcode = engine.SUBTRACT
