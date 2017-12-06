import bpy
from functools import wraps
from bpy.app.handlers import persistent
from .debug import *
# def validCallback(function):
#     @wraps(function)
#     def wrapper(self, context):
#         function(self, context)
#     return wrapper


# Event Handler System
###########################################################

fileSavePreUMOGHandlers = []
fileLoadPostUMOGHandlers = []
addonLoadPostUMOGHandlers = []
sceneUpdatePostUMOGHandlers = []
frameChangePostUMOGHandlers = []

renderPreUMOGHandlers = []
renderInitUMOGHandlers = []
renderCancelUMOGHandlers = []
renderCompleteUMOGHandlers = []

def eventUMOGHandler(event):
    def eventHandlerDecorator(function):
        if event == "FILE_SAVE_PRE": fileSavePreUMOGHandlers.append(function)
        if event == "FILE_LOAD_POST": fileLoadPostUMOGHandlers.append(function)
        if event == "ADDON_LOAD_POST": addonLoadPostUMOGHandlers.append(function)
        if event == "SCENE_UPDATE_POST": sceneUpdatePostUMOGHandlers.append(function)
        if event == "FRAME_CHANGE_POST": frameChangePostUMOGHandlers.append(function)

        if event == "RENDER_INIT": renderInitUMOGHandlers.append(function)
        if event == "RENDER_PRE": renderPreUMOGHandlers.append(function)
        if event == "RENDER_CANCEL": renderCancelUMOGHandlers.append(function)
        if event == "RENDER_COMPLETE": renderCompleteUMOGHandlers.append(function)
        return function
    return eventHandlerDecorator

umogAddonChanged = False

@persistent
def sceneUpdatePostUMOG(scene):
    for handler in sceneUpdatePostUMOGHandlers:
        # DBG(str(handler))
        handler(scene)

    global umogAddonChanged
    if umogAddonChanged:
        umogAddonChanged = False
        for handler in addonLoadPostUMOGHandlers:
            # DBG(str(handler))
            handler()

@persistent
def savePreUMOG(scene):
    for handler in fileSavePreUMOGHandlers:
        # DBG(str(handler))
        handler()

@persistent
def loadPostUMOG(scene):
    for handler in fileLoadPostUMOGHandlers:
        # DBG(str(handler))
        handler()

@persistent
def renderPreUMOG(scene):
    for handler in renderPreUMOGHandlers:
        # DBG(str(handler))
        handler()

@persistent
def frameChangedPostUMOG(scene):
    for handler in frameChangePostUMOGHandlers:
        # DBG(str(handler))
        handler(scene)

@persistent
def renderInitializedUMOG(scene):
    for handler in renderInitUMOGHandlers:
        # DBG(str(handler))
        handler()

@persistent
def renderCancelledUMOG(scene):
    for handler in renderCancelUMOGHandlers:
        # DBG(str(handler))
        handler()

@persistent
def renderCompletedUMOG(scene):
    for handler in renderCancelUMOGHandlers:
        # DBG(str(handler))
        handler()

def register():
    bpy.app.handlers.frame_change_post.append(frameChangedPostUMOG)
    bpy.app.handlers.scene_update_post.append(sceneUpdatePostUMOG)
    bpy.app.handlers.load_post.append(loadPostUMOG)
    bpy.app.handlers.save_pre.append(savePreUMOG)

    bpy.app.handlers.render_complete.append(renderCompletedUMOG)
    bpy.app.handlers.render_init.append(renderInitializedUMOG)
    bpy.app.handlers.render_cancel.append(renderCancelledUMOG)
    bpy.app.handlers.render_pre.append(renderPreUMOG)

    global umogAddonChanged
    umogAddonChanged = True

def unregister():
    bpy.app.handlers.frame_change_post.remove(frameChangedPostUMOG)
    bpy.app.handlers.scene_update_post.remove(sceneUpdatePostUMOG)
    bpy.app.handlers.load_post.remove(loadPostUMOG)
    bpy.app.handlers.save_pre.remove(savePreUMOG)

    bpy.app.handlers.render_complete.remove(renderCompletedUMOG)
    bpy.app.handlers.render_init.remove(renderInitializedUMOG)
    bpy.app.handlers.render_cancel.remove(renderCancelledUMOG)
    bpy.app.handlers.render_pre.remove(renderPreUMOG)
