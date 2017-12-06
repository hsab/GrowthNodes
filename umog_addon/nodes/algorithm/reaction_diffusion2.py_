import bpy
from ... base_types import UMOGNode

class TextureAlternatorNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ReactionDiffusionNode2"
    bl_label = "Reaction Diffusion 2"

    assignedType = "Texture2"

    texture = bpy.props.StringProperty()

    def create(self):
        self.newInput(self.assignedType, "A").isPacked = True
        self.newInput(self.assignedType, "B").isPacked = True
        self.newInput("Float", "Feed", value=0.055).isPacked = True
        self.newInput("Float", "Kill", value=0.062).isPacked = True
        self.newInput("Float", "A Rate", value=1.0).isPacked = True
        self.newInput("Float", "B Rate", value=0.5).isPacked = True
        self.newInput("Float", "Delta Time", value=1.0).isPacked = True
        self.newOutput(self.assignedType, "A'").isPacked = True
        self.newOutput(self.assignedType, "B'").isPacked = True

    def draw(self, layout):
        pass

    def refresh(self):
        pass
        # if self.inputs[2].value == True:
        #     self.outputs[0].value = self.inputs[0].value
        # else:
        #     self.outputs[0].value = self.inputs[1].value
        # self.outputs[0].refresh()

    def execute(self, refholder):
        pixels = self.inputs[0].getPixels()
        self.outputs[0].setPackedImageFromPixels(pixels)
        pixels = self.inputs[1].getPixels()
        self.outputs[1].setPackedImageFromPixels(pixels)
        # print("Feed\t",self.inputs[2].value,"\t", self.inputs[2].getFromSocket.value)
        # print("Kill\t",self.inputs[3].value,"\t", self.inputs[3].getFromSocket.value)
        # print("Da\t",self.inputs[4].value,"\t", self.inputs[4].getFromSocket.value)
        # print("Db\t",self.inputs[5].value,"\t", self.inputs[5].getFromSocket.value)
        # print("Dt\t",self.inputs[6].value,"\t", self.inputs[6].getFromSocket.value)
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