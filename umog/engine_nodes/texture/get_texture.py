from ..engine_node import *
from ...engine import types, engine, array
import bpy

class GetTextureNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_GetTextureNode"
    bl_label = "Get Texture Node"

    texture_name = bpy.props.StringProperty()
    
    resolution = 100

    def init(self, context):
        self.outputs.new("ArraySocketType", "texture")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "texture_name", bpy.data, "textures", icon="TEXTURE_DATA", text="")

        # only one template_preview can exist per screen area https://developer.blender.org/T46733
        # make sure that at most one preview can be opened at any time
        try:
            if self.select and (len(bpy.context.selected_nodes) == 1):
                layout.template_preview(self.outputs[0].getTexture())
        except:
            pass

    def execute(self, refholder):
        pass

    def preExecute(self, refholder):
        pass

    def get_operation(self, input_types):
        return engine.Operation(
            engine.CONST,
            [types.Array(4, self.resolution, self.resolution, 0, 0, 0)],
            [types.Array(4, self.resolution, self.resolution, 0, 0, 0)],
            []
            )

    def get_default_value(self, index, argument_type):
        #return array.array_from_texture(bpy.data.textures[self.texture_name], self.resolution, self.resolution)
        return bpy.data.textures[self.texture_name]
    
    def update(self):
        pass
