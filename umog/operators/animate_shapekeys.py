from ..node_tree import UMOGReferenceHolder
import bpy
import time


class animateShapeKeys(bpy.types.Operator):
    bl_idname = 'umog.animate_shapekeys'
    bl_label = 'Animate Shapekeys'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        
        start_time = time.time()

        refholder = UMOGReferenceHolder()
        node_tree.execute(refholder)
                
        diff_time = time.time() - start_time
        print("the bake took " + str(diff_time))
        
        return {"FINISHED"}
