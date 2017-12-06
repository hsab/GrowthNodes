from ..engine_node import *
from ...engine import types, engine
import bpy

class AddNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_AddNode"
    bl_label = "Add Node"

    opcode = engine.ADD
