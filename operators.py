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

class MyItem(bpy.types.PropertyGroup):
    pass

class WM_UL_my_list(bpy.types.UIList):
    pass

class addCubeSample(bpy.types.Operator):
    bl_idname = 'mesh.add_cube_sample'
    bl_label = 'Add Cube'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {"FINISHED"}

class bakeMeshes(bpy.types.Operator):
    bl_idname = 'umog.bake_meshes'
    bl_label = 'Bake Mesh(es)'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        start_nodes = []
        #initialize NodePriority to -1 for non output and 0 for output nodes
        nn2p = {}
        for node in bpy.context.space_data.edit_tree.nodes:
            try:
                if node._OutputNode:
                    nn2p[node.name] = 0
                    start_nodes.append(node)
            except:
                nn2p[node.name] = -1
        
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
        
        refholder = UMOGReferenceHolder()
        
        for node in sorted_nodes:
            node.preExecute(refholder)
        for frames in range(bpy.context.scene.StartFrame, bpy.context.scene.EndFrame):
            for subframes in range(0, bpy.context.scene.SubFrames):
                for node in sorted_nodes:
                    node.execute(refholder)
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
    
class UMOG_OT_SelectTexture(bpy.types.Operator):
    bl_idname = "umog.select_texture"
    bl_label = "Select Texture"

    collection = bpy.props.CollectionProperty(type=MyItem)
    collection_index = bpy.props.IntProperty()

    pnode = bpy.props.StringProperty()
    
    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout

        layout.template_list(
            "WM_UL_my_list", "",
            self, "collection", self, "collection_index")

    def execute(self, context):
        print("texture selected: " + self.collection[self.collection_index].name)
        try:
            bpy.context.space_data.edit_tree.nodes[self.pnode].texture = self.collection[self.collection_index].name
            print("set property of active node")
        except:
            pass
        return {'FINISHED'}

    def invoke(self, context, event):
        self.collection.clear()
        #print(dir(self.collection))
        for i in bpy.data.textures.keys():
            item = self.collection.add()
            item.name=i
        return context.window_manager.invoke_props_dialog(self)
    
    
class UMOG_OT_SelectTexture(bpy.types.Operator):
    bl_idname = "umog.select_mesh"
    bl_label = "Select Mesh"

    collection = bpy.props.CollectionProperty(type=MyItem)
    collection_index = bpy.props.IntProperty()

    pnode = bpy.props.StringProperty()
    
    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout

        layout.template_list(
            "WM_UL_my_list", "",
            self, "collection", self, "collection_index")

    def execute(self, context):
        print("texture selected: " + self.collection[self.collection_index].name)
        try:
            bpy.context.space_data.edit_tree.nodes[self.pnode].mesh_name = self.collection[self.collection_index].name
            print("set property of active node")
        except:
            pass
        return {'FINISHED'}

    def invoke(self, context, event):
        self.collection.clear()
        #print(dir(self.collection))
        for i in bpy.data.meshes.keys():
            item = self.collection.add()
            item.name=i
        return context.window_manager.invoke_props_dialog(self)
        
class UMOG_OT_EasySculpt(bpy.types.Operator):
    bl_idname = 'umog.easy_sculpt'
    bl_label = 'Easy Sculpt'
    bl_options = {'REGISTER', 'UNDO'}
    
    def check(self, context):
        return True

    def execute(self, context):
        print("attempting to sculpt")
        bpy.ops.object.mode_set(mode = 'SCULPT')
        rv = bpy.ops.sculpt.brush_stroke(stroke=[{ "name": "defaultStroke",
            "mouse" : (0.0, 0.0),
            "pen_flip" : False,
            "is_start": True,
            "location": (1.0, 1.0, -1.0),
            "pressure": 1.0,
            "time": 0.0,
            "size" :500},
        { "name": "defaultStroke",
            "mouse" : (0.0, 0.0),
            "pen_flip" : False,
            "is_start": False,
            "location": (1.0, 1.0, 1.0),
            "pressure": 1.0,
            "time": 1.2,
            "size" :500}
        ])
        print(dir(rv))
        return {'FINISHED'}
