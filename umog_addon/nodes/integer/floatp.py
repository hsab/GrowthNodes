import bpy
from ... base_types import UMOGNode
from ... utils.events import propUpdate


class FloatNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_FloatNode"
    bl_label = "Float"
    assignedType = "Float"

    input_value = bpy.props.IntProperty(update=propUpdate)

    def create(self):
        socket = self.newOutput(
            self.assignedType, "Value", drawOutput=True, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def preExecute(self, refholder):
        # consider saving the result from this
        self.outputs[0].integer_value = self.input_value

    def getProperty(self):
        return self.input_value
