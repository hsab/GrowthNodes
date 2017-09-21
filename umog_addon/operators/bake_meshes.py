from ..node_tree import UMOGReferenceHolder
import bpy
import time


class bakeMeshes(bpy.types.Operator):
    bl_idname = 'umog.bake_meshes'
    bl_label = 'Bake Mesh(es)'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        
        start_time = time.time()

        refholder = UMOGReferenceHolder()
        node_tree.execute(refholder, context.scene.StartFrame, context.scene.EndFrame, context.scene.SubFrames)
                
        diff_time = time.time() - start_time
        print("the bake took " + str(diff_time))
        
        return {"FINISHED"}
