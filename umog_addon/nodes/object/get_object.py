from ... base_types import UMOGNode
import bpy

class GetTextureNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ObjectNode"
    bl_label = "Object"
    assignedType = "Object"

    texture = bpy.props.StringProperty()

    def create(self):
        socket = self.newOutput(self.assignedType, "Object", drawOutput = True, drawLabel = False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def draw(self, layout):
        pass


    def execute(self, refholder):
        # print("get texture node execution, texture: " + self.texture)
        # print("texture handle: " + str(self.outputs[0].texture_index))
        # print(refholder.np2dtextures[self.outputs[0].texture_index])
        pass

    def preExecute(self, refholder):
        pass
        # consider saving the result from this
        # self.outputs[0].texture_index = refholder.getRefForTexture2d(self.texture)