from ..engine_node import *
from ...engine import types, engine
import bpy

class ModulusNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_ModulusNode"
    bl_label = "Modulus Node"

    opcode = engine.MODULUS
