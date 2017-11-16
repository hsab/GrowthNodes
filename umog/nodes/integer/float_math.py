import bpy
from .. import UMOGNode
from ... utils.events import propUpdate

class FloatMathNode(UMOGNode):
    bl_idname = "umog_FloatMathNode"
    bl_label = "Float Math"

    assignedType = "Float"

    fixed_items = bpy.props.EnumProperty(items=(('0', '+', 'addition'),
                                                ('1', '-', 'subtraction'),
                                                ('2', '*', 'multiplication'),
                                                ('3', '/', 'division'),
                                                ('4', '^', 'exponentiation'),
                                                ('5', '%', 'modulus'),
                                                ),
                                         name="fixed list",
                                         update = propUpdate)

    def init(self, context):
        self.newInput(self.assignedType, "A")
        self.newInput(self.assignedType, "B")
        self.newOutput(self.assignedType, "Result")

    def refresh(self):
        self.applyOperation()

    def execute(self, refholder):
        self.applyOperation()
    
    def applyOperation(self):
        if self.fixed_items == '0':
            # Addition
            self.outputs[0].value = self.inputs[0].value + self.inputs[1].value

        elif self.fixed_items == '1':
            # Subtraction
            self.outputs[0].value = self.inputs[0].value - self.inputs[1].value

        elif self.fixed_items == '2':
            # Mult
            self.outputs[0].value = self.inputs[0].value * self.inputs[1].value

        elif self.fixed_items == '3':
            # Div
            try:
                self.outputs[0].value = self.inputs[0].value / self.inputs[1].value
            except:
                print("div by zero")

        elif self.fixed_items == '4':
            # Expo
            self.outputs[0].value = self.inputs[0].value ^ self.inputs[1].value

        elif self.fixed_items == '5':
            # Mod
            try:
                self.outputs[0].value = self.inputs[0].value % self.inputs[1].value
            except:
                print("mod by zero")

        self.outputs[0].name = "{:.5f}".format(self.outputs[0].value)

    def draw_buttons(self, context, layout):
        layout.prop(self, "fixed_items", 'Operation')
