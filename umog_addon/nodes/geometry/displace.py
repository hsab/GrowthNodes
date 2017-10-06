from ..output_node import UMOGOutputNode
import bpy

class DisplaceNode(UMOGOutputNode):
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

    def update(self):
        pass

    def execute(self, refholder):
        print("sculpt node execution, mesh: " + self.mesh_name)
        refholder.handleToImage(self.inputs[0].links[0].to_socket.texture_index,
                                bpy.data.images[self.texture_name_temp])

        obj = bpy.data.objects[self.mesh_name]
        texture = bpy.data.textures[self.texture_name_temp]

        if self.inputs["Texture"].is_linked:

            # if self.use_subdiv:
            #     oname = "SUBDIV"
            #     mod = obj.modifiers.new(name=oname, type='SUBSURF')
            #     bpy.ops.object.modifier_apply(modifier=oname)

            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            bpy.context.scene.objects.link(new_obj)
            bpy.context.scene.objects.active = new_obj
            new_obj.select = True

            if new_obj.data.shape_keys is not None:
                for k in new_obj.data.shape_keys.key_blocks:
                    new_obj.shape_key_remove(k)

            oname = 'DISPLACE'
            mod = new_obj.modifiers.new(name=oname, type='DISPLACE')
            mod.texture = texture
            mod.mid_level = self.mod_midlevel
            mod.strength = self.mod_strength
            bpy.ops.object.modifier_apply(modifier=oname)

            bpy.context.scene.objects.active = obj
            obj.select = False
            new_obj.select = True
            bpy.ops.object.join_shapes()

            bpy.context.scene.objects.active = new_obj
            obj.select = False
            bpy.ops.object.delete()

            obj.active_shape_key_index = len(obj.data.shape_keys.key_blocks) - 1
            obj.select = True
        else:
            print("no texture specified")

    def write_keyframe(self, refholder, frame):
        obj = bpy.data.objects[self.mesh_name]
        if obj.data.shape_keys is not None and len(obj.data.shape_keys.key_blocks) > 0:
            obj.data.shape_keys.key_blocks[-1].value = 1.0
            obj.data.shape_keys.key_blocks[-1].keyframe_insert("value", frame=frame)
            obj.data.shape_keys.key_blocks[-1].value = 0.0
            obj.data.shape_keys.key_blocks[-1].keyframe_insert("value", frame=frame - 1)
            obj.data.shape_keys.key_blocks[-1].keyframe_insert("value", frame=frame + 1)

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