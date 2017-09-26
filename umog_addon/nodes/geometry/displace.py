from ... base_types import UMOGOutputNode
import bpy

class DisplaceNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_DisplaceNode"
    bl_label = "Displace Node"

    temp_texture_prefix = "__umog_internal_"

    mesh_name = bpy.props.StringProperty()
    mesh_dupl_name = bpy.props.StringProperty()

    texture_name_temp = bpy.props.StringProperty()

    mesh_name_index = bpy.props.IntProperty()

    use_subdiv = bpy.props.BoolProperty(default=True)
    mod_midlevel = bpy.props.FloatProperty(min=0.0, max=1.0, default=0.5)
    mod_strength = bpy.props.FloatProperty(default=1.0)

    def init(self, context):
        self.inputs.new("TextureSocketType", "Texture")
        super().init(context)

    def draw_buttons(self, context, layout):
        # layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")
        layout.prop(self, "use_subdiv", text="Subdivide")
        layout.prop(self, "mod_midlevel", text="Midlevel")
        layout.prop(self, "mod_strength", text="Strength")


    def execute(self, refholder):
        print("sculpt node execution, mesh: " + self.mesh_name)
        refholder.handleToImage(self.inputs[0].links[0].to_socket.texture_index,
                                bpy.data.images[self.texture_name_temp])

        obj = bpy.data.objects[self.mesh_name]

        if self.inputs["Texture"].is_linked:

            if self.use_subdiv:
                oname = "SUBDIV"
                mod = obj.modifiers.new(name=oname, type='SUBSURF')
                bpy.ops.object.modifier_apply(modifier=oname)

            oname = "DISPLACE"
            mod = obj.modifiers.new(name=oname, type='DISPLACE')
            dir(mod)
            print(self.texture_name_temp)
            mod.texture = bpy.data.textures[self.texture_name_temp]
            mod.mid_level = self.mod_midlevel
            mod.strength = self.mod_strength
            bpy.ops.object.modifier_apply(modifier=oname)
        else:
            print("no texture specified")

    def write_keyframe(self, refholder, frame):
        obj = bpy.data.objects[self.mesh_name]
        for vertex in obj.data.vertices:
            vertex.keyframe_insert(data_path='co', frame=frame)

    def preExecute(self, refholder):
        image = bpy.data.images.new(self.temp_texture_prefix + self.name, width=bpy.context.scene.TextureResolution,
                                    height=bpy.context.scene.TextureResolution)
        self.texture_name_temp = image.name
        cTex = bpy.data.textures.new(self.temp_texture_prefix + self.name, type='IMAGE')
        cTex.image = image
        print("texture name: " + self.texture_name_temp)
        pass

    def postBake(self, refholder):
        bpy.data.textures.remove(bpy.data.textures[self.texture_name_temp])
        bpy.data.images.remove(bpy.data.images[self.texture_name_temp])
        pass