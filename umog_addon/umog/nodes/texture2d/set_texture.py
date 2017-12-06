from ... base_types import UMOGOutputNode
import copy
import bpy

class SetTextureNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SetTextureNode"
    bl_label = "Set Texture"

    texture = bpy.props.StringProperty()

    texture_index = bpy.props.IntProperty()

    def init(self, context):
        self.inputs.new("TextureSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        # layout.operator("umog.select_texture", text = "Select Texture").pnode = self.name
        layout.prop_search(self, "texture", bpy.data, "textures", icon="TEXTURE_DATA", text="")
        if self.texture != "":       
            self.drawPreview(layout, bpy.data.textures[self.texture])


    def execute(self, refholder):
        refholder.np2dtextures[self.texture_index] = copy.deepcopy(
            refholder.np2dtextures[self.inputs[0].links[0].from_socket.texture_index])
        print(
            "setting texture " + str(self.texture_index) + " " + str(self.inputs[0].links[0].from_socket.texture_index))
        pass

    def preExecute(self, refholder):
        # consider saving the result from this
        self.texture_index = refholder.getRefForTexture2d(self.texture)