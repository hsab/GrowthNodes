from ..node_tree import UMOGReferenceHolder
import bpy
import time


class UMOGBakeOp(bpy.types.Operator):
    """Bakes the simulation for the frame range below."""
    bl_idname = 'umog.bake'
    bl_label = 'Bake Mesh(es)'
    bl_options = {"REGISTER", "UNDO"}

    tree : bpy.props.StringProperty()

    def execute(self, context):
        # test = self.tree
        node_tree = bpy.data.node_groups[self.tree]
        
        start_time = time.time()

        refholder = UMOGReferenceHolder()
        node_tree.execute(refholder)
                
        diff_time = time.time() - start_time
        print("[GrowthNodes] Baking process took " + str(diff_time) + " seconds.")
        
        return {"FINISHED"}
