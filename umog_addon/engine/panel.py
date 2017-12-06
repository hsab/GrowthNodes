import bpy

class EngineNodeEditorPanel(bpy.types.Panel):
    bl_idname = "engine_NodePanel"
    bl_label = "Engine"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Engine"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        try:
            return context.space_data.node_tree.bl_idname == "engine_EngineNodeTree"
        except:
            return False

    def draw(self, context):
        try:
            tree = context.area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "engine_EngineNodeTree":
                self.layout.operator("engine.run_node_tree", icon='RENDER_RESULT', text="Run")
        except:
            pass
