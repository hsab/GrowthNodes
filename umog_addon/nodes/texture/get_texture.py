from ... base_types import UMOGNode
import bpy

class GetTextureNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_GetTextureNode"
    bl_label = "Get Texture Node"

    texture = bpy.props.StringProperty()

    def init(self, context):
        self.outputs.new("TextureSocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        # layout.operator("umog.select_texture", text = "Select Texture").pnode = self.name
        layout.prop_search(self, "texture", bpy.data, "textures", icon="TEXTURE_DATA", text="")
        try:
            # only one template_preview can exist per screen area https://developer.blender.org/T46733
            # make sure that at most one preview can be opened at any time
            if self.select and (len(bpy.context.selected_nodes) == 1):
                layout.template_preview(bpy.data.textures[self.texture])
        except:
            pass

    def update(self):
        pass

    def execute(self, refholder):
        # print("get texture node execution, texture: " + self.texture)
        # print("texture handle: " + str(self.outputs[0].texture_index))
        # print(refholder.np2dtextures[self.outputs[0].texture_index])
        pass

    def preExecute(self, refholder):
        # consider saving the result from this
        self.outputs[0].texture_index = refholder.getRefForTexture2d(self.texture)