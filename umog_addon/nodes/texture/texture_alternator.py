from ... base_types import UMOGNode

class TextureAlternatorNode(UMOGNode):
    bl_idname = "umog_TextureAlternatorNode"
    bl_label = "UMOG Texture Alternator"

    def init(self, context):
        self.inputs.new("TextureSocketType", "Texture0")
        self.inputs.new("TextureSocketType", "Texture1")
        self.inputs.new("IntegerSocketType", "Integer0")
        self.outputs.new("TextureSocketType", "Output")
        super().init(context)

    def execute(self, refholder):
        try:
            counter_index = self.inputs[2].links[0].to_socket.integer_value
        except:
            print("no integer as input")

        if (counter_index % 2) == 0:
            try:
                fn = self.inputs[0].links[0].from_socket
                self.outputs[0].texture_index = fn.texture_index
                print("use texture 0")
            except:
                print("no texture as input")
        else:
            try:
                fn = self.inputs[1].links[0].from_socket
                self.outputs[0].texture_index = fn.texture_index
                print("use texture 1")
            except:
                print("no texture as input")