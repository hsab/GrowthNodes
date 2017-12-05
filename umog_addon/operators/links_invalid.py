from ..node_tree import UMOGReferenceHolder
import bpy

class invalidLinksPopop(bpy.types.Operator):
    bl_idname = 'umog.invalid_links'
    bl_label = 'UMOG has found invalid links.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'ERROR'}, "Node-tree contains links with mismatched types. These are highlighted in red.")
        return {'FINISHED'}

    def invoke(self, context, event):
         return context.window_manager.invoke_confirm(self, event)