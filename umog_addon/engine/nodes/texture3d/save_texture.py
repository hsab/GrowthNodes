from ..engine_node import *
import bpy
import numpy as np




class SaveTexture3dNode(bpy.types.Node, EngineOutputNode):
    bl_idname = "engine_SaveTexture3dNode"
    bl_label = "Save Texture 3d"

    temp_texture_prefix = "__engine_texture_saver_"

    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="img")

    file_name_diff = bpy.props.IntProperty()


    def init(self, context):
        socket = self.inputs.new("ArraySocketType", "texture")
        socket.drawLabel = False
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
        array = np.squeeze(array)
        self.file_name_diff = 0
        
        image = bpy.data.images.new(self.temp_texture_prefix + self.name, array.shape[0], array.shape[1], alpha = False, float_buffer = True)
        
        tex3d = array
        print(str(tex3d.shape))
        for i in range(array.shape[2]):
            slc = tex3d[:,:,i]
            ti = np.ones((array.shape[0], array.shape[1], 4), dtype="float")
            ti[:,:,0] = slc
            ti[:,:,1] = slc
            ti[:,:,2] = slc
            #.tolist()
            image.pixels = ti.flatten()
            image.update()
            
            image.filepath_raw = self.file_path + self.file_name + str(self.file_name_diff) + "_" + str(i) + ".png"
            image.file_format = 'PNG'
            image.save()
            # image.update()
            # nparr = np.asarray(image.pixels, dtype="float")
            # nparr = nparr.reshape(image.size[0], image.size[0], 4)

            # test = bpy.data.images.new("test", image.size[0], image.size[0], alpha = False, float_buffer = True)
            # test.pixels = nparr.flatten()

            # print(image.source == test.source)
        
        bpy.data.images.remove(image)

        self.file_name_diff = self.file_name_diff + 1
        pass

        

