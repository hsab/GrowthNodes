import bpy

bpy.types.Object.bakeCount = bpy.props.IntProperty(
    name="BakeCount",
    description="BakeCount",
    default=1,
    min=1)

bpy.types.Mesh.bakedKeys = {}

bpy.types.Object.hasUMOGBaked = bpy.props.BoolProperty(
    name = "hasUMOGBaked", 
    description = "hasUMOGBaked",
    default = False)

bpy.types.Scene.StartFrame = bpy.props.IntProperty(
    name = "StartFrame", 
    description = "StartFrame",
    default = 1,
    min = 1)

bpy.types.Scene.EndFrame = bpy.props.IntProperty(
    name = "EndFrame", 
    description = "EndFrame",
    default = 2,
    min = 2)

bpy.types.Scene.SubFrames = bpy.props.IntProperty(
    name = "SubFrames", 
    description = "SubFrames",
    default = 1,
    min = 1)
        
bpy.types.Scene.TextureResolution = bpy.props.IntProperty(
    name = "TextureResolution", 
    description = "TextureResolution",
    default = 256,
    min = 64)
