import bpy
from ... base_types import UMOGNode

class IntegerFrameNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_IntegerFrameNode"
    bl_label = "UMOG Integer Frame"

    def init(self, context):
        self.outputs.new("IntegerSocketType", "Integer0")
        self.outputs[0].integer_value = 0
        super().init(context)

    def preExecute(self, refholder):
        self.outputs[0].integer_value = 0

    def execute(self, refholder):
        pass

    def postFrame(self, refholder):
        self.outputs[0].integer_value = self.outputs[0].integer_value + 1
        print("Frame Counter " + str(self.outputs[0].integer_value))