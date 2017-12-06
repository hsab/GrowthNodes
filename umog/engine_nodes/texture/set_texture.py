from ..engine_node import *
import copy
import bpy

class SetTextureNode(bpy.types.Node, EngineOutputNode):
    bl_idname = "engine_SetTextureNode"
    bl_label = "Set Texture Node"

    texture = bpy.props.StringProperty()

    texture_index = bpy.props.IntProperty()

    def init(self, context):
        self.inputs.new("ArraySocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "texture", bpy.data, "textures", icon="TEXTURE_DATA", text="")
        try:
            # only one template_preview can exist per screen area https://developer.blender.org/T46733
            # make sure that at most one preview can be opened at any time
            if self.select and (len(bpy.context.selected_nodes) == 1):
                layout.template_preview(bpy.data.textures[self.texture])
        except:
            pass


    def execute(self, refholder):
        refholder.np2dtextures[self.texture_index] = copy.deepcopy(
            refholder.np2dtextures[self.inputs[0].links[0].from_socket.texture_index])
        print(
            "setting texture " + str(self.texture_index) + " " + str(self.inputs[0].links[0].from_socket.texture_index))
        pass

    def preExecute(self, refholder):
        # consider saving the result from this
        self.texture_index = refholder.getRefForTexture2d(self.texture)