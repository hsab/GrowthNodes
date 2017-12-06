from ... base_types import UMOGOutputNode
import bpy
import glob
import os
import re


class LoadTextureNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_LoadTextureNode"
    bl_label = "Load Texture"

    temp_texture_prefix = "__umog_texture_loader_"
    texture_name_temp = bpy.props.StringProperty()
    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="img*.png")

    file_name_diff = bpy.props.IntProperty()

    def init(self, context):
        self.outputs.new("TextureSocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_path", text="Path")
        layout.prop(self, "file_name", text="File Name")


    def execute(self, refholder):
        index = refholder.execution_scratch[self.name]["index"]
        file_list = refholder.execution_scratch[self.name]["file_list"]
        image_path = self.file_path + file_list[index]
        print(image_path)
        img = bpy.data.images.load(image_path)
        bpy.data.textures[self.texture_name_temp].image = img
        #coerce into np array
        refholder.fillTexture(self.outputs[0].texture_index, self.texture_name_temp)
        bpy.data.textures[self.texture_name_temp].image = None
        bpy.data.images.remove(img)
        print(index)
        refholder.execution_scratch[self.name]["index"] = (index + 1) % len(file_list)
        pass

    def preExecute(self, refholder):
        def tryint(s):
            try:
                return int(s)
            except:
                return s

        def alphanum_key(s):
            """ Turn a string into a list of string and number chunks.
                "z23a" -> ["z", 23, "a"]
            """
            return [ tryint(c) for c in re.split('([0-9]+)', s) ]
        pre = os.getcwd()
        os.chdir(self.file_path)
        refholder.execution_scratch[self.name] = {}
        refholder.execution_scratch[self.name]["file_list"] = glob.glob(self.file_name)
        #make sure the files are naturally sorted
        #file names with more than one set of digits may fail
        refholder.execution_scratch[self.name]["file_list"] = sorted(refholder.execution_scratch[self.name]["file_list"], key=alphanum_key)
        refholder.execution_scratch[self.name]["index"] = 0
        os.chdir(pre)
        cTex = bpy.data.textures.new(self.temp_texture_prefix + self.name, type='IMAGE')
        self.texture_name_temp = cTex.name
        self.outputs[0].texture_index = refholder.createRefForTexture2d()
        pass

    def postBake(self, refholder):
        bpy.data.textures.remove(bpy.data.textures[self.texture_name_temp])
        pass
