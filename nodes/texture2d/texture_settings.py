import bpy
from ... base_types import UMOGNode

class TextureSettingsNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_TextureSettingsNode"
    bl_label = "Texture Settings"

    assignedType = "Texture2"

    def create(self):
        self.width = 220
        self.newInput(self.assignedType, "Texture")
        socket = self.newOutput(self.assignedType, "Texture")

    def draw(self, layout):
        if self.outputs[0].value != "":  
            self.drawPreview(layout, self.outputs[0].getTexture())

        if self.inputs[0].value is not "":
            texture = self.outputs[0].getTexture()
            type = self.outputs[0].getTexture().type
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

    def refresh(self):
        self.outputs[0].value = self.inputs[0].value
        self.outputs[0].refresh()

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

    def execute(self, refholder):
        pass
        # try:
        #     counter_index = self.inputs[2].links[0].to_socket.integer_value
        # except:
        #     print("no integer as input")

        # if (counter_index % 2) == 0:
        #     try:
        #         fn = self.inputs[0].links[0].from_socket
        #         self.outputs[0].texture_index = fn.texture_index
        #         print("use texture 0")
        #     except:
        #         print("no texture as input")
        # else:
        #     try:
        #         fn = self.inputs[1].links[0].from_socket
        #         self.outputs[0].texture_index = fn.texture_index
        #         print("use texture 1")
        #     except:
        #         print("no texture as input")