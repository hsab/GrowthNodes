import bpy
from bpy.props import *
from .. base_types import UMOGSocket
from .. utils.nodes import newNodeAtCursor

class VariableSocket(bpy.types.NodeSocket, UMOGSocket):
    '''Variable socket type'''

    bl_idname = 'VariableSocketType'
    bl_label = 'Variable Socket'
    dataType = "Variable"
    allowedInputTypes = ["All"]


    text = "varName"
    useIsUsedProperty = True
    defaultDrawType = "TEXT_PROPERTY"

    drawColor = (1, 1, 1, 0.5)

    def textChanged(self, context):
        pass

    text = StringProperty(default = "custom name", update = textChanged)

    socketCreationType = StringProperty(default = "")

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.label(text=text)
        row = layout.row()
        self.invokeFunction(row, node, "addIntegerNode", icon = "PLUS", emboss = False,
                description = "Create a new node node")
        self.invokeFunction(row, node, "addIntegerNode", icon = "PLUS", emboss = False,
                description = "Create a new node node")

    def addIntegerNode(self):
        node = newNodeAtCursor("umog_IntegerNode")
        self.linkWith(node.outputs[0])