from ..umog_node import *
from ...engine import types, engine
import bpy

class MultiplyNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_MultiplyNode"
    bl_label = "Multiply Node"

    opcode = engine.MULTIPLY
