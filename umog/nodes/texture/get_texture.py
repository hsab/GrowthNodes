from ..umog_node import UMOGNode
from ...engine import types, engine, mesh
import bpy

class GetTextureNode(UMOGNode):
    bl_idname = "umog_GetTextureNode"
    bl_label = "Get Texture Node"

    texture_name = bpy.props.StringProperty()

    def init(self, context):
        self.outputs.new("ArraySocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "texture_name", bpy.data, "textures", icon="TEXTURE_DATA", text="")
        try:
            # only one template_preview can exist per screen area https://developer.blender.org/T46733
            # make sure that at most one preview can be opened at any time
            if self.select and (len(bpy.context.selected_nodes) == 1):
                layout.template_preview(bpy.data.textures[self.texture_name])
        except:
            pass

    def get_operation(self):
        return engine.Operation(
            engine.CONST,
            [],
            [types.Array(1, 100, 100, 1, 0, 1)],
            [types.Array(1, 100, 100, 1, 0, 1)],
            [])

    def get_buffer_values(self):
        return [mesh.array_from_texture(bpy.data.textures[self.texture_name], 100, 100)]

    def update(self):
        pass
