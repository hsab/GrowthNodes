import bpy
from bpy.props import *
from ... base_types import UMOGNode
from ... utils.debug import *


class ScriptNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_ScriptNode"
    bl_label = "Script Node"
    dynamicLabelType = "ALWAYS"

    assignedType : StringProperty()

    executionCode : StringProperty(default = "")
    textBlockName : StringProperty(default = "")
    scriptName : StringProperty(default = "ScriptName")
    textBlock = None

    def create(self):
        print("in script node create")
        self.assignedType = "Variable"
        self.width = 270
        self.newInput("Boolean", "Execute Per Frame", value = False)


    def draw(self, layout):
        row = layout.row(align = True)
        self.invokeFunction(row, "newOutVariable",
            text = "New Output Variable",
            description = "Create a new output variable socket",
            icon = "TRACKING_REFINE_FORWARDS")

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
            confirm = False,
            icon = "PLAY")

        row = layout.row(align = True)
        if self.textBlockName is "":
            self.invokeFunction(row, "createNewTextBlock", icon = "ZOOM_IN")
        # else:
        #     self.invokeSelector(row, "AREA", "viewTextBlockInArea",
        #         icon = "ZOOM_SELECTED")

        row.prop_search(self, "textBlockName",  bpy.data, "texts", text = "")
        
        row = layout.row(align = True)
        self.invokeFunction(row, "newInVariable",
            text = "New Input Variable",
            description = "Create a new input variable socket",
            icon = "TRACKING_REFINE_BACKWARDS")

        self.drawTypeSpecifics(layout)

    def createNewTextBlock(self):
        textBlock = bpy.data.texts.new(name = self.scriptName)
        textBlock.indentation = 'TABS'
        textBlock.write("#Variables are passed in as locals. Eg. {'varName':socket}\n")
        textBlock.write("#def entry():\n")
        textBlock.write("#	print(varInput)")
        self.textBlockName = textBlock.name
        # self.writeToTextBlock()

    def viewTextBlockInArea(self, area):
        area.type = "TEXT_EDITOR"
        space = area.spaces.active
        space.text = self.textBlock
        space.show_line_numbers = True
        space.show_syntax_highlight = True

    def newInVariable(self):
        socket = self.newInput(self.assignedType, "Variable")
        socket.textProps.editable = True
        socket.display.textInput = True
        socket.display.text = True
        socket.text = "varInput" + str(len(self.inputs) - 1)
        socket.removeable = True
        socket.moveable = True
        socket.defaultDrawType = "TEXT_PROPERTY"

        self.updateOutputName()
        return socket

    def newOutVariable(self):
        socket = self.newOutput(self.assignedType, "Variable")
        socket.textProps.editable = True
        socket.display.textInput = True
        socket.display.text = True
        socket.text = "varOutput" + str(len(self.outputs))
        socket.removeable = True
        socket.moveable = True
        socket.defaultDrawType = "TEXT_PROPERTY"

        self.updateOutputName()
        return socket
    
    def execute(self, refholder):
        if self.inputs[0].value:
            self.run()

    def run(self):
        scriptCode = bpy.data.texts[self.textBlockName].as_string()
        scriptLocals = {}
        scriptGlobals = {}
        if len(self.inputs) > 1:
            for socket in self.inputs[1:]:
                if socket.isLinked:
                    scriptLocals[socket.text] = socket.getFromSocket.value
            for socket in self.outputs:
                scriptLocals[socket.text] = None

            comiledScript = compile(scriptCode, '<string>', 'exec')
            # exec(comiledScript)
            exec(comiledScript, None, scriptLocals)

            for socket in self.outputs:
                socket.value = str(scriptLocals[socket.text])

            print()
            # b = scriptLocals['testthat']()
            # c = scriptLocals['testthat']()
            # d = scriptLocals['testthat']()
            # print("hey",a,b,c,d)
            # exec(scriptCode)
            # entry()

    def updateOutputName(self):
        name = "List ({})".format(len(self.inputs) - 1)
        if len(self.outputs) > 0:
            self.outputs[0].name = name

    def removeUnlinkedInputs(self):
        if len(self.inputs) > 1:
            for socket in self.inputs[1:]:
                if not socket.is_linked:
                    socket.remove()

        for socket in self.outputs:
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
        # self.outputs[0].integer_value = self.input_value
        pass

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

        DBG(type, TRACE = False)

    def removeItemFromList(self, strIndex):
        DBG(self.itemList[int(strIndex)], TRACE = False)
        self.itemList.remove(int(strIndex))