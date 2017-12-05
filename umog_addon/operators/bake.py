from ..node_tree import UMOGReferenceHolder
import bpy
import time


class UMOGBakeOp(bpy.types.Operator):
    """Bakes the simulation for the frame range below."""
    bl_idname = 'umog.bake'
    bl_label = 'Bake Mesh(es)'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        
        start_time = time.time()

        refholder = UMOGReferenceHolder()
        node_tree.execute(refholder)
                
        diff_time = time.time() - start_time
        print("[UMOG] Baking process took " + str(diff_time) + " seconds.")
        
        return {"FINISHED"}
