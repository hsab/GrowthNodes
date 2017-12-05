from ..node_tree import UMOGReferenceHolder
import bpy

class UMOGSetSceneFrameRange(bpy.types.Operator):
    """Set playback/rendering frame range to simulation range"""
    bl_idname = 'umog.frame_range'
    bl_label = 'Set Scene Frame Range'
    bl_options = {'REGISTER', 'UNDO'}

    position = bpy.props.StringProperty(default="")

    def execute(self, context):
        tree = context.area.spaces.active.node_tree
        if self.position == 'start': context.scene.frame_start = tree.properties.StartFrame
        elif self.position == 'end': context.scene.frame_end =  tree.properties.EndFrame
        return {'FINISHED'}

class UMOGSetSceneCurrentFrame(bpy.types.Operator):
    """Set playback/rendering frame range to simulation range"""
    bl_idname = 'umog.frame_jump'
    bl_label = 'Set Scene Frame Range'
    bl_options = {'REGISTER', 'UNDO'}

    position = bpy.props.StringProperty(default="")

    def execute(self, context):
        tree = context.area.spaces.active.node_tree
        if self.position == 'start': context.scene.frame_current = tree.properties.StartFrame
        elif self.position == 'end': context.scene.frame_current =  tree.properties.EndFrame
        return {'FINISHED'}