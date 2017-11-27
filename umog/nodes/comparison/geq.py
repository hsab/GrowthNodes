from ..umog_node import *
from ...engine import types, engine
import bpy

class GreaterThanOrEqualNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_GreaterThanOrEqualNode"
    bl_label = "Greater Than or Equal Node"

    opcode = engine.GEQ
