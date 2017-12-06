from ...base_types import UMOGOutputNode
import bpy
import numpy as np
import math
from mathutils import Vector
import bmesh

class SharpFacesNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SharpFacesNode"
    bl_label = "Sharp Faces"

    assignedType = "Object"

    def create(self):
        self.newInput(self.assignedType, "Object")
        self.newInput("Float", "Angle", value = 20, minValue = 0.0, maxValue= 180)
        self.newInput("Boolean", "Inverse Select", value = False)
        self.newInput("Boolean", "Top", value = True)
        self.newInput("Boolean", "Bottom", value = True)
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
        # bpy.ops.mesh.edges_select_sharp(sharpness=angleLimit)

        obj = self.inputs[0].getObject()
        objData = obj.data
        
        obj.update_from_editmode()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()

        for f in bm.faces:
            f.select = False
            loc, rot, scale = obj.matrix_world.decompose()
            zangle = Vector((0,0,1)).angle(rot * f.normal)
            
            top = self.inputs[3].value
            bottom = self.inputs[4].value
            angle = self.inputs[1].value
            
            zangle = math.degrees(zangle)   
            posDir = zangle <= angle
            negDir = zangle >= 180 - angle
            
            if top and not bottom:
                if posDir:
                    f.select = True
            elif bottom and not top:
                if negDir:
                    f.select = True
            elif top and bottom:
                if posDir or negDir:
                    f.select = True

        bmesh.update_edit_mesh(obj.data)
        bm.free()

        if self.inputs[2].value == True:
            bpy.ops.mesh.select_all(action='INVERT')

        obj.update_from_editmode()

        bpy.context.scene.tool_settings.vertex_group_weight = self.inputs[5].value
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

