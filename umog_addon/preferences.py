import os
import bpy
import sys

addonName = os.path.basename(os.path.dirname(__file__))

def getPreferences():
    return bpy.context.user_preferences.addons[addonName].preferences

def getDeveloperSettings():
    return getPreferences().developer

def getExecutionCodeSettings():
    return getPreferences().executionCode

def getExecutionCodeType():
    return getExecutionCodeSettings().type

def getColorSettings():
    return getPreferences().nodeColors

def getMeshIndicesSettings():
    return getPreferences().drawHandlers.meshIndices

def debuggingIsEnabled():
    return getPreferences().developer.debug

def testsAreEnabled():
    return getPreferences().developer.runTests

def getBlenderVersion():
    return bpy.app.version

def getAnimationNodesVersion():
    return sys.modules[addonName].bl_info["version"]
