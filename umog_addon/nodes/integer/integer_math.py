from ... base_types import UMOGNode
import bpy

class IntegerMathNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_IntegerMathNode"
    bl_label = "UMOG Integer Math"

    fixed_items = bpy.props.EnumProperty(items=
                                         (('0', '+', 'addition'),
                                          ('1', '-', 'subtraction'),
                                          ('2', '*', 'multiplication'),
                                          ('3', '/', 'division'),
                                          ('4', '^', 'exponentiation'),
                                          ('5', '%', 'modulus'),
                                          ),
                                         name="fixed list")

    def init(self, context):
        self.outputs.new("IntegerSocketType", "Integer0")
        self.inputs.new("IntegerSocketType", "Integer0")
        self.inputs.new("IntegerSocketType", "Integer0")
        self.outputs[0].integer_value = 0
        super().init(context)

    def execute(self, refholder):
        if self.fixed_items == '0':
            print("addition")
            self.outputs[0].integer_value = (self.inputs[0].links[0].from_socket.integer_value +
                                             self.inputs[1].links[0].from_socket.integer_value)
        elif self.fixed_items == '1':
            print("subtraction")
            self.outputs[0].integer_value = (self.inputs[0].links[0].from_socket.integer_value -
                                             self.inputs[1].links[0].from_socket.integer_value)
        elif self.fixed_items == '2':
            print("multiplication")
            self.outputs[0].integer_value = (self.inputs[0].links[0].from_socket.integer_value *
                                             self.inputs[1].links[0].from_socket.integer_value)
        elif self.fixed_items == '3':
            print("division")
            try:
                self.outputs[0].integer_value = (self.inputs[0].links[0].from_socket.integer_value /
                                                 self.inputs[1].links[0].from_socket.integer_value)
            except:
                print("div by zero")
        elif self.fixed_items == '4':
            print("exponentiation")
            self.outputs[0].integer_value = (self.inputs[0].links[0].from_socket.integer_value ^
                                             self.inputs[1].links[0].from_socket.integer_value)
        elif self.fixed_items == '5':
            print("modulus")
            try:
                self.outputs[0].integer_value = (self.inputs[0].links[0].from_socket.integer_value %
                                                 self.inputs[1].links[0].from_socket.integer_value)
            except:
                print("mod by zero")

    def draw_buttons(self, context, layout):
        layout.prop(self, "fixed_items", 'Operation')