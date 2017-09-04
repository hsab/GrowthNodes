bl_info = {
    "name": "UMOG",
    "author": "Hirad Sabaghian, Micah Johnston, Marsh Poulson, Jacob Luke",
    "version": (0, 1, 6),
    "blender": (2, 78, 0),
    "location": "Node Editor > UMOG",
    "description": "Mesh Manipulation Tools",
    "warning": "prealpha",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy
from . import UMOG as umg

def register():
    umg.register()
    bpy.utils.register_module(__name__)

def unregister():
    umg.unregister()
    bpy.utils.unregister_module(__name__)
