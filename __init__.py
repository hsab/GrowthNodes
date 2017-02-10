bl_info = {
    "name": "UMOG",
    "author": "Hirad Sabaghian, Micah Johnston, Marsh Poulson, Jacob Luke",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "Node Editor > UMOG",
    "description": "Mesh Manipulation Tools",
    "warning": "prealpha",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}


import bpy
import sys

class MyCustomNode(bpy.types.Node):
	@classmethod
	def poll(cls, tree):
		#avalible in all trees
		return true
	# Description string
	#'''A custom node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'CustomNodeType'
	# Label for nice name display
	bl_label = 'Custom Node'
	# Icon identifier
	bl_icon = 'SOUND'

class HelloWorldPanel(bpy.types.Panel):
	bl_idname = "panel.panel3"
	bl_label = "Panel3"
	bl_space_type = "NODE_EDITOR"
	bl_region_type = "UI"

	def draw(self, context):
		self.layout.operator("mesh.add_cube_sample", icon='MESH_CUBE', text="Add Cube 3")
	
def register():
	print("begin resitration")
	bpy.utils.register_class(MyCustomNode)
	bpy.utils.register_class(HelloWorldPanel)
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()