import bpy
from ... base_types import UMOGNode
from ... utils.events import propUpdate

class IntegerCompareNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_IntegerCompareNode"
    bl_label = "Integer Compare"

    assignedType = "Integer"

    fixed_items = bpy.props.EnumProperty(items=(('0', '>', 'bigger'),
                                                ('1', '>=', 'bigger_eq'),
                                                ('2', '<', 'less'),
                                                ('3', '<=', 'less_eq'),
                                                ('4', '==', 'eq'),
                                                ('5', '!=', 'not_eq'),
                                                ),
                                         name="fixed list",
                                         update = propUpdate)

    def create(self):
        self.newInput(self.assignedType, "A")
        self.newInput(self.assignedType, "B")
        self.newOutput("Boolean", "Result")

    def refresh(self):
        self.applyOperation()

    def execute(self, refholder):
        self.applyOperation()
    
    def applyOperation(self):
        if self.fixed_items == '0':
            self.outputs[0].value = self.inputs[0].value > self.inputs[1].value

        elif self.fixed_items == '1':
            self.outputs[0].value = self.inputs[0].value >= self.inputs[1].value

        elif self.fixed_items == '2':
            self.outputs[0].value = self.inputs[0].value < self.inputs[1].value

        elif self.fixed_items == '3':
            self.outputs[0].value = self.inputs[0].value <= self.inputs[1].value


        elif self.fixed_items == '4':
            self.outputs[0].value = self.inputs[0].value == self.inputs[1].value

        elif self.fixed_items == '5':
            self.outputs[0].value = self.inputs[0].value != self.inputs[1].value


        self.outputs[0].name = str(self.outputs[0].value)

    def draw(self, layout):
        layout.prop(self, "fixed_items", 'Operation')
