import bpy

import numpy as np

class UMOGReferenceHolder:
    def __init__(self):
        self.references = {}
        #maps texture names to integers
        self.ntindex =0
        self.tdict = {}
        self.np2dtextures= {}
    def getRefForTexture2d(self, name):
        if name in self.tdict:
            return self.tdict[name]
        oldidx = self.ntindex
        self.ntindex += 1
        #setup the empty texture array
        tr = bpy.context.scene.TextureResolution
        self.np2dtextures[oldidx] = np.zeros((tr,tr,4))
        self.tdict[name] = oldidx
        #now fill in the values
        self.fillTexture(oldidx, name)
        return oldidx
    #returns the index of an initialized 
    def createRefForTexture2d(self):
        oldidx = self.ntindex
        self.ntindex += 1
        #setup the empty texture array
        tr = bpy.context.scene.TextureResolution
        self.np2dtextures[oldidx] = np.zeros((tr,tr,4))
        return oldidx
        
    def fillTexture(self, index, name):
        tr = bpy.context.scene.TextureResolution
        trh = tr/2
        for i in range(0, tr):
            for j in range(0, tr):
                x, y = (i-trh)/trh, (j-trh)/trh
                self.np2dtextures[index][i,j] = bpy.data.textures[name].evaluate((x,y,0.0))
                
    #used to generate intermediate or output references
    def getNewRef(self):
        oldidx = self.ntindex
        self.ntindex += 1
        return oldidx

class bakeMeshes(bpy.types.Operator):
    bl_idname = 'umog.bake_meshes'
    bl_label = 'Bake Mesh(es)'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        start_nodes = []
        #initialize NodePriority to -1 for non output and 0 for output nodes
        nn2p = {}
        #dictionary of enabled
        nn2e = {}
        for node in bpy.context.space_data.edit_tree.nodes:
            try:
                if node._OutputNode:
                    nn2p[node.name] = 0
                    start_nodes.append(node)
            except:
                nn2p[node.name] = -1
            nn2e[node.name] = True
        
        #now using the start nodes
        while len(start_nodes) != 0:
            next_nodes = []
            for node in start_nodes:
                for ln in node.inputs:
                    try:
                        ln = ln.links[0].from_node
                        if nn2p[ln.name] == -1:
                            nn2p[ln.name] = nn2p[node.name] +1
                            next_nodes.append(ln)
                    except:
                        pass
            start_nodes = next_nodes
        #sort the nodes by NodePriority
        sorted_nodes = sorted(bpy.context.space_data.edit_tree.nodes, key=lambda node:nn2p[node.name])
        #highest numbered nodes should be first
        sorted_nodes.reverse()
        
        for node in sorted_nodes:
            if nn2p[node.name] == -1:
                nn2e[node.name] = False
        
        refholder = UMOGReferenceHolder()
        
        for node in sorted_nodes:
            if nn2e[node.name]:
                node.preExecute(refholder)
        for frames in range(bpy.context.scene.StartFrame, bpy.context.scene.EndFrame):
            for subframes in range(0, bpy.context.scene.SubFrames):
                for node in sorted_nodes:
                    if nn2e[node.name]:
                        node.execute(refholder)
            for node in sorted_nodes:
                if nn2e[node.name]:
                    node.postFrame(refholder)
                    #consider at what point to do the end of frame calls
        return {"FINISHED"}

class addKeyframeSample(bpy.types.Operator):
    bl_idname = 'umog.add_keyframe_sample'
    bl_label = 'Add Keyframe'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        obj.location[2] = 0.0
        obj.keyframe_insert(data_path="location", frame=10.0, index=2)
        obj.location[2] = 1.0
        obj.keyframe_insert(data_path="location", frame=20.0, index=2)
        return {'FINISHED'}

