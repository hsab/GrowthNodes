import bpy
from bpy.props import IntProperty, CollectionProperty, StringProperty, BoolProperty
from bpy.types import Panel, UIList

class TextureListOperators(bpy.types.Operator):
    bl_idname = "umog.texture_action"
    bl_label = "Texture List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
        )
    )

    def invoke(self, context, event):
        scn = context.getActiveUMOGNodeTree()
        idx = scn.textures_index
        textures = scn.textures

        try:
            item = textures[idx]
        except IndexError:
            pass

        if self.action == 'DOWN' and idx < len(textures) - 1:
            item_next = textures[idx+1].name
            textures.move(idx, idx + 1)
            scn.textures_index += 1
            info = 'Item %d selected' % (scn.textures_index + 1)
            self.report({'INFO'}, info)

        elif self.action == 'UP' and idx >= 1:
            item_prev = textures[idx-1].name
            textures.move(idx, idx-1)
            scn.textures_index -= 1
            info = 'Item %d selected' % (scn.textures_index + 1)
            self.report({'INFO'}, info)

        return {"FINISHED"}

# -------------------------------------------------------------------
# draw
# -------------------------------------------------------------------

# custom list
class TextureListItem(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # self.use_filter_show = True
        slot = item
        tex = bpy.data.textures[item.name] if slot else None
        if tex:
             layout.prop(tex, "name", text="", emboss=False, icon_value = layout.icon(tex))
        else:
             layout.label(text="", icon_value=icon)

    def invoke(self, context, event):
        pass   

# draw the panel
class UMOGTexturePanel:
    """Creates a Panel in the Object properties window"""
    bl_label = "Texture Data"


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
        row.prop(scn.props, "ToggleTextureList", toggle=True, icon="COLLAPSEMENU", text="Show List")
        row = layout.row()
        if scn.props.ToggleTextureList:
            row.template_list("TextureListItem", "", scn, "textures", scn, "textures_index", rows=rows)
        
            col = row.column(align=True)
            col.operator("umog.texture_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("umog.texture_action", icon='TRIA_DOWN', text="").action = 'DOWN'
            col.prop(scn.props, "TexturePreviewInPanel", toggle=True, icon="IMAGE_COL", text="")
            row = layout.row()

            row = layout.row()
            row.prop(scn.props, "TexturePreviewInPanel", toggle=True, icon="IMAGE_COL", text="Toggle Preview")
            row = layout.row()
        
        if scn.props.TexturePreviewInPanel and len(scn.textures) > 0:
            row.template_preview(bpy.data.textures[scn.textures[scn.textures_index].name])
        elif len(scn.textures) > 0:
            row.separator()

        if len(scn.textures) > 0:
            texture = bpy.data.textures[scn.textures[scn.textures_index].name]
            type = texture.type

            layoutMain = layout
            layout.prop(scn.props, "ToggleTextureSettings", toggle=True, icon="FORCE_TEXTURE", text="Texture Settings")
            if scn.props.ToggleTextureSettings:
                layout = layoutMain.box()
                layout.prop(texture, "type", text="")
                if type == "CLOUDS":
                    self.drawClouds(texture, layout)
                elif type == "WOOD":
                    self.drawWood(texture, layout)
                elif type == "MARBLE":
                    self.drawMarble(texture, layout)
                elif type == "MAGIC":
                    self.drawMagic(texture, layout)            
                elif type == "BLEND":
                    self.drawBlend(texture, layout)
                elif type == "STUCCI":
                    self.drawStucci(texture, layout)
                elif type == "IMAGE":
                    self.drawImage(texture, layout)
                elif type == "ENVIRONMENT_MAP":
                    self.drawEnvironmentMap(texture, layout)
                elif type == "MUSGRAVE":
                    self.drawMusgrave(texture, layout)
                elif type == "VORONOI":
                    self.drawVoronoi(texture, layout)
                elif type == "DISTORTED_NOISE":
                    self.drawDistortedNoise(texture, layout)
                elif type == "OCEAN":
                    self.drawOcean(texture, layout)
            
            row = layoutMain.row()
            row.separator()
            layoutMain.prop(scn.props, "ToggleRampSettings", toggle=True, icon="IPO", text="Ramp Settings")
            if scn.props.ToggleRampSettings:
                layout = layoutMain.box()
                layout.prop(texture, "use_color_ramp", text="Ramp")
                if texture.use_color_ramp:
                    layout.template_color_ramp(texture, "color_ramp", expand=True)

            row = layoutMain.row()
            row.separator()
            layoutMain.prop(scn.props, "ToggleColorSettings", toggle=True, icon="COLOR", text="Color Settings")
            if scn.props.ToggleColorSettings:
                layout = layoutMain.box()
                split = layout.split()

                col = split.column()
                col.label(text="RGB Multiply:")
                sub = col.column(align=True)
                sub.prop(texture, "factor_red", text="R")
                sub.prop(texture, "factor_green", text="G")
                sub.prop(texture, "factor_blue", text="B")

                col = split.column()
                col.label(text="Adjust:")
                col.prop(texture, "intensity")
                col.prop(texture, "contrast")
                col.prop(texture, "saturation")

                col = layout.column()
                col.prop(texture, "use_clamp", text="Clamp")


    def drawBlend(self, tex, layout):
        layout.prop(tex, "progression")

        sub = layout.row()

        sub.active = (tex.progression in {'LINEAR', 'QUADRATIC', 'EASING', 'RADIAL'})
        sub.prop(tex, "use_flip_axis", expand=True)

    def drawClouds(self, tex, layout):
        layout.row().prop(tex, "cloud_type", expand=True)
        layout.label(text="Noise:")
        layout.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "noise_depth", text="Depth")

        split.prop(tex, "nabla", text="Nabla")

    def drawWood(self, tex, layout):
        layout.row().prop(tex, "noise_basis_2", expand=True)
        layout.row().prop(tex, "wood_type", expand=True)

        col = layout.column()
        col.active = tex.wood_type in {'RINGNOISE', 'BANDNOISE'}
        col.label(text="Noise:")
        col.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()
        split.active = tex.wood_type in {'RINGNOISE', 'BANDNOISE'}

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "turbulence")

        split.prop(tex, "nabla")

    def drawVoronoi(self, tex, layout):
        split = layout.split()

        col = split.column()
        col.label(text="Distance Metric:")
        col.prop(tex, "distance_metric", text="")
        sub = col.column()
        sub.active = tex.distance_metric == 'MINKOVSKY'
        sub.prop(tex, "minkovsky_exponent", text="Exponent")
        col.label(text="Coloring:")
        col.prop(tex, "color_mode", text="")
        col.prop(tex, "noise_intensity", text="Intensity")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Feature Weights:")
        sub.prop(tex, "weight_1", text="1", slider=True)
        sub.prop(tex, "weight_2", text="2", slider=True)
        sub.prop(tex, "weight_3", text="3", slider=True)
        sub.prop(tex, "weight_4", text="4", slider=True)

        layout.label(text="Noise:")
        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")
        row.prop(tex, "nabla")

    def drawStucci(self, tex, layout):
        layout.row().prop(tex, "stucci_type", expand=True)
        layout.label(text="Noise:")
        layout.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")
        row.prop(tex, "turbulence")

    def drawOcean(self, tex, layout):
        ot = tex.ocean

        col = layout.column()
        col.prop(ot, "ocean_object")
        col.prop(ot, "output")

    def drawMusgrave(self, tex, layout):
        layout.prop(tex, "musgrave_type")

        split = layout.split()

        col = split.column()
        col.prop(tex, "dimension_max", text="Dimension")
        col.prop(tex, "lacunarity")
        col.prop(tex, "octaves")

        musgrave_type = tex.musgrave_type
        col = split.column()
        if musgrave_type in {'HETERO_TERRAIN', 'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL'}:
            col.prop(tex, "offset")
        col.prop(tex, "noise_intensity", text="Intensity")
        if musgrave_type in {'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL'}:
            col.prop(tex, "gain")

        layout.label(text="Noise:")

        layout.prop(tex, "noise_basis", text="Basis")

        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")
        row.prop(tex, "nabla")

    def drawMarble(self, tex, layout):
        layout.row().prop(tex, "marble_type", expand=True)
        layout.row().prop(tex, "noise_basis_2", expand=True)
        layout.label(text="Noise:")
        layout.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "noise_depth", text="Depth")

        col = split.column()
        col.prop(tex, "turbulence")
        col.prop(tex, "nabla")

    def drawMagic(self, tex, layout):
        row = layout.row()
        row.prop(tex, "noise_depth", text="Depth")
        row.prop(tex, "turbulence")

    def drawImage(self, tex, layout):
        layout.template_image(tex, "image", tex.image_user)

    def drawEnvironmentMap(self, tex, layout):
        env = tex.environment_map

        row = layout.row()
        row.prop(env, "source", expand=True)
        row.menu("TEXTURE_MT_envmap_specials", icon='DOWNARROW_HLT', text="")

        if env.source == 'IMAGE_FILE':
            layout.template_ID(tex, "image", open="image.open")
            layout.template_image(tex, "image", tex.image_user, compact=True)
        else:
            layout.prop(env, "mapping")
            if env.mapping == 'PLANE':
                layout.prop(env, "zoom")
            layout.prop(env, "viewpoint_object")

            split = layout.split()

            col = split.column()
            col.prop(env, "layers_ignore")
            col.prop(env, "resolution")
            col.prop(env, "depth")

            col = split.column(align=True)

            col.label(text="Clipping:")
            col.prop(env, "clip_start", text="Start")
            col.prop(env, "clip_end", text="End")

    def drawDistortedNoise(self, tex, layout):
        layout.prop(tex, "noise_distortion")
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "distortion", text="Distortion")
        col.prop(tex, "noise_scale", text="Size")

        split.prop(tex, "nabla")

class UMOGTexturePanelNodeEditor(bpy.types.Panel, UMOGTexturePanel):
    bl_idname = "umog_TexturePanel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "GrowthNodes"


class UMOGTexturePanel3dView(bpy.types.Panel, UMOGTexturePanel):
    bl_category = "GrowthNodes"
    bl_idname = "umog_TexturePanel_view"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"