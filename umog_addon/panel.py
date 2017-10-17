import bpy

class UMOGNodeEditorPanel(bpy.types.Panel):
    bl_idname = "umog_NodePanel"
    bl_label = "UMOG"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"

    def draw(self, context):
        self.layout.operator("umog.run_node_tree", icon='RENDER_RESULT', text="Run")
