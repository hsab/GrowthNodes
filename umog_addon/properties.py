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
