import bpy
from ... base_types import UMOGNode

class TextureAlternatorNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ObjectAlternatorNode"
    bl_label = "Object Alternator"

    assignedType = "Object"

    Object = bpy.props.StringProperty()

    def create(self):
        self.newInput(self.assignedType, "Object")
        self.newInput(self.assignedType, "Object")
        self.newInput("Boolean", "Condition")

        socket = self.newOutput(self.assignedType, "Object")

    def draw(self, layout):
        pass

    def refresh(self):
        if self.inputs[2].value == True:
            self.outputs[0].value = self.inputs[0].value
        else:
            self.outputs[0].value = self.inputs[1].value
        self.outputs[0].refresh()

    def execute(self, refholder):
        pass