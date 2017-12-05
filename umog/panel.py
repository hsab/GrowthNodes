import bpy

class UMOGNodeEditorPanel(bpy.types.Panel):
    bl_idname = "umog_NodePanel"
    bl_label = "UMOG"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        try:
            return context.space_data.node_tree.bl_idname == "umog_UMOGNodeTree"
        except:
            return False

    def draw(self, context):
        try:
            tree = context.area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                self.layout.operator("umog.run_node_tree", icon='RENDER_RESULT', text="Run")
        except:
            pass
