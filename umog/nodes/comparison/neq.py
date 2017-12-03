from ..umog_node import *
from ...engine import types, engine
import bpy

class NotEqualNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_NotEqualNode"
    bl_label = "Not Equal Node"

    opcode = engine.NEQ
