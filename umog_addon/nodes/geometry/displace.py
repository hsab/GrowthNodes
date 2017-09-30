from ... base_types import UMOGOutputNode
import bpy


class DisplaceNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_DisplaceNode"
    bl_label = "Displace Node"

    assignedType = "Object"

    mesh_name = bpy.props.StringProperty()
    mesh_dupl_name = bpy.props.StringProperty()

    texture_name_temp = bpy.props.StringProperty()

    mesh_name_index = bpy.props.IntProperty()

    # use_subdiv = bpy.props.BoolProperty(default=True)
    mod_midlevel = bpy.props.FloatProperty(min=0.0, max=1.0, default=0.5)
    mod_strength = bpy.props.FloatProperty(default=1.0)

    def create(self):
        self.newInput(self.assignedType, "Object")
        socket = self.newInput("Texture2", "Texture")
        self.newInput("Float", "Midlevel", value=0.5)
        self.newInput("Float", "Strength", value=0.1)
        socket = self.newOutput(self.assignedType, "Output")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def refresh(self):
        self.outputs[0].value = self.inputs[0].value
        self.outputs[0].refresh()

    def execute(self, refholder):
        obj = self.inputs[0].getObject()
        texture = self.inputs[1].getTexture()
        midLevel = self.inputs[2].value
        strength = self.inputs[3].value

        # Is Object and Texture are Linked
        if self.inputs[0].is_linked and self.inputs[1].is_linked:
            oname = "DISPLACE"
            mod = obj.modifiers.new(name=oname, type='DISPLACE')
            dir(mod)
            print(self.texture_name_temp)
            mod.texture = texture
            mod.mid_level = midLevel
            mod.strength = strength
            bpy.ops.object.modifier_apply(modifier=oname, apply_as="SHAPE")

            shapekey = obj.data.shape_keys.key_blocks[-1]
            shapekey.value = 1
            bakeCount = self.nodeTree.bakeCount
            shapekey.name = \
                "baked_umog_" + \
                str(bakeCount) + \
                "_displace_" + \
                str(bpy.context.scene.frame_current)

            obj.hasUMOGBaked = True
            obj.bakeCount = bakeCount
            
            if bakeCount not in obj.data.bakedKeys:
                obj.data.bakedKeys[bakeCount] = []

            obj.data.bakedKeys[bakeCount].append(shapekey)
        else:
            print("no texture specified")

    def write_keyframe(self, refholder, frame):
        pass
        # obj = bpy.data.objects[self.mesh_name]
        # for vertex in obj.data.vertices:
        #     vertex.keyframe_insert(data_path='co', frame=frame)

    def preExecute(self, refholder):
        pass
        # image = bpy.data.images.new(self.temp_texture_prefix + self.name, width=bpy.context.scene.TextureResolution,
        #                             height=bpy.context.scene.TextureResolution)
        # self.texture_name_temp = image.name
        # cTex = bpy.data.textures.new(self.temp_texture_prefix + self.name, type='IMAGE')
        # cTex.image = image
        # print("texture name: " + self.texture_name_temp)
        # pass

    def postBake(self, refholder):
        # bpy.data.textures.remove(bpy.data.textures[self.texture_name_temp])
        # bpy.data.images.remove(bpy.data.images[self.texture_name_temp])
        pass
