bl_info = {
    "name": "GrowthNodes",
    "author": "Hirad Sab",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "Node Editor > GrowthNodes",
    "description": "Surface Growth Simulation Nodes",
    "warning": "Testing Needed",
    "wiki_url": "https://github.com/hsab/GrowthNodes",
    "tracker_url": "https://github.com/hsab/GrowthNodes/issues",
    "category": "Node"
}

import os
import sys
import traceback
from os.path import dirname, join, abspath

addonDirectoryName = "umog_addon"
currentDirectory = dirname(abspath(__file__))
addonsDirectory = dirname(currentDirectory)
currentDirectory = join(currentDirectory, addonDirectoryName)
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

try: from .umog_addon import import_modules
except: pass

if "import_modules" not in globals():
    message = ("\n\n"
        "The UMOG Nodes addon cannot be registered correctly.\n"
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

from .umog_addon.preferences import getBlenderVersion
if getBlenderVersion() < (2, 76, 0):
    message = ("\n\n"
        "UMOG requires at least Blender 2.77.\n"
        "Your are using an older version.\n"
        "Please download the latest official release.")
    raise Exception(message)

# if not os.path.isfile(compilationInfoPath):
#     message = ("\n\n"
#         "This is just the source code of UMOG, not a compiled or dynamic build.\n"
#         "Please download a build for your operating system instead or run setup.py with --pyximport command.\n"
#         "If you download a build from releases, don't forget to remove this copy first.")
#     raise Exception(message)

# import json
# with open(compilationInfoPath) as f:
#     compilation_info = json.load(f)

# if "sys.pyximport" in compilation_info:
#     try:
#         import pyximport
#     except:
#         pass
#     if "pyximport" not in globals():
#         message = ("\n\n"
#             "UMOG's pyximport is enabled.\n\n"
#             "This is for development purposes and is not intended for production.\n"
#             "Your python does not include the pyximport library.\n\n"
#             "Please download a compiled build for you operating system,\nor follow development guides on wiki.")
#         raise Exception(message)

# elif compilation_info["sys.platform"] != sys.platform:
#     message = ("\n\n"
#         "This UMOG build is for another OS.\n\n"
#         "You are using: {}\n"
#         "This build is for: {}\n\n"
#         "Please download a build for your operating system."
#         ).format(sys.platform, compilation_info["sys.platform"])
#     raise Exception(message)

# else:
#     currentPythonVersion = tuple(sys.version_info[:3])
#     addonPythonVersion = tuple(compilation_info["sys.version_info"][:3])

#     if currentPythonVersion[:2] != addonPythonVersion[:2]:
#         message = ("\n\n"
#                    "There is a Python version mismatch.\n\n"
#                    "Your Blender build uses: {}\n"
#                    "UMOG has been compiled for: {}\n\n"
#                    "You have three options:\n"
#                    "  1. Try make Blender use another Python version.\n"
#                    "     (Blender 2.78/2.79 officially uses Python 3.5.x)\n"
#                    "  2. Compile UMOG yourself using the correct Python version.\n"
#                    "     (Look in the developer manual for more information)\n"
#                    "  3. Create an issue on Github and ask if someone can create a build for you."
#                    ).format(currentPythonVersion, addonPythonVersion)
#         raise Exception(message)

# Load all submodules
##################################
#
from .umog_addon import import_modules

modules = import_modules.importAllSubmodules(__path__[0], __package__,addonDirectoryName)

if "bpy" in locals():
    print("UMOG can't be reloaded.")

from . umog_addon.sockets.info import updateSocketInfo
updateSocketInfo()

import bpy
# from . import umog_addon as UMG

def register():
    # UMG.register()
    bpy.utils.register_module(__name__)
    for module in modules:
        if hasattr(module, "register"):
            module.register()
    print("Registered UMOG with {} modules.".format(len(modules)))

def unregister():
    # UMG.unregister()
    bpy.utils.unregister_module(__name__)
    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()
    print("Unregistered UMOG.")
