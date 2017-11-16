import bpy
from .. import UMOGNode

class IntegerSubframeNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_IntegerSubframeNode"
    bl_label = "UMOG Integer Subframe"

    def init(self, context):
        self.outputs.new("IntegerSocketType", "Integer0")
        self.outputs[0].integer_value = 0
        super().init(context)

    def preExecute(self, refholder):
        self.outputs[0].integer_value = 0

    def execute(self, refholder):
        self.outputs[0].integer_value = self.outputs[0].integer_value + 1
        print("Subrame Counter " + str(self.outputs[0].integer_value))

    def postFrame(self, refholder):
        self.outputs[0].integer_value = 0