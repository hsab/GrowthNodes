from ..engine_node import *
import bpy
import numpy as np


class SaveTextureNode(bpy.types.Node, EngineOutputNode):
    bl_idname = "engine_SaveTextureNode"
    bl_label = "Save Texture"

    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="img")

    # file_name_diff = bpy.props.IntProperty()

    def init(self, context):
        socket = self.inputs.new("ArraySocketType", "texture")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_path", text="Path")
        layout.prop(self, "file_name", text="File Name")

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.OUT,
            input_types,
            [],
            [])

    def output_value(self, value):
        array = value.array
        img = bpy.data.images.new('', array.shape[1], array.shape[2], alpha=True, float_buffer=True)
        img.pixels = np.ravel(value.array, 'F')
        img.filepath_raw = self.file_path + self.file_name + ".png"
        img.file_format = 'PNG'
        img.save()

        # texture = bpy.data.textures.new(self.file_name, type="IMAGE")
        # texture.image = img

    def execute(self, refholder):
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

        # self.file_name_diff = self.file_name_diff + 1
        pass
