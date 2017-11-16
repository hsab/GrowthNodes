import bpy
from .. import UMOGNode
from ... utils.events import propUpdate


class BooleanNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_BooleanNode"
    bl_label = "Boolean"
    assignedType = "Boolean"

    input_value = bpy.props.IntProperty(update=propUpdate)

    def create(self):
        socket = self.newOutput(
            self.assignedType, "", drawOutput=True, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def preExecute(self, refholder):
        # consider saving the result from this
        self.outputs[0].integer_value = self.input_value

    def getProperty(self):
        return self.input_value
