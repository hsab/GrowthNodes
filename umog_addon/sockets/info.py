import bpy
from collections import defaultdict
# from .. utils.enum_items import enumItemsFromList
from .. utils.nodes import iterSubclassesWithAttribute

class SocketInfo:
    def __init__(self):
        self.reset()

    def reset(self):
        self.idNames = set()
        self.dataTypes = set()

        self.classByType = dict()
        self.typeConversion = dict()
        self.allowedInputDataTypes = dict()
        self.allowedTargetDataTypes = defaultdict(set)

        self.baseIdName = dict()
        self.listIdName = dict()
        self.baseDataType = dict()
        self.listDataType = dict()

        self.baseDataTypes = set()
        self.listDataTypes = set()

        self.copyFunctionByType = dict()

    def update(self, socketClasses):
        self.reset()

        # create lookup tables first
        for socket in socketClasses:
            self.insertSocket(socket)

        # then insert the socket connections
        for socket in socketClasses:
            if hasattr(socket, "baseDataType"):
                self.insertSocketConnection(socket.baseDataType, socket.dataType)

        # insert allowed input data types
        for socket in socketClasses:
            if "All" in socket.allowedInputTypes:
                inputTypes = self.dataTypes
            else:
                inputTypes = socket.allowedInputTypes

            self.allowedInputDataTypes[socket.dataType] = inputTypes
            self.allowedInputDataTypes[socket.bl_idname] = inputTypes

            for inputType in inputTypes:
                self.allowedTargetDataTypes[inputType].add(socket.dataType)
                self.allowedTargetDataTypes[self.typeConversion[inputType]].add(socket.dataType)

    def insertSocket(self, socketClass):
        idName = socketClass.bl_idname
        dataType = socketClass.dataType

        self.idNames.add(idName)
        self.dataTypes.add(dataType)

        self.classByType[idName] = socketClass
        self.classByType[dataType] = socketClass

        self.typeConversion[idName] = dataType
        self.typeConversion[dataType] = idName

        if socketClass.isCopyable():
            copyFunction = eval("lambda value: " + socketClass.getCopyExpression())
        else:
            copyFunction = lambda value: value

        self.copyFunctionByType[idName] = copyFunction
        self.copyFunctionByType[dataType] = copyFunction

_socketInfo = SocketInfo()

def updateSocketInfo():
    socketClasses = getSocketClasses()
    _socketInfo.update(socketClasses)

def getSocketClasses():
    from .. base_types import UMOGSocket
    return list(iterSubclassesWithAttribute(UMOGSocket, "bl_idname"))


def returnOnFailure(returnValue):
    def failHandlingDecorator(function):
        def wrapper(*args, **kwargs):
            try: return function(*args, **kwargs)
            except: return returnValue
        return wrapper
    return failHandlingDecorator

# Data Type <-> Id Name
@returnOnFailure(None)
def toIdName(input):
    if isIdName(input): return input
    return _socketInfo.typeConversion[input]

def isIdName(name):
    return name in _socketInfo.idNames
