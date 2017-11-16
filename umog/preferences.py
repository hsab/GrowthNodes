import os
import sys
import bpy
from bpy.props import *

currentFileDirectory = os.path.dirname(__file__)
addonName = os.path.basename(os.path.dirname(currentFileDirectory))

class DeveloperProperties(bpy.types.PropertyGroup):
    bl_idname = "umog_DeveloperProperties"

    executionInfo = BoolProperty(name = "Execution Info", default = False,
        description = "Enable informative print statements")
    traceInfo = BoolProperty(name = "Trace Info", default = False,
        description = "Enable selective traceback statements")

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = addonName

    developer = PointerProperty(type = DeveloperProperties)

    def draw(self, context):
        layout = self.layout

        row = layout.row()

        col = row.column(align = True)
        col.prop(self.developer, "executionInfo")
        col.prop(self.developer, "traceInfo")

def getPreferences():
    return bpy.context.user_preferences.addons[addonName].preferences

def getDeveloperSettings():
    return getPreferences().developer

def getBlenderVersion():
    return bpy.app.version

def getUMOGVersion():
    return sys.modules[addonName].bl_info["version"]
