import bpy


class UMOGNodeEditorPanel(bpy.types.Panel):
    bl_idname = "umog_NodePanel"
    bl_label = "UMOG"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        try:
            return context.space_data.node_tree.bl_idname == "umog_UMOGNodeTree"
        except:
            return False

    def draw(self, context):
        try:
            tree = context.area.spaces.active.node_tree
            if getattr(tree, "bl_idname", "") == "umog_UMOGNodeTree":
                props = tree.properties
                self.layout.operator(
                    "umog.bake_meshes", icon='RENDER_RESULT', text="Bake Mesh(es)")
                self.layout.operator(
                    "umog.render_animation", icon='RENDER_ANIMATION', text="Render Animation")
                self.layout.prop(props, 'StartFrame')
                self.layout.label(
                    "Length: " + str(props.EndFrame - props.StartFrame))
                self.layout.prop(props, 'EndFrame')
                #self.layout.prop(props, 'SubFrames')
                self.layout.prop(props, 'TextureResolution')
        except:
            pass


# class UMOGDataPanel(bpy.types.Panel):
#     bl_idname = "umog_DataPanel"
#     bl_label = "Baked Data"
#     bl_space_type = "NODE_EDITOR"
#     bl_region_type = "TOOLS"
#     bl_category = "UMOG"
#     bl_options = {"DEFAULT_CLOSED"}

#     @classmethod
#     def poll(cls, context):
#         try:
#             return context.space_data.node_tree.bl_idname == "umog_UMOGNodeTree" and context.object.type == "MESH"
#         except:
#             return False

#     def draw(self, context):
#         # self.layout.operator("umog.animate_shapekeys",
#         #                      icon='KEYTYPE_KEYFRAME_VEC', text="Animate Keys")
#         obj = context.object
#         bakeCount = obj.bakeCount
#         bakeDict = obj.data.bakedKeys

#         # C.object.shape_key_remove(C.object.data.shape_keys.key_blocks["DISPLACE"])
#         # C.object.data.bakedKeys[1][0].value = 0

#         for list in bakeDict:
#             layout = self.layout
#             rows = 2
#             shapekeys = bakeDict[list]

#             if len(shapekeys) > 0:
#                 for shape in shapekeys:
#                     row = layout.row()
#                     split = row.split(percentage = 0.1)
#                     col = split.column()
#                     try:
#                         test = shape.name in obj.data.shape_keys.key_blocks
#                     except:
#                         pass
#                     else:
#                         name = shape.name.split("_")[-1]
#                         col.label(name)
#                         split.prop(obj.data.shape_keys.key_blocks[shape.name], 'value')
                    


            # self.prop()
            # self.layout.template_list("MESH_UL_shape_keys", "", obj.data.shape_keys,
            #                       "key_blocks", obj, "active_shape_key_index", rows=rows)
