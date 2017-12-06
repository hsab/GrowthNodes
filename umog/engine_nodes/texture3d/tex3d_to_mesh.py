from ..engine_node import *
from ...packages import mcubes

import threading
import sys
import bpy
import copy
import numpy as np

class EngineTexture3MeshNode(bpy.types.Node, EngineOutputNode):
    bl_idname = "engine_Texture3MeshNode"
    bl_label = "Mesh 3d Texture Node"
    
    mesh_name = bpy.props.StringProperty()
    
    iso_level = bpy.props.FloatProperty(default=0, soft_min=0.0, step=1, precision=2)
    
    def init(self, context):
        self.inputs.new("ArraySocketType", "A")

    def draw_buttons(self, context, layout):
        layout.prop(self, "mesh_name")
        layout.prop(self, "iso_level", "Iso Level")
        

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.OUT,
            input_types,
            [],
            [])

    def output_value(self, value):
        array = value.array
        #img = bpy.data.images.new('', array.shape[1], array.shape[2], alpha=True, float_buffer=True)
        #img.pixels = np.ravel(value.array, 'F')
        #img.filepath_raw = self.file_path + self.file_name + ".png"
        #img.file_format = 'PNG'
        #img.save()
        
        array = np.squeeze(array)
        
        verts, tris = mcubes.marching_cubes(array, self.iso_level)
        
        me = bpy.data.meshes.new(self.mesh_name)
        ob = bpy.data.objects.new(self.mesh_name, me)
        ob.location = (0,0,0)
        ob.show_name = True
        # Link object to scene
        bpy.context.scene.objects.link(ob)
        
        resolution = array.shape[0]
        
        for vert_i in range(len(verts)):
            for pos_i in range(len(verts[vert_i])):
                verts[vert_i][pos_i] = verts[vert_i][pos_i]/resolution -0.5
        
        #type conversions
        verts = tuple(tuple(x) for x in verts)
        tris = tuple(tuple(x) for x in tris)

        #pydevd.settrace()
        # Create mesh from given verts, edges, faces. Either edges or
        # faces should be [], or you ask for problems
        me.from_pydata(verts, [], tris)

        # Update mesh with new data
        me.update(calc_edges=True)

