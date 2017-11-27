from ..umog_node import *
from ...engine import types, engine
import bpy

class LessThanNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_LessThanNode"
    bl_label = "Less Than Node"

    opcode = engine.LT
