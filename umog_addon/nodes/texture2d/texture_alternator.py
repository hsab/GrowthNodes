import bpy
from ... base_types import UMOGNode

class TextureAlternatorNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_TextureAlternatorNode"
    bl_label = "Texture Alternator"

    assignedType = "Texture2"

    texture = bpy.props.StringProperty()

    def create(self):
        self.newInput(self.assignedType, "Texture")
        self.newInput(self.assignedType, "Texture")
        self.newInput("Boolean", "Condition")

        socket = self.newOutput(self.assignedType, "Texture")

    def draw(self, layout):
        if self.outputs[0].value != "":
            self.drawPreview(layout, self.outputs[0].getTexture())

    def refresh(self):
        if self.inputs[2].value == True:
            self.outputs[0].value = self.inputs[0].value
        else:
            self.outputs[0].value = self.inputs[1].value
        self.outputs[0].refresh()

    def execute(self, refholder):
        pass
        # try:
        #     counter_index = self.inputs[2].links[0].to_socket.integer_value
        # except:
        #     print("no integer as input")

        # if (counter_index % 2) == 0:
        #     try:
        #         fn = self.inputs[0].links[0].from_socket
        #         self.outputs[0].texture_index = fn.texture_index
        #         print("use texture 0")
        #     except:
        #         print("no texture as input")
        # else:
        #     try:
        #         fn = self.inputs[1].links[0].from_socket
        #         self.outputs[0].texture_index = fn.texture_index
        #         print("use texture 1")
        #     except:
        #         print("no texture as input")