from ...base_types import UMOGOutputNode
import bpy
import numpy as np
import math
from mathutils import Vector
import bmesh

class SharpEdgesNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SharpEdgesNode"
    bl_label = "Sharp Edges"

    assignedType = "Object"

    def create(self):
        self.newInput(self.assignedType, "Object")
        self.newInput("Float", "Sharpness", value = 20, minValue = 0.0, maxValue= 180)
        self.newInput("Float", "Weight", value = 1.0, minValue = 0.0, maxValue= 1.0)

        socket = self.newOutput(self.assignedType, "Output")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket = self.newOutput("VertexGroup", "Vertex Group")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

        self.width = 200

    def refresh(self):
        self.outputs[0].value = self.inputs[0].value
        self.outputs[0].refresh()

        if self.inputs[0].value == '':
            self.outputs[1].value = ''
            self.outputs[1].object = ''
            self.outputs[1].refresh()
        else:
            self.outputs[1].value = self.name
            self.outputs[1].object = self.inputs[0].value
            self.outputs[1].refresh()

    def execute(self, refholder):
        self.selectVertexGroup()
        self.inputs[0].setSelected()
        overrideContext = self.inputs[0].setViewEditMode(selectAll = 'DESELECT')

        angleLimit = math.radians(self.inputs[1].value)
        bpy.ops.mesh.edges_select_sharp(sharpness=angleLimit)

        obj = self.inputs[0].getObject()
        objData = obj.data
        
        obj.update_from_editmode()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.edges.ensure_lookup_table()
        selected = [e for e in bm.edges if e.select]

        for e in selected:
           faces = e.link_faces
           for f in faces:
               f.select = True

        bmesh.update_edit_mesh(obj.data)
        # bm.free()
        obj.update_from_editmode()

        bpy.context.scene.tool_settings.vertex_group_weight = self.inputs[2].value
        bpy.ops.object.vertex_group_assign()

        self.inputs[0].setViewObjectMode()

    def write_keyframe(self, refholder, frame):
        pass

    def preExecute(self, refholder):
        self.setupVertexGroupOutput()

    def postBake(self, refholder):
        pass

    def setupVertexGroupOutput(self):
        name = self.name
        obj = self.inputs[0].getObject()

        if name not in obj.vertex_groups:
            bpy.ops.object.vertex_group_add()
            obj.vertex_groups.active.name = name

        self.outputs[1].value = name
        self.outputs[1].object = self.inputs[0].value

    def selectVertexGroup(self):
        name = self.name
        obj = self.inputs[0].getObject()

        if name in obj.vertex_groups:
            obj.vertex_groups.active_index = obj.vertex_groups[name].index
            self.inputs[0].setSelected()
            overrideContext = self.inputs[0].setViewEditMode(selectAll = 'SELECT')
            bpy.ops.object.vertex_group_remove_from()
            self.inputs[0].setViewObjectMode()


