import bpy
from .. import UMOGNode
from ... utils.events import propUpdate


class IntegerNode(UMOGNode):
    bl_idname = "umog_IntegerNode"
    bl_label = "UMOG Integer"
    assignedType = "Integer"

    input_value = bpy.props.IntProperty(update=propUpdate)

    def init(self, context):
        socket = self.newOutput(
            self.assignedType, "Value", drawOutput=True, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def preExecute(self, refholder):
        # consider saving the result from this
        self.outputs[0].integer_value = self.input_value

    def getProperty(self):
        return self.input_value
