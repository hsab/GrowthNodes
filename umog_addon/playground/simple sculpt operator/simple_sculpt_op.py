import bpy
import mathutils as mt


def main(context):
    if bpy.context.area.type == 'VIEW_3D':
        bpy.ops.object.mode_set(mode = 'SCULPT')
        print("Context is SCULPT", bpy.context.mode == "SCULPT")
        print("Context is:", bpy.context.area.type)
        ctx = bpy.context.copy()
        ctx['area'] = bpy.context.area
        ctx['region'] = bpy.context.area.regions[-1]
        bpy.ops.sculpt.brush_stroke(ctx, stroke=[{
            "name": "first",
            "mouse" : (0, 0),
            "is_start": True,
            "location": (0.0422, -0.17006, 0.82477),
            "pressure": 1.0,
            'pen_flip': False,
            'time': 1.0,
            "size": 44},
            {"name": "second",
            "mouse" : (0, 0),
            "is_start": True,
            "location": (0.0422, -0.17006, 0.82477),
            "pressure": 1.0,
            'pen_flip': False,
            'time': 1.0,
            "size": 44}])
        bpy.ops.object.mode_set(mode = 'OBJECT')
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