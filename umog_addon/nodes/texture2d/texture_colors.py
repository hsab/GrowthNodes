import bpy
from ... base_types import UMOGNode

class TextureColorsNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_TextureColorsNode"
    bl_label = "Texture Colors"

    assignedType = "Texture2"

    def create(self):
        self.width = 220
        self.newInput(self.assignedType, "Texture")
        socket = self.newOutput(self.assignedType, "Texture")

    def draw(self, layout):
        if self.outputs[0].value != "":          
            self.drawPreview(layout, self.outputs[0].getTexture())
            
        if self.inputs[0].value is not "":
            tex = self.inputs[0].getTexture()
            layout.prop(tex, "use_color_ramp", text="Ramp")
            if tex.use_color_ramp:
                layout.template_color_ramp(tex, "color_ramp", expand=True)

            split = layout.split()

            col = split.column()
            col.label(text="RGB Multiply:")
            sub = col.column(align=True)
            sub.prop(tex, "factor_red", text="R")
            sub.prop(tex, "factor_green", text="G")
            sub.prop(tex, "factor_blue", text="B")

            col = split.column()
            col.label(text="Adjust:")
            col.prop(tex, "intensity")
            col.prop(tex, "contrast")
            col.prop(tex, "saturation")

            col = layout.column()
            col.prop(tex, "use_clamp", text="Clamp")

    def refresh(self):
        self.outputs[0].value = self.inputs[0].value
        self.outputs[0].refresh()

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