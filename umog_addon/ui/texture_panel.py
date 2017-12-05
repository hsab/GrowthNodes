import bpy
from bpy.props import IntProperty, CollectionProperty, StringProperty 
from bpy.types import Panel, UIList

class TextureListOperators(bpy.types.Operator):
    bl_idname = "umog.texture_action"
    bl_label = "Texture List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
        )
    )

    def invoke(self, context, event):
        scn = context.getActiveUMOGNodeTree()
        idx = scn.textures_index
        textures = scn.textures

        try:
            item = textures[idx]
        except IndexError:
            pass

        if self.action == 'DOWN' and idx < len(textures) - 1:
            item_next = textures[idx+1].name
            textures.move(idx, idx + 1)
            scn.textures_index += 1
            info = 'Item %d selected' % (scn.textures_index + 1)
            self.report({'INFO'}, info)

        elif self.action == 'UP' and idx >= 1:
            item_prev = textures[idx-1].name
            textures.move(idx, idx-1)
            scn.textures_index -= 1
            info = 'Item %d selected' % (scn.textures_index + 1)
            self.report({'INFO'}, info)

        return {"FINISHED"}

# -------------------------------------------------------------------
# draw
# -------------------------------------------------------------------

# custom list
class TextureListItem(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show = True
        slot = item
        tex = bpy.data.textures[item.name] if slot else None
        if tex:
             layout.prop(tex, "name", text="", emboss=False, icon_value = layout.icon(tex))
        else:
             layout.label(text="", icon_value=icon)

    def invoke(self, context, event):
        pass   

# draw the panel
class UMOGTexturePanel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "umog_TexturePanel"
    bl_label = "Textures"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"

    def draw(self, context):
        layout = self.layout
        scn = context.getActiveUMOGNodeTree()
        
        rows = 8
        row = layout.row()
        row.template_list("TextureListItem", "", scn, "textures", scn, "textures_index", rows=rows)

        col = row.column(align=True)
        col.operator("umog.texture_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("umog.texture_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()


# Create custom property group
class CustomProp(bpy.types.PropertyGroup):
    name = StringProperty()
    id = IntProperty()
    texture = StringProperty()

# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------

def register():
    bpy.types.NodeTree.textures = CollectionProperty(type=CustomProp)
    bpy.types.NodeTree.textures_index = IntProperty()

def unregister():
    del bpy.types.NodeTree.textures
    del bpy.types.NodeTree.textures_index

if __name__ == "__main__":
    register()