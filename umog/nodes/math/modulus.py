from ..umog_node import *
from ...engine import types, engine
import bpy

class ModulusNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_ModulusNode"
    bl_label = "Modulus Node"

    opcode = engine.MODULUS
