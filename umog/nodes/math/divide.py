from ..umog_node import *
from ...engine import types, engine
import bpy

class DivideNode(bpy.types.Node, UMOGBinaryScalarNode):
    bl_idname = "umog_DivideNode"
    bl_label = "Divide Node"

    opcode = engine.DIVIDE
