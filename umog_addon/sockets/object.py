import bpy
from bpy.props import *
from bpy.types import Object
from .. base_types import UMOGSocket
from .. utils.nodes import newNodeAtCursor

class ObjectSocket(bpy.types.NodeSocket, UMOGSocket):
    '''Custom Object socket type'''

    bl_idname = 'ObjectSocketType'
    bl_label = 'Object Socket'
    dataType = "Object"
    allowedInputTypes = ["Object"]

    drawColor = (0, 1, 1, 0.5)
    storable = False
    comparable = True

    objectName = StringProperty()
    objectCreationType = StringProperty(default = "")
    showHideToggle = BoolProperty(default = False)

    def drawProperty(self, layout, text, node):
        layout.label(text=text)
        row = layout.row()
        self.invokeFunction(row, node, "addIntegerNode", icon = "PLUS", emboss = False,
                description = "Create a new node node")

    def addIntegerNode(self):
        node = newNodeAtCursor("umog_IntegerNode")
        self.linkWith(node.outputs[0])