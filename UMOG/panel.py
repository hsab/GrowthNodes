import bpy

################################
# START: PANEL
class HelloWorldPanel(bpy.types.Panel):
    bl_idname = "panel.panel3"
    bl_label = "UMOG"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"

    def draw(self, context):
        self.layout.operator("umog.bake_meshes", icon='RENDER_RESULT', text="Bake Mesh(es)")
        self.layout.operator("umog.add_keyframe_sample", icon='RENDER_ANIMATION', text="Render Animation")
        self.layout.prop(bpy.context.scene, 'StartFrame')
        self.layout.prop(bpy.context.scene, 'EndFrame')
        self.layout.prop(bpy.context.scene, 'SubFrames')
        self.layout.prop(bpy.context.scene, 'TextureResolution')

# END: PANEL
################################
