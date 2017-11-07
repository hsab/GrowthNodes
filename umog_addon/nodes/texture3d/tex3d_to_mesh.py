from ... base_types import UMOGNode
from . import pyglet_tr_impl
from ...packages import mcubes

import threading
import sys
import bpy
import copy
import numpy as np
import pyximport
pyximport.install()

PYDEV_SOURCE_DIR = "/usr/lib/eclipse/dropins/pydev/plugins/org.python.pydev_6.0.0.201709191431/pysrc"
 
import sys
 
if PYDEV_SOURCE_DIR not in sys.path:
   sys.path.append(PYDEV_SOURCE_DIR)
 
import pydevd

class UMOGTexture3MeshNode(bpy.types.Node, UMOGNode):
    bl_idname = "umog_Texture3MeshNode"
    bl_label = "Mesh 3d Texture Node"
    
    mesh_name = bpy.props.StringProperty()
    
    def create(self):
        self.newInput("Texture3", "A").isPacked = True

    def draw(self, layout):
        layout.prop(self, "mesh_name")
        

    def execute(self, refholder):
        if self.inputs[0].isLinked:
            verts, tris = mcubes.marching_cubes(self.inputs[0].getFromSocket.getPixels(),0)
            
            me = bpy.data.meshes.new(self.mesh_name)
            ob = bpy.data.objects.new(self.mesh_name, me)
            ob.location = (0,0,0)
            ob.show_name = True
            # Link object to scene
            bpy.context.scene.objects.link(ob)
            
            resolution = self.nodeTree.properties.TextureResolution
            
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
            
            

    def preExecute(self, refholder):
        pass
