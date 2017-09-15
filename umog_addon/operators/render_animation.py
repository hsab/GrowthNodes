from .. nodetree import UMOGReferenceHolder
import bpy

class renderAnimation(bpy.types.Operator):
    bl_idname = 'umog.render_animation'
    bl_label = 'Render Animation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        for frame in range(context.scene.StartFrame, context.scene.EndFrame + 1):
            print(frame)
            bpy.context.space_data.edit_tree.execute(UMOGReferenceHolder())
            obj.location[2] += 1.0
            obj.keyframe_insert(data_path="location", frame=frame, index=2)

        return {'FINISHED'}
