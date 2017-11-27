from ..umog_node import *
from ...engine import types, engine
import bpy

class LessThanOrEqualNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_LessThanOrEqualNode"
    bl_label = "Less Than or Equal Node"

    opcode = engine.LEQ
