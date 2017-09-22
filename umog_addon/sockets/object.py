import bpy
from bpy.props import *
from bpy.types import Object
from .. base_types import UMOGSocket
from .. utils.nodes import newNodeAtCursor
# from .. utils.id_reference import tryToFindObjectReference

class ObjectSocket(bpy.types.NodeSocket, UMOGSocket):
    '''Custom Object socket type'''

    bl_idname = 'ObjectSocketType'
    bl_label = 'Object Socket'
    dataType = "Object"
    allowedInputTypes = ["Object"]

    drawColor = (0, 1, 1, 0.5)
    storable = False
    comparable = True

    objectName = StringProperty()
    objectCreationType = StringProperty(default = "")
    showHideToggle = BoolProperty(default = False)

    # def drawProperty(self, layout, text, node):
    #     row = layout.row(align = True)

    #     scene = self.nodeTree.scene
    #     if scene is None: scene = bpy.context.scene
    #     row.prop_search(self, "objectName", scene, "objects", icon = "NONE", text = text)

    #     if self.objectCreationType != "":
    #         self.invokeFunction(row, node, "createObject", icon = "PLUS")

    #     if self.showHideToggle:
    #         object = self.getValue()
    #         if object is not None:
    #             icon = "RESTRICT_VIEW_ON" if object.hide else "RESTRICT_VIEW_OFF"
    #             self.invokeFunction(row, node, "toggleObjectVisibilty", icon = icon,
    #                 description = "Toggle viewport and render visibility.")

    #     self.invokeFunction(row, node, "handleEyedropperButton", icon = "EYEDROPPER", passEvent = True,
    #         description = "Assign active object to this socket (hold CTRL to open a rename object dialog)")


    # def draw_color(self, context, node):
    #     return (0, 1, 1, 0.5)

    # Optional function for drawing the socket input value
    def drawProperty(self, layout, text, node):
        layout.label(text=text)
        row = layout.row()
        self.invokeFunction(row, node, "addIntegerNode", icon = "PLUS", emboss = False,
                description = "Create a new node node")

    def addIntegerNode(self):
        node = newNodeAtCursor("umog_IntegerNode")
        self.linkWith(node.outputs[0])

    # def getValue(self):
    #     if self.objectName == "": return None

    #     object = tryToFindObjectReference(self.objectName)
    #     name = getattr(object, "name", "")
    #     if name != self.objectName: self.objectName = name
    #     return object

    # def setProperty(self, data):
    #     self.objectName = data

    # def getProperty(self):
    #     return self.objectName

    # def updateProperty(self):
    #     self.getValue()

    # def handleEyedropperButton(self, event):
    #     if event.ctrl:
    #         bpy.ops.an.rename_datablock_popup("INVOKE_DEFAULT",
    #             oldName = self.objectName,
    #             path = "bpy.data.objects",
    #             icon = "OBJECT_DATA")
    #     else:
    #         object = bpy.context.active_object
    #         if object: self.objectName = object.name

    # def createObject(self):
    #     type = self.objectCreationType
    #     if type == "MESH": data = bpy.data.meshes.new("Mesh")
    #     if type == "CURVE":
    #         data = bpy.data.curves.new("Curve", "CURVE")
    #         data.dimensions = "3D"
    #         data.fill_mode = "FULL"
    #     object = bpy.data.objects.new("Target", data)
    #     bpy.context.scene.objects.link(object)
    #     self.objectName = object.name

    # def toggleObjectVisibilty(self):
    #     object = self.getValue()
    #     if object is None: return
    #     object.hide = not object.hide
    #     object.hide_render = object.hide

    # @classmethod
    # def getDefaultValue(cls):
    #     return None

    # @classmethod
    # def correctValue(cls, value):
    #     if isinstance(value, Object) or value is None:
    #         return value, 0
    #     return cls.getDefaultValue(), 2