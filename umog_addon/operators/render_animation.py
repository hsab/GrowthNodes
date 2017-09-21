from ..node_tree import UMOGReferenceHolder
import bpy

class renderAnimation(bpy.types.Operator):
    bl_idname = 'umog.render_animation'
    bl_label = 'Render Animation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        node_tree = context.space_data.edit_tree

        refholder = UMOGReferenceHolder()

        node_tree.execute(refholder, context.scene.StartFrame, context.scene.EndFrame, context.scene.SubFrames, write_keyframes=True)

        # print(frame)
        # obj.location[2] += 1.0
        # obj.keyframe_insert(data_path="location", frame=frame, index=2)

        return {'FINISHED'}
