import bpy

class EngineSocket:
    _isEngineSocket = True

    property_path = bpy.props.StringProperty()

    def init(self, context):
        pass

    def draw(self, context, layout, node, text):
        if self.property_path != "" and not self.is_output and not self.is_linked:
            layout.prop(node, self.property_path, text="value")

        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 0.5)
