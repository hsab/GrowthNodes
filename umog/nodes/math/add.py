from ..umog_node import *
from ...engine import types, engine
import bpy

class AddNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_AddNode"
    bl_label = "Add Node"

    opcode = engine.ADD
