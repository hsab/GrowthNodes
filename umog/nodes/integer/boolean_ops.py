import bpy
from ... base_types import UMOGNode
from ... utils.events import propUpdate

class BooleanMathNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_BooleanOpshNode"
    bl_label = "Boolean Operations"

    assignedType = "Boolean"

    fixed_items = bpy.props.EnumProperty(items=(('0', 'and', 'and'),
                                                ('1', 'or', 'or'),
                                                ('2', '==', 'equals')),
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
            self.outputs[0].value = (self.inputs[0].value and self.inputs[1].value)

        elif self.fixed_items == '1':
            # Subtraction
            self.outputs[0].value = (self.inputs[0].value or self.inputs[1].value)

        elif self.fixed_items == '2':
            # Mult
            self.outputs[0].value = (self.inputs[0].value == self.inputs[1].value)

        self.outputs[0].name = str(self.outputs[0].value)

    def draw_buttons(self, context, layout):
        layout.prop(self, "fixed_items", 'Operation')
