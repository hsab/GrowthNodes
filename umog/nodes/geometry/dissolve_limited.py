from ..umog_node import *
import bpy
import numpy as np
import math
from mathutils import Vector


class DissolveLimitedNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_DissolveLimitedNode"
    bl_label = "Dissolve Limited Node"

    delimitOptions = bpy.props.EnumProperty(items=
        (('NORMAL', 'Normal', 'Delimit by face directions.'),
         ('MATERIAL ', 'Material', 'Delimit by face material.'),
         ('SEAM', 'Seam', 'Delimit by edge seams.'),
         ('SHARP', 'Sharp', 'Delimit by sharp edges.'),
         ('UV', 'UV', 'Delimit by UV coordinates.')
        ),
        name="Delimit Operation",
        default = {"NORMAL"},
        options = {"ENUM_FLAG"})

    def draw_buttons(self, context, layout):
        layout.prop(self, "delimitOptions", "Delimit Operation")

    def init(self, context):
        self.inputs.new("ObjectSocketType", "Object")
        self.inputs.new("VertexGroupSocketType", "Vertex Group")
        self.newInput("ScalarSocketType", "Angle Limit", value = 0.001, minValue = 0.0, maxValue= 180)
        self.inputs.new("BooleanSocketType", "All Boundries")

        socket = self.outputs.new("ObjectSocketType", "Output")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket = self.outputs.new("VertexGroupSocketType", "Vertex Group")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

        self.width = 200

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
        
        angleLimit = math.radians(self.inputs[2].value)
        boundries = self.inputs[3].value

        bpy.ops.mesh.dissolve_limited(angle_limit=angleLimit, use_dissolve_boundaries=boundries, delimit=self.delimitOptions)
        self.inputs[0].setViewObjectMode()

    def write_keyframe(self, refholder, frame):
        pass

    def preExecute(self, refholder):
        pass

    def postBake(self, refholder):
        pass
