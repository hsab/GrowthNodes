import os
import bpy
import sys

addonName = os.path.basename(os.path.dirname(__file__))

def getPreferences():
    return bpy.context.user_preferences.addons[addonName].preferences
