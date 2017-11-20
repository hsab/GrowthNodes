import bpy
from bpy.props import *
from collections import defaultdict
from .. utils.events import propUpdate
from .. utils.debug import *

class SocketDisplayProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_SocketDisplayProperties"
    editable = BoolProperty(default = False)
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


class UMOGSocket(bpy.types.NodeSocket):
    _isUMOGSocket = True
    drawColor = (1, 1, 1, 1)

    removeable = BoolProperty(default=False)
    moveable = BoolProperty(default=False)

    drawOutput = BoolProperty(default=False)
    drawLabel = BoolProperty(default=True)

    text = StringProperty(default="Default Name")
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
            if not self.is_output and self.isLinked:
                self.socketRecentlyRefreshed = True
                beforeValue = self.getProperty()
                afterValue = self.links[0].from_socket.getProperty()
                self.setProperty(self.links[0].from_socket.getProperty())
                self.refresh()

                # DBG("SOCKET SUCCESSFULLY REFRESHED:",
                #     "Type:   " + self.dataType,
                #     "Name:   " + self.name,
                #     "Path:   " + self.path_from_id(),
                #     "Before: " + str(beforeValue),
                #     "After:  " + str(afterValue),
                #     trace=True)
                
    def packSocket(self):
        if self.isPacked:
            self.pack()
    # Overwrite in subclasses
    ##########################################################

    def pack(self):
        pass

    def refresh(self):
        pass

    def setProperty(self, data):
        pass

    def getProperty(self):
        return

    # Drawing
    ##########################################################

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

    def drawIsUsedProperty(self, context, subrow, node):
        icon = "LAYER_ACTIVE" if self.isUsed else "LAYER_USED"
        if self.useIsUsedProperty:
            if self.is_output:
                subrow.prop(self, "isUsed", text="", icon=icon)
            if self.is_linked and not self.isUsed:
                if not self.is_output:
                    subrow.label("", icon="QUESTION")
                    subrow.label("", icon="TRIA_RIGHT")
                else:
                    subrow.label("", icon="TRIA_RIGHT")
                    subrow.label("", icon="QUESTION")
            if not self.is_output:
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

        if self.displayProps.editable and self.display.textInput:
            self.drawRefreshContain(leftSubrow)
            middleSubrow.prop(self, "text", text="")

        else:
            if not self.is_output and self.isUnlinked and self.isUsed:
                self.drawRefreshContain(leftSubrow)
                self.drawSocket(context, middleSubrow, row, 
                                displayText, node, self.defaultDrawType)
            else:
                if self.is_output:
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

        if not self.is_output:
            subrow = rightSubrow
            self.drawIsUsedProperty(context, subrow, node)
            # self.drawMoveOperators(context, subrow, node)
            # self.drawRemoveOperators(context, subrow, node)
        else:
            subrow = leftSubrow
            subrow.alignment = "LEFT"
            self.drawIsUsedProperty(context, subrow, node)
            # self.drawRemoveOperators(context, subrow, node)
            # self.drawMoveOperators(context, subrow, node)

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
        if self.display.text or (self.displayProps.editable and self.display.textInput):
            return self.text
        return self.name

    def draw_color(self, context, node):
        return self.drawColor

    # Properties
    ##########################################################

    @property
    def getConnectedNode(self):
        if self.is_output:
            return self.links[0].to_node
        else:
            return self.links[0].from_node

    @property
    def getConnectedNodes(self):
        nodes = []
        if self.is_output:
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
    def nodeTree(self):
        return self.id_data

    @property
    def isLinked(self):
        return len(self.links) > 0

    @property
    def isUnlinked(self):
        return len(self.links) == 0

    @classmethod
    def hasProperty(cls):
        return hasattr(cls, "drawProperty")

# Register
##################################

def register():
    # PointerProperties can only be added after the PropertyGroup is registered
    bpy.types.NodeSocket.display = PointerProperty(type=SocketDisplayProperties)
