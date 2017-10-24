import bpy
import sys
import types

from bpy.props import *
from ..base_types import UMOGSocket
from ..utils.events import propUpdate


class VertexGroupSocket(bpy.types.NodeSocket, UMOGSocket):
    # Description string
    '''Custom Vertex Group  socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Vertex Group SocketType'
    # Label for nice name display
    bl_label = 'Vertex Group Socket'
    dataType = "VertexGroup"
    allowedInputTypes = ["VertexGroup"]

    useIsUsedProperty = False
    defaultDrawType = "PREFER_PROPERTY"

    drawColor = (0.376470588, 0.48627451, 0.541176471, 1)

    object = StringProperty(update = propUpdate)
    value = StringProperty(update = propUpdate)

    def drawProperty(self, context, layout, layoutParent, text, node):
        if self.object != "":
            obj = bpy.data.objects[self.object]
            if obj.type == 'MESH':
                layout.prop_search(self, "value", obj, "vertex_groups",
                                   icon = "GROUP_VERTEX", text = "")

    def getValue(self):
        return self.value

    def setProperty(self, data):
        self.object = self.getFromSocket.object
        self.value = data

    def getProperty(self):
        return self.value

    def refresh(self):
        self.name = self.value

    def getObject(self):
        return bpy.data.objects[self.object]

    def setObject(self, data):
        self.object = data

    def getVertexGroup(self):
        return self.getObject().vertex_groups[self.value]

    def setVertexGroupActive(self):
        self.getObject().vertex_groups.active_index = self.getVertexGroup().index
