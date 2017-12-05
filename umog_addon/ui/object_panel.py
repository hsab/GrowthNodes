import bpy
from bpy.props import IntProperty, CollectionProperty, StringProperty, BoolProperty
from bpy.types import Panel, UIList

class ObjectListOperators(bpy.types.Operator):
    bl_idname = "umog.object_action"
    bl_label = "Object List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
        )
    )

    def invoke(self, context, event):
        scn = context.getActiveUMOGNodeTree()
        idx = scn.objects_index
        objects = scn.objects

        try:
            item = objects[idx]
        except IndexError:
            pass

        if self.action == 'DOWN' and idx < len(objects) - 1:
            item_next = objects[idx+1].name
            objects.move(idx, idx + 1)
            scn.objects += 1
            info = 'Item %d selected' % (scn.objects + 1)
            self.report({'INFO'}, info)

        elif self.action == 'UP' and idx >= 1:
            item_prev = objects[idx-1].name
            objects.move(idx, idx-1)
            scn.objects -= 1
            info = 'Item %d selected' % (scn.objects + 1)
            self.report({'INFO'}, info)

        return {"FINISHED"}

# -------------------------------------------------------------------
# draw
# -------------------------------------------------------------------

# custom list
class ObjectListItem(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # self.use_filter_show = True
        slot = item
        obj = bpy.data.objects[item.name] if slot else None
        if obj:
             layout.prop(obj, "name", text="", emboss=False, icon_value = layout.icon(obj))
        else:
             layout.label(text="", icon_value=icon)

    def invoke(self, context, event):
        pass   

# draw the panel
class UMOGObjectPanel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "umog_ObjectPanel"
    bl_label = "Object Data & Animation"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"

    def draw(self, context):
        layout = self.layout
        scn = context.getActiveUMOGNodeTree()
        
        rows = 2
        row = layout.row()
        row.prop(scn.props, "ToggleObjectList", toggle=True, icon="COLLAPSEMENU", text="Show List")
        row = layout.row()
        if scn.props.ToggleObjectList:
            row.template_list("ObjectListItem", "", scn, "objects", scn, "objects_index", rows=rows)
        
            col = row.column(align=True)
            col.operator("umog.object_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("umog.object_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        if len(scn.objects) > 0:
            row = layout.row()

            row = layout.row()
            row.prop(scn.props, "ToggleShapeKeyList", toggle=True, icon="SHAPEKEY_DATA", text="Toggle Shapekeys")
            row = layout.row()

            if scn.props.ToggleShapeKeyList:
                rows = 4
                obj = bpy.data.objects[scn.objects[scn.objects_index].name]
                objData = obj.data
                key = objData.shape_keys
                kb = obj.active_shape_key
                
                enable_edit = obj.mode != 'EDIT'
                enable_edit_value = False

                if obj.show_only_shape_key is False:
                    if enable_edit or (obj.type == 'MESH' and obj.use_shape_key_edit_mode):
                        enable_edit_value = True

                row.template_list("MESH_UL_shape_keys", "", key, "key_blocks", obj, "active_shape_key_index", rows=rows)
                col = row.column()

                sub = col.column(align=True)
                sub.operator("object.shape_key_add", icon='ZOOMIN', text="").from_mix = False
                sub.operator("object.shape_key_remove", icon='ZOOMOUT', text="").all = False
                sub.menu("MESH_MT_shape_key_specials", icon='DOWNARROW_HLT', text="")

                sub = col.column(align=True)
                sub.operator("object.shape_key_move", icon='TRIA_UP', text="").type = 'UP'
                sub.operator("object.shape_key_move", icon='TRIA_DOWN', text="").type = 'DOWN'

                split = layout.split(percentage=0.4)
                row = split.row()
                row.enabled = enable_edit
                row.prop(key, "use_relative")

                row = split.row()
                row.alignment = 'RIGHT'

                sub = row.row(align=True)
                sub.label()  # XXX, for alignment only
                subsub = sub.row(align=True)
                subsub.active = enable_edit_value
                subsub.prop(obj, "show_only_shape_key", text="")
                sub.prop(obj, "use_shape_key_edit_mode", text="")

                sub = row.row()
                if key.use_relative:
                    sub.operator("object.shape_key_clear", icon='X', text="")
                else:
                    sub.operator("object.shape_key_retime", icon='RECOVER_LAST', text="")

                if key.use_relative:
                    if obj.active_shape_key_index != 0:
                        row = layout.row()
                        row.active = enable_edit_value
                        row.prop(kb, "value")

                        split = layout.split()

                        col = split.column(align=True)
                        col.active = enable_edit_value
                        col.label(text="Range:")
                        col.prop(kb, "slider_min", text="Min")
                        col.prop(kb, "slider_max", text="Max")

                        col = split.column(align=True)
                        col.active = enable_edit_value
                        col.label(text="Blend:")
                        col.prop_search(kb, "vertex_group", obj, "vertex_groups", text="")
                        col.prop_search(kb, "relative_key", key, "key_blocks", text="")

                else:
                    layout.prop(kb, "interpolation", expand=True)
                    row = layout.column()
                    row.active = enable_edit_value
                    row.prop(key, "eval_time")
        # if len(scn.textures) > 0:
        #     texture = bpy.data.textures[scn.textures[scn.textures_index].name]
        #     type = texture.type

        #     layoutMain = layout
        #     layout.prop(scn.props, "ToggleTextureSettings", toggle=True, icon="FORCE_TEXTURE", text="Texture Settings")
        #     if scn.props.ToggleTextureSettings:
        #         layout = layoutMain.box()
        #         layout.prop(texture, "type", text="")
        #         if type == "CLOUDS":
        #             self.drawClouds(texture, layout)
        #         elif type == "WOOD":
        #             self.drawWood(texture, layout)
        #         elif type == "MARBLE":
        #             self.drawMarble(texture, layout)
        #         elif type == "MAGIC":
        #             self.drawMagic(texture, layout)            
        #         elif type == "BLEND":
        #             self.drawBlend(texture, layout)
        #         elif type == "STUCCI":
        #             self.drawStucci(texture, layout)
        #         elif type == "IMAGE":
        #             self.drawImage(texture, layout)
        #         elif type == "ENVIRONMENT_MAP":
        #             self.drawEnvironmentMap(texture, layout)
        #         elif type == "MUSGRAVE":
        #             self.drawMusgrave(texture, layout)
        #         elif type == "VORONOI":
        #             self.drawVoronoi(texture, layout)
        #         elif type == "DISTORTED_NOISE":
        #             self.drawDistortedNoise(texture, layout)
        #         elif type == "OCEAN":
        #             self.drawOcean(texture, layout)
            
        #     row = layoutMain.row()
        #     row.separator()
        #     layoutMain.prop(scn.props, "ToggleRampSettings", toggle=True, icon="IPO", text="Ramp Settings")
        #     if scn.props.ToggleRampSettings:
        #         layout = layoutMain.box()
        #         layout.prop(texture, "use_color_ramp", text="Ramp")
        #         if texture.use_color_ramp:
        #             layout.template_color_ramp(texture, "color_ramp", expand=True)

        #     row = layoutMain.row()
        #     row.separator()
        #     layoutMain.prop(scn.props, "ToggleColorSettings", toggle=True, icon="COLOR", text="Color Settings")
        #     if scn.props.ToggleColorSettings:
        #         layout = layoutMain.box()
        #         split = layout.split()

        #         col = split.column()
        #         col.label(text="RGB Multiply:")
        #         sub = col.column(align=True)
        #         sub.prop(texture, "factor_red", text="R")
        #         sub.prop(texture, "factor_green", text="G")
        #         sub.prop(texture, "factor_blue", text="B")

        #         col = split.column()
        #         col.label(text="Adjust:")
        #         col.prop(texture, "intensity")
        #         col.prop(texture, "contrast")
        #         col.prop(texture, "saturation")

        #         col = layout.column()
        #         col.prop(texture, "use_clamp", text="Clamp")