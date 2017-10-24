from ...base_types import UMOGOutputNode
import bpy
import numpy as np
from mathutils import Vector


class DissolveDegenerateNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_DissolveDegenerateNode"
    bl_label = "Dissolve Degenerate Node"

    assignedType = "Object"

    def create(self):
        self.newInput(self.assignedType, "Object")
        self.newInput("Float", "Threshold", value = 0.001, minValue = 0.0, maxValue= 10.0)
        socket = self.newOutput(self.assignedType, "Output")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def refresh(self):
        self.outputs[0].value = self.inputs[0].value
        self.outputs[0].refresh()

    def execute(self, refholder):
        self.inputs[0].setSelected()
        overrideContext = self.inputs[0].setViewEditMode(selectAll = 'SELECT')
        
        bpy.ops.mesh.dissolve_degenerate(overrideContext, threshold=self.inputs[1].value)
        self.inputs[0].setViewObjectMode()

    def write_keyframe(self, refholder, frame):
        pass

    def preExecute(self, refholder):
        pass

    def postBake(self, refholder):
        pass
