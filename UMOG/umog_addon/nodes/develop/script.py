import bpy
from bpy.props import *
from ... base_types import UMOGNode
from ... utils.debug import *


class ScriptNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ScriptNode"
    bl_label = "Script Node"
    dynamicLabelType = "ALWAYS"

    assignedType = StringProperty()

    executionCode = StringProperty(default = "")
    textBlockName = StringProperty(default = "")
    scriptName = StringProperty(default = "ScriptName")
    textBlock = None

    def create(self):
        print("in script node create")
        self.assignedType = "Variable"
        self.width = 270

    def draw(self, layout):
        layout.prop(self, "scriptName", text = "", icon = "GROUP_VERTEX")
        row = layout.row(align = True)
        self.invokeFunction(row, "removeUnlinkedInputs",
            text = "Remove Unlinked",
            description = "Remove unlinked inputs",
            confirm = True,
            icon = "X")

        self.invokeFunction(row, "run",
            text = "Run Script",
            description = "Runs the selected script text block",
            confirm = True,
            icon = "PLAY")

        row = layout.row(align = True)
        if self.textBlockName is "":
            self.invokeFunction(row, "createNewTextBlock", icon = "ZOOMIN")
        # else:
        #     self.invokeSelector(row, "AREA", "viewTextBlockInArea",
        #         icon = "ZOOM_SELECTED")

        row.prop_search(self, "textBlockName",  bpy.data, "texts", text = "")
        
        row = layout.row(align = True)
        self.invokeFunction(row, "newVariable",
            text = "newVariable",
            description = "Create a new variable socket",
            icon = "PLUS")

        self.drawTypeSpecifics(layout)

    def createNewTextBlock(self):
        textBlock = bpy.data.texts.new(name = self.scriptName)
        textBlock.use_tabs_as_spaces = True
        textBlock.write("#Variables are passed in as locals. Eg. {'varName':socket}")
        textBlock.write("#def entry():\n")
        textBlock.write("#	print(varName)")
        self.textBlockName = textBlock.name
        # self.writeToTextBlock()

    def viewTextBlockInArea(self, area):
        area.type = "TEXT_EDITOR"
        space = area.spaces.active
        space.text = self.textBlock
        space.show_line_numbers = True
        space.show_syntax_highlight = True

    def newVariable(self):
        socket = self.newInput(self.assignedType, "Variable")
        socket.textProps.editable = True
        socket.display.textInput = True
        socket.display.text = True
        socket.text = "varName"
        socket.removeable = True
        socket.moveable = True
        socket.defaultDrawType = "TEXT_PROPERTY"

        self.updateOutputName()
        return socket
    
    def run(self):
        scriptCode = bpy.data.texts[self.textBlockName].as_string()
        scriptLocals = {}
        for socket in self.inputs:
            scriptLocals[socket.text] = socket.getConnectedNode.getProperty()

        comiledScript = compile(scriptCode, '<string>', 'exec')
        exec(comiledScript, scriptLocals, scriptLocals)
        a = scriptLocals['testthat']()
        b = scriptLocals['testthat']()
        c = scriptLocals['testthat']()
        d = scriptLocals['testthat']()
        print("hey",a,b,c,d)
        # exec(textBlock.as_string())
        # entry()

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