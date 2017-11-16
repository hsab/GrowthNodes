'''
This module can create and register operators dynamically based on a description.
'''
import bpy
from bpy.props import *
from .. utils.debug import *
from bpy.app.handlers import persistent

operatorsByDescription = {}

def getInvokeFunctionOperator(description):
    if description not in operatorsByDescription:
        createOperator(description)

    return operatorsByDescription[description]


def invoke_InvokeFunction(self, context, event):
    self._event = event
    if self.confirm:
        return context.window_manager.invoke_confirm(self, event)
    return self.execute(context)

def execute_InvokeFunction(self, context):
    # DBG()
    args = []
    if self.invokeWithData: args.append(self.data)
    if self.passEvent: args.append(self._event)
    self.umog_executeCallback(self.callback, *args)

    bpy.context.area.tag_redraw()
    return {"FINISHED"}

def createOperator(description):
    print(description)
    operatorID = str(len(operatorsByDescription))
    idName = "umog.invoke_function_" + operatorID

    operator = type("InvokeFunction_" + operatorID, (bpy.types.Operator, ), {
        "bl_idname" : idName,
        "bl_label" : "Are you sure?",
        "bl_description" : description,
        "invoke" : invoke_InvokeFunction,
        "execute" : execute_InvokeFunction })
    operator.callback = StringProperty()
    operator.invokeWithData = BoolProperty(default = False)
    operator.confirm = BoolProperty()
    operator.data = StringProperty()
    operator.passEvent = BoolProperty()

    operatorsByDescription[description] = operator.bl_idname
    # DBG(str(description), operator, operator.bl_idname, TRACE = False)
    bpy.utils.register_class(operator)
