bl_info = {
    "name": "GrowthNodes",
    "author": "Hirad Sab",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "GrowthNodes Editor",
    "description": "Surface Growth Simulation Nodes",
    "warning": "This version is still in development.",
    "wiki_url": "https://github.com/hsab/GrowthNodes",
    "tracker_url": "https://github.com/hsab/GrowthNodes/issues",
    "category": "Node"
}

import os
import sys
import traceback
from os.path import dirname, join, abspath, basename

currentDirectory = dirname(abspath(__file__))
addonsDirectory = dirname(currentDirectory)
compilationInfoPath = join(currentDirectory, "compilation_info.json")
addonName = basename(currentDirectory)

counter = 0
for name in os.listdir(addonsDirectory):
    name = name.lower()
    if "umog" in name:
        counter += 1

if counter > 1:
    message = ("\n\n"
        "There are multiple versions of GrowthNodes installed\n"
        "Please uninstall/remove all older versions of the addon\n")
    raise Exception(message)

try: from . import auto_load
except: pass

if "auto_load" not in globals():
    message = ("\n\n"
        "The GrowthNodes Nodes addon cannot be registered correctly.\n"
        "Please try to remove and install it again.\n"
        "If it still does not work, report it.\n")
    raise Exception(message)

try: import numpy
except: pass

if "numpy" not in globals():
    message = ("\n\n"
        "GrowthNodes depends on the numpy library.\n"
        "Unfortunally the Blender built you are using does not have this library.\n"
        "You can either install numpy manually or use another Blender version\n"
        "that comes with numpy (e.g. the newest official Blender release).")
    raise Exception(message)

from . preferences import getBlenderVersion
if getBlenderVersion() < (2, 80, 0):
    message = ("\n\n"
        "GrowthNodes requires at least Blender 2.80.\n"
        "Your are using an older version.\n"
        "Please download the latest official release.")
    raise Exception(message)

from . import auto_load
auto_load.init()

from . sockets.info import updateSocketInfo
updateSocketInfo()

def register():
    auto_load.register()
    print("Registered GrowthNodes")

def unregister():
    auto_load.unregister()
    print("Unregistered GrowthNodes")
