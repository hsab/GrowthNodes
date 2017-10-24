from ...base_types import UMOGOutputNode
import bpy
import numpy as np
from mathutils import Vector


class SubdivideNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SubdivideNode"
    bl_label = "Subdivide"

    assignedType = "Object"

    def create(self):
        self.newInput(self.assignedType, "Object")
        self.newInput("VertexGroup", "Vertex Group")

        self.newInput("Integer", "Cut Count", value = 1, minValue = 1, maxValue = 6)
        self.newInput("Float", "Smooth Factor", value = 0.0, minValue = 0.0, maxValue = 1.0)
        
        socket = self.newOutput(self.assignedType, "Object")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket = self.newOutput("VertexGroup", "Vertex Group")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

        self.width = 220

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
            bpy.ops.mesh.select_all(action='DESELECT')

            bpy.ops.mesh.select_face_by_sides(number=4, type='NOTEQUAL', extend=True)
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

            bpy.ops.mesh.select_all(action='DESELECT')
            self.inputs[1].select()
            bpy.ops.mesh.tris_convert_to_quads(face_threshold=3.14159, shape_threshold=3.14159)

 
        bpy.ops.mesh.subdivide(number_cuts=self.inputs[2].value, smoothness=self.inputs[3].value)

        objdata = self.inputs[0].getObject().data
        objdata.update()
        self.inputs[0].setViewObjectMode()


    def write_keyframe(self, refholder, frame):
        pass

    def preExecute(self, refholder):
        pass

    def postBake(self, refholder):
        pass
