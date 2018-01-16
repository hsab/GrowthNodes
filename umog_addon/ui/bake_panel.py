import bpy
import math

class UMOGBakePanel:
    bl_label = "Bake Properties"

    @classmethod
    def poll(cls, context):
        try:
            for window in bpy.context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'NODE_EDITOR':
                        space_data = area.spaces.active
                        return space_data.node_tree.bl_idname == "umog_UMOGNodeTree"
        except:
            return False

    def draw(self, context):
        try:
            for window in bpy.context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'NODE_EDITOR':
                        tree = area.spaces.active.node_tree
                        snode = area.spaces.active
            scene = context.scene
            screen = context.screen
            # snode = context.space_data
            layout = self.layout
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
            # if True:
                props = tree.properties
                totalFrames = props.EndFrame - props.StartFrame

                row = layout.row()
                row.scale_y = 1.5
                row.operator("umog.bake", icon='FORCE_LENNARDJONES', text="Bake Nodetree")
                row = layout.row()
                row.template_ID(snode, "node_tree", new="node.new_node_tree")
                row = layout.row()
                row.separator()
                layout.prop(props, "ShowFrameSettings", toggle=True, icon="MOD_WIREFRAME", text="Bake Settings")
                if props.ShowFrameSettings:
                    box = layout.box()
                    col = box.column(align=True)
                    row = col.row(align=True).split(percentage=1/6, align=True)
                    scol = row.column(align=True)
                    scol.scale_y = 2
                    scol.operator("umog.frame_range", text="", icon='KEYTYPE_MOVING_HOLD_VEC').position = 'start'
                    row = row.split(percentage=5/6, align=True)
                    scol = row.column(align=True)
                    scol.scale_y = 1
                    scol.prop(props, 'StartFrame', text="Bake Start")
                    scol.prop(props, 'EndFrame', text="Bake End")
                    row = row.split(align=True)
                    scol = row.column(align=True)
                    scol.scale_y = 2
                    scol.operator("umog.frame_range", text="", icon='KEYTYPE_MOVING_HOLD_VEC').position = 'end'
                    #===================
                    #Play Buttons
                    row = col.row(align=True).split(align=True)
                    row.operator("screen.frame_jump", text="", icon='REW').end = False
                    row.operator("umog.frame_jump", text="", icon='PREV_KEYFRAME').position = 'start'
                    if not screen.is_animation_playing:
                        # if using JACK and A/V sync hide the play-reversed button since JACK transport doesn't support reversed playback
                        if scene.sync_mode == 'AUDIO_SYNC' and context.user_preferences.system.audio_device == 'JACK':
                            row.operator("screen.animation_play", text="", icon='PLAY')
                        else:
                            row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
                            row.operator("screen.animation_play", text="", icon='PLAY')
                    else:
                        row.operator("screen.animation_play", text="", icon='PAUSE')
                    row.operator("umog.frame_jump", text="", icon='NEXT_KEYFRAME').position = 'end'
                    row.operator("screen.frame_jump", text="", icon='FF').end = True
                    col.prop(scene, "frame_current", text="Current Frame")
                    #===================
                    #Total Frames
                    row = box.row(align=True)
                    split = row.split(percentage=0.7)
                    left_side = split.column(align=True)
                    left_side.label("Total Frames:", icon='PHYSICS')
                    right_side = split.column()
                    right_side.alignment = 'RIGHT'
                    right_side.label(str(totalFrames))
                    #===================
                    #FPS
                    row = box.row(align=True)
                    split = row.split(percentage=0.7)
                    left_side = split.column(align=True)
                    left_side.label("FPS:", icon='SEQUENCE')
                    right_side = split.column()
                    right_side.alignment = 'RIGHT'
                    right_side.label(str(scene.render.fps))
                    #===================
                    #Total Time
                    row = box.row(align=True)
                    split = row.split(percentage=0.7)
                    left_side = split.column(align=True)
                    left_side.label("Total Seconds:", icon='TIME')
                    right_side = split.column()
                    right_side.alignment = 'RIGHT'
                    right_side.label(str(totalFrames / scene.render.fps))
                    #===================
                    #Texture Resolution
                    row = box.row(align=True)
                    # row = col.row(align=True).split(align=True)
                    # split = row.split(percentage=0.7)
                    # left_side = split.column(align=True)
                    row.label("Texture Resolution:", icon='RENDER_REGION')
                    row = box.row(align=True)
                    row.prop(props, 'TextureResolution', text="")
                
        except:
            pass

class UMOGBakePanelNodeEditor(bpy.types.Panel, UMOGBakePanel):
    bl_category = "GrowthNodes"
    bl_idname = "umog_NodePanel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"

class UMOGBakePanel3dView(bpy.types.Panel, UMOGBakePanel):
    bl_category = "GrowthNodes"
    bl_idname = "umog_NodePanel_view"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    
