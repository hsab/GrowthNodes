from ..node_tree import UMOGReferenceHolder
import bpy

class UMOGPopupOp(bpy.types.Operator):
    bl_idname = 'umog.popup'
    bl_label = 'UMOG: There was an issue with the nodetree!'
    bl_options = {'REGISTER', 'UNDO'}

    errType = bpy.props.StringProperty(default="ERROR")
    errMsg = bpy.props.StringProperty(default="An error occurred.")

    def execute(self, context):
        self.report({self.errType}, self.errMsg)
        return {'FINISHED'}

    def invoke(self, context, event):
         return context.window_manager.invoke_confirm(self, event)