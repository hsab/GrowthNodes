bl_info = {
    "name": "UMOG",
    "author": "Hirad Sabaghian, Micah Johnston, Marsh Poulson, Jacob Luke",
    "version": (0, 2, 1),
    "blender": (2, 79, 0),
    "location": "Node Editor > UMOG",
    "description": "Mesh Manipulation Tools",
    "warning": "prealpha",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import os
import sys
import traceback
from os.path import dirname, join, abspath

currentDirectory = dirname(abspath(__file__))
addonsDirectory = dirname(currentDirectory)
compilationInfoPath = join(currentDirectory, "compilation_info.json")

counter = 0
for name in os.listdir(addonsDirectory):
    name = name.lower()
    if "umog" in name:
        counter += 1

if counter > 1:
    message = ("\n\n"
        "There are multiple versions of UMOG installed\n"
        "Please uninstall/remove all older versions of the addon\n")
    raise Exception(message)

try: from . import import_modules
except: pass

if "import_modules" not in globals():
    message = ("\n\n"
        "UMOG cannot be registered correctly.\n"
        "Please try to remove and install it again.\n"
        "If it still does not work, report it.\n")
    raise Exception(message)

try: import numpy
except: pass

if "numpy" not in globals():
    message = ("\n\n"
        "UMOG depends on the numpy library.\n"
        "Unfortunally the Blender built you are using does not have this library.\n"
        "You can either install numpy manually or use another Blender version\n"
        "that comes with numpy (e.g. the newest official Blender release).")
    raise Exception(message)

import bpy
if bpy.app.version < (2, 76, 0):
    message = ("\n\n"
        "UMOG requires at least Blender 2.77.\n"
        "Your are using an older version.\n"
        "Please download the latest official release.")
    raise Exception(message)

if not os.path.isfile(compilationInfoPath):
    message = ("\n\n"
        "This is just the source code of UMOG, not a compiled or dynamic build.\n"
        "Please download a build for your operating system instead or run setup.py with --pyximport command.\n"
        "If you download a build from releases, don't forget to remove this copy first.")
    raise Exception(message)

import json
with open(compilationInfoPath) as f:
    compilation_info = json.load(f)

if compilation_info["sys.platform"] != sys.platform:
    message = ("\n\n"
        "This UMOG build is for another OS.\n\n"
        "You are using: {}\n"
        "This build is for: {}\n\n"
        "Please download a build for your operating system."
        ).format(sys.platform, compilation_info["sys.platform"])
    raise Exception(message)

else:
    currentPythonVersion = tuple(sys.version_info[:3])
    addonPythonVersion = tuple(compilation_info["sys.version_info"][:3])

    if currentPythonVersion[:2] != addonPythonVersion[:2]:
        message = ("\n\n"
                   "There is a Python version mismatch.\n\n"
                   "Your Blender build uses: {}\n"
                   "UMOG has been compiled for: {}\n\n"
                   "You have three options:\n"
                   "  1. Try make Blender use another Python version.\n"
                   "     (Blender 2.78/2.79 officially uses Python 3.5.x)\n"
                   "  2. Compile UMOG yourself using the correct Python version.\n"
                   "     (Look in the developer manual for more information)\n"
                   "  3. Create an issue on Github and ask if someone can create a build for you."
                   ).format(currentPythonVersion, addonPythonVersion)
        raise Exception(message)

# Load all submodules
##################################
#
from . import import_modules
modules = import_modules.importAllSubmodules(__path__[0], 'umog_addon')

from .umog.sockets.info import updateSocketInfo
updateSocketInfo()

def register():
    bpy.utils.register_module(__name__)
    for module in modules:
        if hasattr(module, "register"):
            module.register()
    print("Registered UMOG with {} modules.".format(len(modules)))

def unregister():
    bpy.utils.unregister_module(__name__)
    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()
    print("Unregistered UMOG.")
