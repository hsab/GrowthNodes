from ..umog_node import *
from ...engine import types, engine
import bpy

class EqualNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_EqualNode"
    bl_label = "Equal Node"

    opcode = engine.EQ
