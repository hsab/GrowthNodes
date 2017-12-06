from ..engine_node import *
from ...engine import types, engine
import bpy

class DivideNode(bpy.types.Node, EngineBinaryScalarNode):
    bl_idname = "engine_DivideNode"
    bl_label = "Divide Node"

    opcode = engine.DIVIDE
