import bpy
import mathutils as mt

def main(context):
    if bpy.context.area.type == 'VIEW_3D':
        obj = context.active_object
        v = obj.data.vertices[0]
        co_final = obj.matrix_world * v.co
        obj_empty = bpy.data.objects.new("Test", None)
        context.scene.objects.link(obj_empty)
        obj_empty.location = co_final
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.normals_make_consistent()
        
        bpy.ops.object.mode_set(mode = 'SCULPT')
        print("Context is:", bpy.context.area.type)
        print("Mode changed to ", bpy.context.mode == "SCULPT")
        
        bpy.data.brushes["SculptDraw"].stroke_method = "DOTS"
        bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False

        if not context.sculpt_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()
            bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
            bpy.context.scene.tool_settings.sculpt.constant_detail = 1.5

        
        ctx = bpy.context.copy()
        ctx['area'] = bpy.context.area
        ctx['region'] = bpy.context.area.regions[-1]
        
        verts = list(obj.data.vertices)
        
        for vert in verts:
            bpy.ops.sculpt.brush_stroke(ctx, stroke=[{
                "name": "first",
                "mouse" : (250 , 250),
                "is_start": True,
                "location": obj.matrix_world * vert.co,
                "pressure": 1.0,
                'pen_flip': False,
                'time': 1.0,
                "size": 44}])
#        bpy.ops.object.mode_set(mode = 'OBJECT')
        print("ALL GOOD!")


class SimpleOperator(bpy.types.Operator):
    '''Tooltip'''
    bl_idname = "object.simple_operator"
    bl_label = "Simple Sculpt Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()