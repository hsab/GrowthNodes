import bpy
from .. import UMOGNode
from ...utils.events import propUpdate


class IntegerFrameNode(UMOGNode):
    bl_idname = "umog_IntegerFrameNode"
    bl_label = "UMOG Integer Frame"

    assignedType = "Integer"

    input_value = bpy.props.IntProperty(update=propUpdate)

    def init(self, context):
        socket = self.newOutput(self.assignedType, "Frame: ")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket.value = bpy.context.scene.frame_current
        socket.name = "Frame: " + str(self.outputs[0].value)

    def preExecute(self, refholder):
        # consider saving the result from this
        self.outputs[0].integer_value = self.input_value

    def refresh(self):
        self.refreshOnFrameChange()

    def refreshOnFrameChange(self):
        self.outputs[0].value = bpy.context.scene.frame_current
        self.outputs[0].name = "Frame: " + str(self.outputs[0].value)

    def getProperty(self):
        return self.input_value
