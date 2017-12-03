from ..umog_node import *
from ...engine import types, engine
import bpy

class GreaterThanNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_GreaterThanNode"
    bl_label = "Greater Than Node"

    opcode = engine.GT
