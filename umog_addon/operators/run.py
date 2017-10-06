from ..engine import engine
import bpy
import time

class runNodeTree(bpy.types.Operator):
    bl_idname = 'umog.run_node_tree'
    bl_label = 'Run Node Tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        node_tree = context.space_data.edit_tree

        total_start_time = time.time()

        start_time = time.time()
        mesh = engine.Mesh(bpy.context.object.data)
        diff_time = time.time() - start_time
        print("mesh conversion took " + str(diff_time))

        start_time = time.time()
        texture = engine.Texture2D.from_texture(bpy.data.textures['Tex'], 100, 100)
        diff_time = time.time() - start_time
        print("texture conversion took " + str(diff_time))

        start_time = time.time()
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        engine.displace(mesh, texture)
        diff_time = time.time() - start_time
        print("displacement took " + str(diff_time))

        blender_mesh = bpy.data.meshes.new('asdf')
        obj = bpy.data.objects.new('asdf', blender_mesh)
        scn = bpy.context.scene
        scn.objects.link(obj)
        scn.objects.active = obj
        obj.select = True

        start_time = time.time()
        blender_mesh.from_pydata(*mesh.to_pydata())
        diff_time = time.time() - start_time
        print("mesh conversion took " + str(diff_time))

        total_time = time.time() - total_start_time
        print("total: " + str(total_time))

        return {'FINISHED'}
