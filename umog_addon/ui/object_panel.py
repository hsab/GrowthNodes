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
class UMOGObjectPanel:
    """Creates a Panel in the Object properties window"""
    bl_label = "Object Data & Animation"

    @classmethod
    def poll(cls, context):
        try:
            for window in bpy.context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'NODE_EDITOR':
                        space_data = area.spaces.active
                        return space_data.node_tree.bl_idname == "umog_UMOGNodeTree"
        except:
            return False

    def draw(self, context):
        try:
            for window in bpy.context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'NODE_EDITOR':
                        scn = area.spaces.active.node_tree
            # scn = context.getActiveUMOGNodeTree()
            test = scn.props
        except:
            return 

        if getattr(scn, "bl_idname", "") == "umog_UMOGNodeTree":
            layout = self.layout
        else:
            return


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
            row.prop(scn.props, "ToggleShapeKeyList", toggle=True, icon="SHAPEKEY_DATA", text="Shapekeys")
            row = layout.row()

            obj = bpy.data.objects[scn.objects[scn.objects_index].name]
            objData = obj.data
            key = objData.shape_keys
            kb = obj.active_shape_key

            if scn.props.ToggleShapeKeyList:
                rows = 4
                
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

                sub.operator("object.shape_key_move", icon='TRIA_UP', text="").type = 'UP'
                sub.operator("object.shape_key_move", icon='TRIA_DOWN', text="").type = 'DOWN'
                sub.menu("MESH_MT_shape_key_specials", icon='DOWNARROW_HLT', text="")

                if kb:
                    box = layout.box()
                    split = box.split(percentage=0.4)
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
                            row = box.row()
                            row.active = enable_edit_value
                            row.prop(kb, "value")

                            split = box.split()

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
                        row = box.row()
                        row.prop(kb, "interpolation", expand=True)
                        row = box.column()
                        row.active = enable_edit_value
                        row.prop(key, "eval_time")
                        
                row = layout.row()
            

            group = obj.vertex_groups.active

            row.separator()
            row = layout.row()
            row.prop(scn.props, "ToggleVertexGroupList", toggle=True, icon="GROUP_VERTEX", text="Vertex Groups")
            row = layout.row()
            if scn.props.ToggleVertexGroupList:
                    row.template_list("MESH_UL_vgroups", "", obj, "vertex_groups", obj.vertex_groups, "active_index", rows=rows)
                    col = row.column(align=True)
                    col.operator("object.vertex_group_add", icon='ZOOMIN', text="")
                    col.operator("object.vertex_group_remove", icon='ZOOMOUT', text="").all = False
                    if group:
                        col.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
                        col.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
                    col.menu("MESH_MT_vertex_group_specials", icon='DOWNARROW_HLT', text="")

                    if obj.vertex_groups and (obj.mode == 'EDIT' or (obj.mode == 'WEIGHT_PAINT' and obj.type == 'MESH' and obj.data.use_paint_mask_vertex)):
                        row = layout.row()

                        sub = row.row(align=True)
                        sub.operator("object.vertex_group_assign", text="Assign")
                        sub.operator("object.vertex_group_remove_from", text="Remove")

                        sub = row.row(align=True)
                        sub.operator("object.vertex_group_select", text="Select")
                        sub.operator("object.vertex_group_deselect", text="Deselect")

                        layout.prop(context.tool_settings, "vertex_group_weight", text="Weight")

class UMOGObjectPanelNodeEditor(bpy.types.Panel, UMOGObjectPanel):
    bl_idname = "umog_ObjectPanel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "GrowthNodes"


class UMOGObjectPanel3dView(bpy.types.Panel, UMOGObjectPanel):
    bl_category = "GrowthNodes"
    bl_idname = "umog_ObjectPanel_view"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"