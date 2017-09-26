from ... base_types import UMOGOutputNode
import bpy


class SaveTextureNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SaveTextureNode"
    bl_label = "Save Texture Node"

    temp_texture_prefix = "__umog_texture_saver_"
    texture_name_temp = bpy.props.StringProperty()
    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="img")

    file_name_diff = bpy.props.IntProperty()

    texture_index = bpy.props.IntProperty()

    def init(self, context):
        self.inputs.new("TextureSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_path", text="Path")
        layout.prop(self, "file_name", text="File Name")


    def execute(self, refholder):
        refholder.handleToImage(self.inputs[0].links[0].from_socket.texture_index,
                                bpy.data.images[self.texture_name_temp])
        image = bpy.data.images[self.texture_name_temp]
        image.filepath_raw = self.file_path + self.file_name + str(self.file_name_diff) + ".png"
        image.file_format = 'PNG'
        image.save()
        self.file_name_diff = self.file_name_diff + 1
        pass

    def preExecute(self, refholder):
        self.file_name_diff = 0
        image = bpy.data.images.new(self.temp_texture_prefix + self.name, width=bpy.context.scene.TextureResolution,
                                    height=bpy.context.scene.TextureResolution)
        self.texture_name_temp = image.name
        cTex = bpy.data.textures.new(self.temp_texture_prefix + self.name, type='IMAGE')
        cTex.image = image
        print("texture name: " + self.texture_name_temp)
        pass

    def postBake(self, refholder):
        bpy.data.textures.remove(bpy.data.textures[self.texture_name_temp])
        bpy.data.images.remove(bpy.data.images[self.texture_name_temp])
        pass