import bpy
from ... base_types import UMOGNode
from ... utils.events import propUpdate


class IntegerMathNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_IntegerMathNode"
    bl_label = "Integer Math"

    assignedType = "Integer"

    fixed_items = bpy.props.EnumProperty(items=(('0', '+', 'addition'),
                                                ('1', '-', 'subtraction'),
                                                ('2', '*', 'multiplication'),
                                                ('3', '/', 'division'),
                                                ('4', '^', 'exponentiation'),
                                                ('5', '%', 'modulus'),
                                                ),
                                         name="fixed list",
                                         update = propUpdate)

    def create(self):
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

        self.outputs[0].name = str(self.outputs[0].value)

    def draw(self, layout):
        layout.prop(self, "fixed_items", 'Operation')
