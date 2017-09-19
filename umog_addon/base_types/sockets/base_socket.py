import bpy
from bpy.props import *
from collections import defaultdict
from ... utils.recursion import noRecursion

class SocketTextProperties(bpy.types.PropertyGroup):
    bl_idname = "an_SocketTextProperties"
    unique = BoolProperty(default = False)
    editable = BoolProperty(default = False)
    variable = BoolProperty(default = False)

class SocketDisplayProperties(bpy.types.PropertyGroup):
    bl_idname = "an_SocketDisplayProperties"
    text = BoolProperty(default = False)
    textInput = BoolProperty(default = False)
    moveOperators = BoolProperty(default = False)
    removeOperator = BoolProperty(default = False)

class SocketExecutionProperties(bpy.types.PropertyGroup):
    bl_idname = "an_SocketExecutionProperties"
    neededCopies = IntProperty(default = 0, min = 0)

alternativeIdentifiersPerSocket = defaultdict(list)

class UMOGSocket:
    storable = True
    comparable = False
    _isUMOGSocket = True

    def textChanged(self, context):
        updateText(self)

    text = StringProperty(default = "custom name", update = textChanged)
    removeable = BoolProperty(default = False)
    moveable = BoolProperty(default = False)
    moveGroup = IntProperty(default = 0)

    useIsUsedProperty = BoolProperty(default = False)

    display = PointerProperty(type = SocketDisplayProperties)
    textProps = PointerProperty(type = SocketTextProperties)

    dataIsModified = BoolProperty(default = False)
    defaultDrawType = StringProperty(default = "TEXT_PROPERTY")

 # Overwrite in subclasses
    ##########################################################

    def setProperty(self, data):
        pass

    def getProperty(self):
        return

    @classmethod
    def getDefaultValue(cls):
        raise NotImplementedError("All sockets have to define a getDefaultValue method")

    @classmethod
    def correctValue(cls, value):
        '''
        Return Types:
          If the value has the correct type: (value, 0)
          If the value has a correctable type: (corrected_value, 1)
          if the value has a uncorrectable type: (default_value, 2)
        '''
        raise NotImplementedError("All sockets have to define a correctValue method")

    @classmethod
    def getConversionCode(cls, dataType):
        return None

    # Drawing
    ##########################################################

    def draw(self, context, layout, node, text):
        displayText = self.getDisplayedName()

        row = layout.row(align = True)
        if self.textProps.editable and self.display.textInput:
            row.prop(self, "text", text = "")
        else:
            if self.isInput and self.isUnlinked and self.isUsed:
                self.drawSocket(row, displayText, node, self.defaultDrawType)
            else:
                if self.isOutput: row.alignment = "RIGHT"
                row.label(displayText)

        if self.moveable and self.display.moveOperators:
            row.separator()
            self.invokeFunction(row, node, "moveUpInGroup", icon = "TRIA_UP")
            self.invokeFunction(row, node, "moveDownInGroup", icon = "TRIA_DOWN")

        if self.removeable and self.display.removeOperator:
            row.separator()
            self.invokeFunction(row, node, "remove", icon = "X")

        if self.useIsUsedProperty:
            if self.is_linked and not self.isUsed:
                row.label("", icon = "QUESTION")
                row.label("", icon = "TRIA_RIGHT")
            icon = "LAYER_ACTIVE" if self.isUsed else "LAYER_USED"
            row.prop(self, "isUsed", text = "", icon = icon)

    def drawSocket(self, layout, text, node, drawType = "TEXT_PROPERTY"):
        '''
        Draw Types:
            TEXT_PROPERTY_OR_NONE: Draw only if a property exists
            TEXT_PROPERTY: Draw the text and the property if one exists
            PREFER_PROPERTY: Uses PROPERTY_ONLY is one exists, otherwise TEXT_ONLY
            PROPERTY_ONLY: Draw the property; If there is now property, draw nothing
            TEXT_ONLY: Ignore the property; Just label the text
        '''
        if drawType == "TEXT_PROPERTY_OR_NONE":
            if self.hasProperty(): drawType = "TEXT_PROPERTY"

        if drawType == "PREFER_PROPERTY":
            if self.hasProperty(): drawType = "PROPERTY_ONLY"
            else: drawType = "TEXT_ONLY"

        if drawType == "TEXT_PROPERTY":
            if self.hasProperty(): self.drawProperty(layout, text, node)
            else: layout.label(text)
        elif drawType == "PROPERTY_ONLY":
            if self.hasProperty(): self.drawProperty(layout, text = "", node = node)
        elif drawType == "TEXT_ONLY":
            layout.label(text)

    def getDisplayedName(self):
        if self.display.text or (self.textProps.editable and self.display.textInput):
            return self.text
        return self.name

    def copyDisplaySettingsFrom(self, other):
        self.display.text = other.display.text
        self.display.textInput = other.display.textInput
        self.display.moveOperators = other.display.moveOperators
        self.display.removeOperator = other.display.removeOperator

    # def _selector_PATH(self, data):
    #     bpy.ops.an.choose_path("INVOKE_DEFAULT",
    #         callback = self.newCallback(self.node, data))

    # def _selector_AREA(self, data):
    #     bpy.ops.an.select_area("INVOKE_DEFAULT",
    #         callback = self.newCallback(self.node, data))

    def newCallback(self, node, functionName):
        return newSocketCallback(self, node, functionName)

    # Misc
    ##########################################################

    def free(self):
        try: del alternativeIdentifiersPerSocket[self.getTemporaryIdentifier()]
        except: pass
        try: del colorOverwritePerSocket[self.getTemporaryIdentifier()]
        except: pass

    @property
    def alternativeIdentifiers(self):
        return alternativeIdentifiersPerSocket[self.getTemporaryIdentifier()]

    @alternativeIdentifiers.setter
    def alternativeIdentifiers(self, value):
        alternativeIdentifiersPerSocket[self.getTemporaryIdentifier()] = value

    def getTemporaryIdentifier(self):
        return str(hash(self)) + self.identifier

    # Move Utilities
    ##########################################################

    def moveUp(self):
        self.moveTo(self.getIndex() - 1)

    def moveTo(self, index, node = None):
        ownIndex = self.getIndex(node)
        if ownIndex != index:
            self.sockets.move(ownIndex, index)
            self.node.socketMoved()

    def moveUpInGroup(self):
        """Cares about moveable sockets"""
        self.moveInGroup(moveUp = True)

    def moveDownInGroup(self):
        """Cares about moveable sockets"""
        self.moveInGroup(moveUp = False)

    def moveInGroup(self, moveUp = True):
        """Cares about moveable sockets"""
        if not self.moveable: return
        moveableSocketIndices = [index for index, socket in enumerate(self.sockets) if socket.moveable and socket.moveGroup == self.moveGroup]
        currentIndex = list(self.sockets).index(self)

        targetIndex = -1
        for index in moveableSocketIndices:
            if moveUp and index < currentIndex:
                targetIndex = index
            if not moveUp and index > currentIndex:
                targetIndex = index
                break

        if targetIndex != -1:
            self.sockets.move(currentIndex, targetIndex)
            if moveUp: self.sockets.move(targetIndex + 1, currentIndex)
            else: self.sockets.move(targetIndex - 1, currentIndex)
            self.node.socketMoved()


    # Link/Remove Utilities
    ##########################################################

    def linkWith(self, socket):
        if self.isOutput: return self.nodeTree.links.new(socket, self)
        else: return self.nodeTree.links.new(self, socket)

    def remove(self):
        self.free()
        node = self.node
        node.removeSocket(self)
        node.socketRemoved()

    def removeLinks(self):
        removedLink = False
        if self.is_linked:
            tree = self.nodeTree
            for link in self.links:
                tree.links.remove(link)
                removedLink = True
        return removedLink

    def isLinkedToType(self, dataType):
        return any(socket.dataType == dataType for socket in self.linkedSockets)


    # Properties
    ##########################################################

    @property
    def isOutput(self):
        return self.is_output

    @property
    def isInput(self):
        return not self.is_output

    @property
    def nodeTree(self):
        return self.id_data

    @property
    def sockets(self):
        """Returns all sockets next to this one (all inputs or outputs)"""
        return self.node.outputs if self.isOutput else self.node.inputs

    @classmethod
    def hasProperty(cls):
        return hasattr(cls, "drawProperty")

    @classmethod
    def isCopyable(self):
        return hasattr(self, "getCopyExpression")

    @classmethod
    def getCopyExpression(cls):
        return "value[:]"

@noRecursion
def updateText(socket):
    correctText(socket)

def correctText(socket):
    if socket.textProps.variable:
        socket.text = toVariableName(socket.text)
    if socket.textProps.unique:
        text = socket.text
        socket.text = "temporary name to avoid some errors"
        socket.text = getNotUsedText(socket.node, prefix = text)
    socket.node.customSocketNameChanged(socket)

def getNotUsedText(node, prefix):
    text = prefix
    while isTextUsed(node, text):
        text = prefix + "_" + getRandomString(2)
    return text

def isTextUsed(node, name):
    for socket in node.sockets:
        if socket.text == name: return True
    return False

    # Register
##################################

def getSocketVisibility(socket):
    return not socket.hide

def setSocketVisibility(socket, value):
    socket.hide = not value

def toID(socket):
    node = socket.node
    return ((node.id_data.name, node.name), socket.is_output, socket.identifier)

def getNodeTree(socket):
    return socket.node.id_data

def getSocketIndex(socket, node = None):
    if node is None: node = socket.node
    if socket.is_output:
        return list(node.outputs).index(socket)
    return list(node.inputs).index(socket)

def isAnimationNodeSocket(socket):
    return getattr(socket, "_isAnimationNodeSocket", False)

def register():
    bpy.types.NodeSocket.toID = toID
    bpy.types.NodeSocket.getIndex = getSocketIndex
    bpy.types.NodeSocket.getNodeTree = getNodeTree

    bpy.types.NodeSocket.show = BoolProperty(default = True,
        get = getSocketVisibility, set = setSocketVisibility)

    bpy.types.NodeSocket.isAnimationNodeSocket = BoolProperty(default = False,
        get = isAnimationNodeSocket)

def unregister():
    del bpy.types.NodeSocket.toID
    del bpy.types.NodeSocket.show
    del bpy.types.NodeSocket.isAnimationNodeSocket