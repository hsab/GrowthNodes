from ..umog_node import *
import bpy
import numpy as np
from mathutils import Vector


class DissolveDegenerateNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_DissolveDegenerateNode"
    bl_label = "Dissolve Degenerate Node"

    def init(self, context):
        self.inputs.new("ObjectSocketType", "Object")
        self.inputs.new("VertexGroupSocketType", "Vertex Group")

        self.newInput("ScalarSocketType", "Threshold", value = 0.001, minValue = 0.0, maxValue= 10.0)
        socket = self.outputs.new("ObjectSocketType", "Object")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket = self.outputs.new("VertexGroupSocketType", "Vertex Group")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def refresh(self):
        if self.inputs[0].value == '':
            self.inputs[1].value = ''
            self.inputs[1].object = ''
        else:
            self.inputs[1].object = self.inputs[0].value

        self.outputs[0].value = self.inputs[0].value
        self.outputs[0].refresh()

        self.outputs[1].value = self.inputs[1].value
        self.outputs[1].refresh()

    def execute(self, refholder):
        if self.inputs[1].value == '':
            self.inputs[0].setSelected()
            overrideContext = self.inputs[0].setViewEditMode(selectAll = 'SELECT')
        else:
            self.inputs[1].setSelected()
            overrideContext = self.inputs[1].select()

        bpy.ops.mesh.dissolve_degenerate(overrideContext, threshold=self.inputs[2].value)
        self.inputs[0].setViewObjectMode()

    def write_keyframe(self, refholder, frame):
        pass

    def preExecute(self, refholder):
        pass

    def postBake(self, refholder):
        pass
