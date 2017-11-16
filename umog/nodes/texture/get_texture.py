from .. import UMOGNode
from ...engine import types, engine, mesh
import bpy

class GetTextureNode(UMOGNode):
    bl_idname = "umog_GetTextureNode"
    bl_label = "Get Texture Node"
    assignedType = "Texture2"

    texture = bpy.props.StringProperty()
    texture_name = bpy.props.StringProperty()

    def create(self):
        socket = self.newOutput(
            self.assignedType, "Texture", drawOutput=True, drawLabel=False)
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def draw(self, layout):
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
