import bpy
from bpy.props import *
from collections import defaultdict
from ... utils.recursion import noRecursion
from ... operators.callbacks import newSocketCallback
from ... utils.names import getRandomString, toVariableName
from ... operators.dynamic_operators import getInvokeFunctionOperator
from ... utils.events import propUpdate
from ... utils.debug import *


class SocketTextProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_SocketTextProperties"
    unique = BoolProperty(default=False)
    editable = BoolProperty(default=False)
    variable = BoolProperty(default=False)


class SocketDisplayProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_SocketDisplayProperties"
    text = BoolProperty(default=False)
    textInput = BoolProperty(default=False)
    moveOperators = BoolProperty(default=False)
    removeOperator = BoolProperty(default=False)
    refreshableIcon = BoolProperty(default=True)
    packedIcon = BoolProperty(default=True)

    isRefreshableInfo = BoolProperty(name="Draw Is Refreshable", default=True,
                                     description='''Refreshable [ON]
        Refresh this socket on change
        Value of this socket will be refreshed on node-tree changes''')
    notRefreshableInfo = BoolProperty(name="Draw Is Not Refreshable", default=True,
                                      description='''Refreshable [OFF]
        Don't refresh this socket on change
        Value of this socket is refreshed only at the beginning of bake''')
    isPackedInfo = BoolProperty(name="Draw Is Self-contained", default=True,
                                    description='''Data Packed [ON]
        Stores the initial value of this socket
        Value of this socket affects this node's calculations only at the beginning of bake''')
    notPackedInfo = BoolProperty(name="Draw Is Not Self-contained", default=True,
                                     description='''Data Packed [OFF]
        Updates the value of this socket
        Value of this socket will affects this node's calculations on every frame''')


class SocketExecutionProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_SocketExecutionProperties"
    neededCopies = IntProperty(default=0, min=0)


alternativeIdentifiersPerSocket = defaultdict(list)


class UMOGSocket:
    _isUMOGSocket = True
    drawColor = (1, 1, 1, 1)

    originalName = StringProperty(default="Default Name")

    display = PointerProperty(type=SocketDisplayProperties)
    removeable = BoolProperty(default=False)
    moveable = BoolProperty(default=False)
    moveGroup = IntProperty(default=0)

    drawOutput = BoolProperty(default=False)
    drawLabel = BoolProperty(default=True)
    textProps = PointerProperty(type=SocketTextProperties)

    def textChanged(self, context):
        updateText(self)
        propUpdate(context)

    text = StringProperty(default="Default Name", update=textChanged)
    defaultDrawType = StringProperty(default="TEXT_PROPERTY")

    isUsed = BoolProperty(name="Is Used", default=True,
                          description="Enable this socket (orange point means that the socket will be evaluated)", update=propUpdate)
    useIsUsedProperty = BoolProperty(default=False)

    isRefreshable = BoolProperty(
        name="Is Refreshable", default=True, update=propUpdate)

    isPacked = BoolProperty(
        name="Is Data Packed", default=False, update=propUpdate)

    socketRecentlyRefreshed = BoolProperty(default=False)

    # Refresh and free 
    ##########################################################
    def refreshSocket(self):
        if self.isRefreshable and not (self.isPacked and self.nodeTree.executeInProgress):
            if self.isInput and self.isLinked:
                fromSocket = self.getFromSocket
                fromSocketAllowed = fromSocket.dataType in self.allowedInputTypes
                allSocketsAllowed = "All" in self.allowedInputTypes
                if allSocketsAllowed or fromSocketAllowed:
                    self.socketRecentlyRefreshed = True
                    beforeValue = self.getProperty()
                    afterValue = self.getFromSocket.getProperty()
                    self.setProperty(self.getFromSocket.getProperty())
                    self.refresh()
                else:
                    self.reverseName()

                # DBG("SOCKET SUCCESSFULLY REFRESHED:",
                #     "Type:   " + self.dataType,
                #     "Name:   " + self.name,
                #     "Path:   " + self.path_from_id(),
                #     "Before: " + str(beforeValue),
                #     "After:  " + str(afterValue),
                #     trace=True)
            if self.isInput and self.isUnlinked:
                self.reverseName()
                
    def freeSocket(self):
        self.destroy()
    
    def packSocket(self):
        if self.isPacked:
            self.pack()
    # Overwrite in subclasses
    ##########################################################

    def destroy(self):
        pass

    def pack(self):
        pass

    def refresh(self):
        pass

    def setProperty(self, data):
        pass

    def getProperty(self):
        return

    @classmethod
    def getDefaultValue(cls):
        raise NotImplementedError(
            "All sockets have to define a getDefaultValue method")

    @classmethod
    def correctValue(cls, value):
        '''
        Return Types:
          If the value has the correct type: (value, 0)
          If the value has a correctable type: (corrected_value, 1)
          if the value has a uncorrectable type: (default_value, 2)
        '''
        raise NotImplementedError(
            "All sockets have to define a correctValue method")

    @classmethod
    def getConversionCode(cls, dataType):
        return None

    # Drawing
    ##########################################################

    def reverseName(self):
        self.name = self.originalName

    def drawRefreshContain(self, subrow):
        subrow.enabled = False
        if self.display.refreshableIcon:
            if self.isRefreshable:
                icon = "RECOVER_LAST"
                subrow.prop(self.display, "isRefreshableInfo",
                            text="", icon=icon)
            else:
                icon = "TIME"
                subrow.prop(self.display, "notRefreshableInfo",
                            text="", icon=icon)

        if self.display.packedIcon:
            if self.isPacked:
                icon = "PACKAGE"
                subrow.prop(self.display, "isPackedInfo",
                            text="", icon=icon)
            else:
                icon = "LOAD_FACTORY"
                subrow.prop(self.display, "notPackedInfo",
                            text="", icon=icon)

    def drawMoveOperators(self, context, subrow, node):
        if self.moveable and self.display.moveOperators:
            if self.isInput:
                subrow.separator()
            self.invokeFunction(subrow, node, "moveUpInGroup", icon="TRIA_UP")
            self.invokeFunction(
                subrow, node, "moveDownInGroup", icon="TRIA_DOWN")
            if not self.isInput:
                subrow.separator()

    def drawRemoveOperators(self, context, subrow, node):
        if self.removeable and self.display.removeOperator:
            if self.isInput:
                subrow.separator()
            self.invokeFunction(subrow, node, "remove", icon="X")
            if not self.isInput:
                subrow.separator()

    def drawIsUsedProperty(self, context, subrow, node):
        icon = "LAYER_ACTIVE" if self.isUsed else "LAYER_USED"
        if self.useIsUsedProperty:
            if not self.isInput:
                subrow.prop(self, "isUsed", text="", icon=icon)
            if self.is_linked and not self.isUsed:
                if self.isInput:
                    subrow.label("", icon="QUESTION")
                    subrow.label("", icon="TRIA_RIGHT")
                else:
                    subrow.label("", icon="TRIA_RIGHT")
                    subrow.label("", icon="QUESTION")
            if self.isInput:
                subrow.prop(self, "isUsed", text="", icon=icon)

    def draw(self, context, layout, node, text):
        displayText = self.getDisplayedName()

        row = layout.row(align=True)

        col = row.column()
        leftSubrow = col.row(align=True)

        col = row.column()
        middleSubrow = col.row(align=True)

        col = row.column()
        rightSubrow = col.row(align=True)

        if self.textProps.editable and self.display.textInput:
            self.drawRefreshContain(leftSubrow)
            middleSubrow.prop(self, "text", text="")

        else:
            if self.isInput and self.isUnlinked and self.isUsed:
                self.drawRefreshContain(leftSubrow)
                self.drawSocket(context, middleSubrow, row, 
                                displayText, node, self.defaultDrawType)
            else:
                if self.isOutput:
                    middleSubrow.alignment = "RIGHT"
                    if not self.drawOutput:
                        self.drawRefreshContain(rightSubrow)
                    else:
                        self.drawSocket(context, middleSubrow, row,
                                        displayText, node, self.defaultDrawType)
                        self.drawRefreshContain(rightSubrow)

                else:
                    self.drawRefreshContain(leftSubrow)
                if self.drawLabel:
                    middleSubrow.label(displayText)

        if self.isInput:
            subrow = rightSubrow
            self.drawIsUsedProperty(context, subrow, node)
            self.drawMoveOperators(context, subrow, node)
            self.drawRemoveOperators(context, subrow, node)
        else:
            subrow = leftSubrow
            subrow.alignment = "LEFT"
            self.drawRemoveOperators(context, subrow, node)
            self.drawMoveOperators(context, subrow, node)
            self.drawIsUsedProperty(context, subrow, node)

    def drawSocket(self, context, layout, layoutParent, text, node, drawType="TEXT_PROPERTY"):
        '''
        Draw Types:
            TEXT_PROPERTY_OR_NONE: Draw only if a property exists
            TEXT_PROPERTY: Draw the text and the property if one exists
            PREFER_PROPERTY: Uses PROPERTY_ONLY is one exists, otherwise TEXT_ONLY
            PROPERTY_ONLY: Draw the property; If there is now property, draw nothing
            TEXT_ONLY: Ignore the property; Just label the text
        '''
        if drawType == "TEXT_PROPERTY_OR_NONE":
            if self.hasProperty():
                drawType = "TEXT_PROPERTY"

        if drawType == "PREFER_PROPERTY":
            if self.hasProperty():
                drawType = "PROPERTY_ONLY"
            else:
                drawType = "TEXT_ONLY"

        if drawType == "TEXT_PROPERTY":
            if self.hasProperty():
                self.drawProperty(context, layout, layoutParent, text, node)
            else:
                layout.label(text)
        elif drawType == "PROPERTY_ONLY":
            if self.hasProperty():
                self.drawProperty(context, layout, layoutParent, text="", node=node)
        elif drawType == "TEXT_ONLY":
            layout.label(text)

    def getDisplayedName(self):
        if self.display.text or (self.textProps.editable and self.display.textInput):
            return self.text
        return self.name

    def draw_color(self, context, node):
        return self.drawColor

    def copyDisplaySettingsFrom(self, other):
        self.display.text = other.display.text
        self.display.textInput = other.display.textInput
        self.display.moveOperators = other.display.moveOperators
        self.display.removeOperator = other.display.removeOperator

    def invokeFunction(self, layout, node, functionName, text="", icon="NONE",
                       description="", emboss=True, confirm=False,
                       data=None, passEvent=False):
        idName = getInvokeFunctionOperator(description)
        props = layout.operator(idName, text=text, icon=icon, emboss=emboss)
        props.callback = self.newCallback(node, functionName)
        props.invokeWithData = data is not None
        props.confirm = confirm
        props.data = str(data)
        props.passEvent = passEvent

    def newCallback(self, node, functionName):
        return newSocketCallback(self, node, functionName)

    # Misc
    ##########################################################

    def free(self):
        try:
            del alternativeIdentifiersPerSocket[self.getTemporaryIdentifier()]
        except:
            pass
        try:
            del colorOverwritePerSocket[self.getTemporaryIdentifier()]
        except:
            pass

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
        self.moveTo(self.index - 1)

    def moveTo(self, index, node=None):
        ownIndex = self.index
        if ownIndex != index:
            self.sockets.move(ownIndex, index)
            self.node.socketMoved()

    def moveUpInGroup(self):
        """Cares about moveable sockets"""
        self.moveInGroup(moveUp=True)

    def moveDownInGroup(self):
        """Cares about moveable sockets"""
        self.moveInGroup(moveUp=False)

    def moveInGroup(self, moveUp=True):
        """Cares about moveable sockets"""
        if not self.moveable:
            return
        moveableSocketIndices = [index for index, socket in enumerate(
            self.sockets) if socket.moveable and socket.moveGroup == self.moveGroup]
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
            if moveUp:
                self.sockets.move(targetIndex + 1, currentIndex)
            else:
                self.sockets.move(targetIndex - 1, currentIndex)
            self.node.socketMoved()

    # Link/Remove Utilities
    ##########################################################

    def linkWith(self, socket):
        if self.isOutput:
            return self.nodeTree.links.new(socket, self)
        else:
            return self.nodeTree.links.new(self, socket)

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
    def getFromSocket(self):
        if not self.isOutput:
            return self.links[0].from_socket

    @property
    def getConnectedNode(self):
        if self.isOutput:
            return self.links[0].to_node
        else:
            return self.links[0].from_node

    @property
    def getConnectedNodes(self):
        nodes = []
        if self.isOutput:
            for link in self.links:
                nodes.append(link.to_node)
        else:
            for link in self.links:
                nodes.append(link.from_node)
        return nodes

    @property
    def index(self):
        if self.is_output:
            return list(self.node.outputs).index(self)
        return list(self.node.inputs).index(self)

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

    @property
    def isLinked(self):
        return len(self.links) > 0

    @property
    def isUnlinked(self):
        return len(self.links) == 0

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
        socket.text = getNotUsedText(socket.node, prefix=text)
    socket.node.customSocketNameChanged(socket)


def getNotUsedText(node, prefix):
    text = prefix
    while isTextUsed(node, text):
        text = prefix + "_" + getRandomString(2)
    return text


def isTextUsed(node, name):
    for socket in node.sockets:
        if socket.text == name:
            return True
    return False

    # Register
##################################


def getSocketIndex(socket, node=None):
    if node is None:
        node = socket.node
    if socket.is_output:
        return list(node.outputs).index(socket)
    return list(node.inputs).index(socket)


def isUMOGNodeSocket(socket):
    return getattr(socket, "_isUMOGSocket", False)


def register():
    bpy.types.NodeSocket.getIndex = getSocketIndex
    bpy.types.NodeSocket.isUMOGNodeSocket = BoolProperty(
        default=False, get=isUMOGNodeSocket)


def unregister():

    del bpy.types.NodeSocket.isUMOGNodeSocket
