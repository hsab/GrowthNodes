from ... base_types import UMOGNode
import bpy

class IntegerNode(UMOGNode):
    bl_idname = "umog_IntegerNode"
    bl_label = "UMOG Integer"

    input_value = bpy.props.IntProperty()

    def init(self, context):
        self.outputs.new("IntegerSocketType", "Integer0")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "input_value", text="Value")

    def preExecute(self, refholder):
        # consider saving the result from this
        self.outputs[0].integer_value = self.input_value