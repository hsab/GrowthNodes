from ..umog_node import *
from ...engine import types, engine, mesh, alembic, data
import bpy
import bmesh

class SetMeshNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SetMeshNode"
    bl_label = "Set Mesh Node"

    mesh_name = bpy.props.StringProperty()

    def init(self, context):
        self.inputs.new("MeshSocketType", "mesh")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "mesh_name", bpy.data, "meshes", icon="MESH_CUBE", text="")

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.MESH)

        return engine.Operation(
            engine.OUT,
            input_types,
            [],
            [])

    def output_value(self, value):
        bmesh.new().to_mesh(bpy.data.meshes[self.mesh_name])
        if isinstance(value, mesh.Mesh):
            mesh.to_blender_mesh(value, bpy.data.meshes[self.mesh_name])
            bpy.data.meshes[self.mesh_name].update(calc_edges=True)
        elif isinstance(value, mesh.MeshSequence):
            print("alembic export")
            filename = "//" + self.mesh_name + ".abc"
            users = []
            for obj in bpy.data.objects:
                if obj.type == "MESH" and obj.data == bpy.data.meshes[self.mesh_name]:
                    users.append(obj)
                    for modifier in obj.modifiers:
                        if modifier.type == "MESH_SEQUENCE_CACHE":
                            obj.modifiers.remove(modifier)

            alembic.export_mesh_sequence(value, bytes(bpy.path.abspath(filename), "UTF8"))

            bpy.ops.cachefile.open(filepath=filename)
            for c in bpy.data.cache_files:
                print(c.filepath)
                if c.filepath == filename:
                    cachefile = c
            for obj in users:
                mod = obj.modifiers.new("MeshSequenceCache", "MESH_SEQUENCE_CACHE")
                mod.cache_file = cachefile
                mod.object_path = "/mesh"

    def update(self):
        pass
