import bpy
from bpy.props import *
from ... base_types import UMOGNode
# from ... sockets.info import getListDataTypes, toBaseDataType, toListDataType


items = ("Custom", "Location", "Rotation", "Scale", "LocRotScale")
enumItems = [(item, item, "") for item in items]

class GenericType(bpy.types.PropertyGroup):
    bl_idname = "umog_GenericType"
    # path = StringProperty(default = "test", update = propertyChanged, description = "String Property")
    genTypeStringProp = StringProperty(default = "Location", description = "String Property")
    genTypeIntProp = FloatProperty(default = 0, min = -51, soft_max =5, description = "Float Property")

class MotherNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_MotherNode"
    bl_label = "Mother Node"
    dynamicLabelType = "ALWAYS"

    itemList = CollectionProperty(type = GenericType)

    selectedEnum = EnumProperty(default = "Location", items = enumItems, name = "Path Type")

    assignedType = StringProperty()

    def setup(self):
        self.assignedType = "Object"

    def create(self):
        pass
        # self.newInput("Float", "Float", "enable", value = False)
        # self.newInput("Texture", "Texture", "setKeyframe")
        # self.newInput("Mat3", "Mat3", "removeUnwanted")
        # self.newInput("Integer", "Object", "object")

    def draw(self, layout):
        row = layout.row(align = True)
        row.prop(self, "selectedEnum", text = "")
        self.invokeFunction(row, "addItemToList", icon = "PLUS")

        col = layout.column(align = True)
        for i, item in enumerate(self.itemList):
            row = col.row(align = True)
            split = row.split(align = True, percentage = 0.5)
            split.prop(item, "genTypeStringProp", text = "")
            split.prop(item, "genTypeIntProp", text = "")
            self.invokeFunction(row, "removeItemFromList", icon = "X", data = str(i))

        row = layout.row(align = True)
        self.invokeFunction(row, "newInputSocket",
            text = "New Input",
            description = "Create a new input socket",
            icon = "PLUS")
        self.invokeFunction(row, "removeUnlinkedInputs",
            description = "Remove unlinked inputs",
            confirm = True,
            icon = "X")

        self.drawTypeSpecifics(layout)


    # def drawLabel(self):
    #     return "Create " + toListDataType(self.assignedType)

    # def getInputSocketVariables(self):
    #     return {socket.identifier : "float_" + str(i) for i, socket in enumerate(self.inputs)}


    # def edit(self):
    #     self.updateOutputName()
    #     emptySocket = self.inputs["..."]
    #     origin = emptySocket.directOrigin
    #     if origin is None: return
    #     socket = self.newInputSocket()
    #     socket.linkWith(origin)
    #     emptySocket.removeLinks()

    # def assignListDataType(self, listDataType):
    #     self.assignedType = toBaseDataType(listDataType)

    # def assignBaseDataType(self, baseDataType, inputAmount = 2):
    #     self.assignedType = baseDataType
    #     self.recreateSockets(inputAmount)

    # def recreateSockets(self, inputAmount = 2):
    #     self.clearSockets()

    #     self.newInput("Node Control", "...")
    #     for i in range(inputAmount):
    #         self.newInputSocket()
    #     self.newOutput(toListDataType(self.assignedType), "List", "outList")

    def newInputSocket(self):
        socket = self.newInput(self.assignedType, "Object")
        socket.dataIsModified = True
        socket.display.text = True
        socket.text = "Object"
        socket.removeable = True
        socket.moveable = True
        socket.defaultDrawType = "PREFER_PROPERTY"
        socket.moveUp()

        if len(self.inputs) > 2:
            socket.copyDisplaySettingsFrom(self.inputs[0])

        self.updateOutputName()
        return socket

    def updateOutputName(self):
        name = "List ({})".format(len(self.inputs) - 1)
        if len(self.outputs) > 0:
            self.outputs[0].name = name

    def removeUnlinkedInputs(self):
        for socket in self.inputs[:-1]:
            if not socket.is_linked:
                socket.remove()

    def drawTypeSpecifics(self, layout):
        if len(self.inputs) == 1:
            self.drawAdvancedTypeSpecific(layout)

    def drawAdvancedTypeSpecific(self, layout):
        if self.assignedType in ("Object", "Spline"):
            pass
            # self.invokeFunction(layout, "createInputsForSelectedObjects", text = "From Selection", icon = "PLUS")
        if self.assignedType == "Object Group":
            pass
            # self.invokeFunction(layout, "createInputsForSelectedObjectGroups", text = "From Selection", icon = "PLUS")

    # def createInputsForSelectedObjects(self):
    #     names = getSortedSelectedObjectNames()
    #     for name in names:
    #         socket = self.newInputSocket()
    #         socket.objectName = name

    # def createInputsForSelectedObjectGroups(self):
    #     groups = self.getGroupsOfObjects(bpy.context.selected_objects)
    #     for group in groups:
    #         socket = self.newInputSocket()
    #         socket.groupName = group.name

    # def getGroupsOfObjects(self, objects):
    #     groups = set()
    #     for object in objects:
    #         groups.update(group for group in bpy.data.groups if object.name in group.objects)
    #     return list(groups)


    def preExecute(self, refholder):
        # consider saving the result from this
        self.outputs[0].integer_value = self.input_value

    def addItem(self, path, index = -1):
        item = self.itemList.add()
        item.genTypeStringProp = path
        item.genTypeIntProp = index

    def addItemToList(self):
        type = self.selectedEnum
        if type == "Custom": self.addItem("")
        elif type == "Location": self.addItem("loc")
        elif type == "Rotation": self.addItem("rot")
        elif type == "Scale": self.addItem("scale")
        elif type == "LocRotScale":
            self.addItem("loc")
            self.addItem("rot")
            self.addItem("scale")

    def removeItemFromList(self, strIndex):
        self.itemList.remove(int(strIndex))