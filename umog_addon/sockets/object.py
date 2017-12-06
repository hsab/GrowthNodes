import bpy
import sys
import types

from bpy.props import *
from ..base_types import UMOGSocket
from ..utils.events import propUpdate


class ObjectSocket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Object socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'ObjectSocketType'
    # Label for nice name display
    bl_label = 'Object Socket'
    dataType = "Object"
    allowedInputTypes = ["Object"]

    useIsUsedProperty = False
    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0, 0.588235294, 0.533333333, 1)

    value = StringProperty(update = propUpdate)

    def drawProperty(self, context, layout, layoutParent, text, node):
        layout.prop_search(self, "value", bpy.data, "objects", icon = "MESH_CUBE",
                           text = "")
        if self.value is not "":
            pass

    def getValue(self):
        pass

    def setProperty(self, data):
        self.value = data

    def getProperty(self):
        return self.value

    def refresh(self):
        self.name = self.value

    def getObject(self):
        return bpy.data.objects[self.value]

    def setSelected(self):
        self.setViewObjectMode()
        
        for obj in bpy.data.objects:
            obj.select = False

        obj = self.getObject()

        obj.select = True
        bpy.context.scene.objects.active = obj

    def getCustomContext(self):
        win = bpy.context.window
        scr = win.screen
        areas3d = [area for area in scr.areas if area.type == 'VIEW_3D']
        region = [region for region in areas3d[0].regions if region.type == 'WINDOW']

        if len(areas3d) is 0:
            raise Exception("Execution requires a 3D View region")

        override = {
            'window': win,
            'screen': scr,
            'area': areas3d[0],
            'region': region[0],
            'scene': bpy.context.scene,
        }

        return override

    def setViewEditMode(self, selectAll = False):
        override = self.getCustomContext()
        
        bpy.ops.object.mode_set(mode='EDIT')    
        if selectAll is not False:
            bpy.ops.mesh.select_all(override, action=selectAll)
            obj = self.getObject()
            obj.update_from_editmode()
        return override

    def setViewObjectMode(self):       
        bpy.ops.object.mode_set(mode='OBJECT')
