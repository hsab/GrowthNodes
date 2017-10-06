import bpy
from bpy.props import *
from ... base_types import UMOGNode
from ... utils.debug import *


items = ("Custom", "Location", "Rotation", "Scale", "LocRotScale")
enumItems = [(item, item, "") for item in items]

class GenericType(bpy.types.PropertyGroup):
    bl_idname = "umog_GenericType"
    genTypeStringProp = StringProperty(default = "Location", description = "String Property")
    genTypeIntProp = FloatProperty(default = 0, min = -51, soft_max =5, description = "Float Property")

class MotherNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_MotherNode"
    bl_label = "Mother Node"
    dynamicLabelType = "ALWAYS"

    itemList = CollectionProperty(type = GenericType)

    selectedEnum = EnumProperty(default = "Location", items = enumItems, name = "Path Type")

    assignedType = StringProperty()

    def create(self):
        print("mothernode setup")
        self.width = 300
        self.assignedType = "Texture2"

    def draw(self, layout):
        row = layout.row(align = True)
        row.prop(self, "selectedEnum", text = "")
        self.invokeFunction(row, "addItemToList",
            description = "Add item to list",
            icon = "PLUS")

        col = layout.column(align = True)
        for i, item in enumerate(self.itemList):
            row = col.row(align = True)
            split = row.split(align = True, percentage = 0.5)
            split.prop(item, "genTypeStringProp", text = "")
            split.prop(item, "genTypeIntProp", text = "")
            self.invokeFunction(row, "removeItemFromList",
                description = "Remove item from list",
                icon = "X", 
                data = str(i))

        row = layout.row(align = True)
        row.alert = True
        self.invokeFunction(row, "removeUnlinkedInputs",
            text = "Remove Unlinked",
            emboss = True,
            description = "Remove unlinked inputs",
            confirm = True,
            icon = "X")

        row = layout.row(align = True)
        row.alert = True
        self.invokeFunction(row, "newOutputNode",
            text = "Output Socket",
            emboss = True,
            description = "Remove unlinked inputs",
            confirm = True,
            icon = "PLUS")

        row = layout.row(align = True)
        self.invokeFunction(row, "newEditableSocket",
            text = "Editable Socket",
            description = "Create a new input socket",
            icon = "PLUS")
        row = layout.row(align = True)
        self.invokeFunction(row, "newWithDrawPropertySocket",
            text = "With Property Socket",
            description = "Create a new input socket",
            icon = "PLUS")
        row = layout.row(align = True)
        self.invokeFunction(row, "newMoveableSocket",
            text = "Moveable Socket",
            description = "Create a new input socket",
            icon = "PLUS")
        row = layout.row(align = True)
        self.invokeFunction(row, "newRemoveableSocket",
            text = "Removeable Socket",
            description = "Create a new input socket",
            icon = "PLUS")
        row = layout.row(align = True)
        self.invokeFunction(row, "newUseIsUsedProperty",
            text = "Property Socket",
            description = "Create a new input socket",
            icon = "PLUS")

        self.drawTypeSpecifics(layout)

    def newOutputNode(self):
        socket = self.newOutput(self.assignedType, "Texture2")
        # socket.textProps.editable = True
        # socket.display.text = True
        socket.text = "Texture2"
        socket.drawOutput = True
        socket.drawLabel = False
        # socket.removeable = True
        # socket.moveable = True
        # socket.display.removeOperator = True
        # socket.display.moveOperators = True
        # socket.useIsUsedProperty = True
        socket.defaultDrawType = "TEXT_PROPERTY"

    def newEditableSocket(self):
        socket = self.newInput(self.assignedType, "Float")
        socket.textProps.editable = True
        socket.display.textInput = True
        socket.display.text = True
        socket.text = "Editable"
        socket.removeable = True
        socket.moveable = True
        socket.defaultDrawType = "TEXT_PROPERTY"

        # if len(self.inputs) > 2:
        #     socket.copyDisplaySettingsFrom(self.inputs[0])

        self.updateOutputName()
        return socket

    def newWithDrawPropertySocket(self):
        socket = self.newInput(self.assignedType, "Float")
        # socket.display.text = True
        # socket.text = "Output"
        # socket.moveable = True
        # socket.display.moveOperators = True
        # socket.defaultDrawType = "TEXT_PROPERTY"

        self.updateOutputName()
        return socket

    def newMoveableSocket(self):
        socket = self.newInput(self.assignedType, "Float")
        socket.display.text = True
        socket.text = "Moveable"
        socket.moveable = True
        socket.display.moveOperators = True
        socket.defaultDrawType = "TEXT_PROPERTY"

        self.updateOutputName()
        return socket

    def newRemoveableSocket(self):
        socket = self.newInput(self.assignedType, "Float")
        socket.display.text = True
        socket.text = "Removeable"
        socket.removeable = True
        socket.moveable = True
        socket.display.removeOperator = True
        socket.defaultDrawType = "TEXT_PROPERTY"

        self.updateOutputName()
        return socket

    def newUseIsUsedProperty(self):
        socket = self.newInput(self.assignedType, "Float")
        socket.display.text = True
        socket.text = "Toggle Use"
        socket.moveable = True
        socket.removeable = True
        socket.moveable = True
        socket.display.removeOperator = True
        socket.display.moveOperators = True
        socket.useIsUsedProperty = True
        socket.defaultDrawType = "TEXT_PROPERTY"

        self.updateOutputName()
        return socket

    def updateOutputName(self):
        name = "List ({})".format(len(self.inputs) - 1)
        if len(self.outputs) > 0:
            self.outputs[0].name = name

    def removeUnlinkedInputs(self):
        for socket in self.inputs:
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

        # DBG(type, TRACE = False)

    def removeItemFromList(self, strIndex):
        # DBG(self.itemList[int(strIndex)], TRACE = False)
        self.itemList.remove(int(strIndex))