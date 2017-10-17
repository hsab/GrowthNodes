from ..node_tree import UMOGReferenceHolder
import bpy
import time

class runNodeTree(bpy.types.Operator):
    bl_idname = 'umog.run_node_tree'
    bl_label = 'Run Node Tree'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        
        start_time = time.time()

        node_tree.execute()
                
        diff_time = time.time() - start_time
        print("took " + str(diff_time))
        
        return {"FINISHED"}
