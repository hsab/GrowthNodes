import bpy

class UMOGNodeEditorPanel(bpy.types.Panel):
    bl_idname = "umog_NodePanel"
    bl_label = "UMOG"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"

    def draw(self, context):
        self.layout.operator("umog.bake_meshes", icon='RENDER_RESULT', text="Bake Mesh(es)")
        self.layout.operator("umog.render_animation", icon='RENDER_ANIMATION', text="Render Animation")
        self.layout.operator("umog.run_node_tree", icon='RENDER_ANIMATION', text="Run")
        self.layout.prop(bpy.context.scene, 'StartFrame')
        self.layout.prop(bpy.context.scene, 'EndFrame')
        self.layout.prop(bpy.context.scene, 'SubFrames')
        self.layout.prop(bpy.context.scene, 'TextureResolution')

