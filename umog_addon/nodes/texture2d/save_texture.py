from ... base_types import UMOGNode
import bpy
import numpy as np


class SaveTextureNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_SaveTextureNode"
    bl_label = "Save Texture"

    assignedType = "Texture2"

    temp_texture_prefix = "__umog_texture_saver_"
    texture_name_temp = bpy.props.StringProperty()

    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="img")

    file_name_diff = bpy.props.IntProperty()

    texture_index = bpy.props.IntProperty()

    def create(self):
        socket = self.newInput(self.assignedType, "Texture")
        socket.drawLabel = False

    def draw(self, layout):
        layout.prop(self, "file_path", text="Path")
        layout.prop(self, "file_name", text="File Name")


    def execute(self, refholder):
        try:
            texture = self.inputs[0].getFromSocket.getTexture()
            image = texture.image
            # image.update()
            # nparr = np.asarray(image.pixels, dtype="float")
            # nparr = nparr.reshape(image.size[0], image.size[0], 4)

            # test = bpy.data.images.new("test", image.size[0], image.size[0], alpha = False, float_buffer = True)
            # test.pixels = nparr.flatten()

            image.filepath_raw = self.file_path + self.file_name + str(self.file_name_diff) + ".png"
            image.file_format = 'PNG'
            image.save()
        except:
            resolution = self.nodeTree.properties.TextureResolution
            pixels = np.empty((resolution, resolution, 4), dtype = "float")
            texture = self.inputs[0].getFromSocket.getTexture()
            self.inputs[0].proceduralToNumpy(texture, pixels, resolution, resolution)
            image = bpy.data.images.new("temp", resolution, resolution, alpha = False,
                             float_buffer = True)
            image.pixels = pixels.flatten()
            image.update()
            image.filepath_raw = self.file_path + self.file_name + str(self.file_name_diff) + ".png"
            image.file_format = 'PNG'
            image.save()
            bpy.data.images.remove(image)
        # print(image.source == test.source)

        self.file_name_diff = self.file_name_diff + 1
        pass

    def preExecute(self, refholder):
        self.file_name_diff = 0
        # image = bpy.data.images.new(self.temp_texture_prefix + self.name, width=bpy.context.scene.TextureResolution,
        #                             height=bpy.context.scene.TextureResolution)
        # self.texture_name_temp = image.name
        # cTex = bpy.data.textures.new(self.temp_texture_prefix + self.name, type='IMAGE')
        # cTex.image = image
        # print("texture name: " + self.texture_name_temp)
        pass

    def postBake(self, refholder):
        # bpy.data.textures.remove(bpy.data.textures[self.texture_name_temp])
        # bpy.data.images.remove(bpy.data.images[self.texture_name_temp])
        pass