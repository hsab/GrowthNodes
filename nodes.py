import bpy
import bmesh

try:
    PYDEV_SOURCE_DIR = "/usr/lib/eclipse/plugins/org.python.pydev_5.6.0.201703221358/pysrc"
    import sys
    if PYDEV_SOURCE_DIR not in sys.path:
        sys.path.append(PYDEV_SOURCE_DIR)
    import pydevd
    print("debugging enabled")
except:
    print("no debugging enabled")
    
#begin base node classes

class UMOGNode(bpy.types.Node):
    bl_width_min = 10
    bl_width_max = 5000

    _IsUMOGNode = True
    
    bl_label = "UMOGNode"
    
    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "umog_UMOGNodeTree"
    
    def init(self, context):
        print('umog node base init')
    #this will be called when the node is executed by bake meshes
    #will be called each iteration
    def execute(self, refholder):
        pass
    #will be called once before the node will be executed by bake meshes
    #refholder is passed to this so it can register any objects that need it
    def preExecute(self, refholder):
        pass
        
class UMOGOutputNode(UMOGNode):
    _OutputNode = True
    def init(self, context):
        super().init(context)

#end base node classes

#BEGIN: UMOG_NODES
            
class UMOGMeshInputNode(UMOGNode):
    bl_idname = "umog_MeshInputNode"
    bl_label = "UMOG Mesh Input Node"
        
    def init(self,context):
        print('initializing umog node')
        self.inputs.new("GetObjectSocketType", "My Input")
        self.outputs.new("GetObjectSocketType", "My Output")
        super().init(context)
        
    def execute(self, refholder):
        print("input node execution")

class UMOGNoiseGenerationNode(UMOGNode):
    bl_idname = "umog_NoiseGenerationNode"
    bl_label = "UMOG Noise Generation Node"
    
    def init(self, context):
        print('initializing umog noise node')
        self.inputs.new("NodeSocketInt", "X")
        self.inputs.new("NodeSocketInt", "Y")
        self.inputs.new("NodeSocketInt", "Z")
        self.outputs.new("NodeSocketInt", "Output")
        super().init(context)
        
    def execute(self, refholder):
        print("noise node execution")

class PrintNode(UMOGOutputNode):
    bl_idname = "umog_PrintNode"
    bl_label = "Print Node"
    
    def init(self, context):
        print('initializing umog print node')
        self.inputs.new("NodeSocketString", "Print String")
        super().init(context)

    def execute(self, refholder):
        """if self.inputs['Print String'].is_linked:
            input_String = "NOTHING ENTERED"
        else:
            input_String = self.inputs['Print String']
            
        print(input_String)"""
        print("THIS PRINT WORKS")
        
        
class GetTextureNode(UMOGNode):
    bl_idname = "umog_GetTextureNode"
    bl_label = "Get Texture Node"

    texture = bpy.props.StringProperty()
    
    texture_index = bpy.props.IntProperty()

    def init(self, context):
        self.outputs.new("GetTextureSocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.operator("umog.select_texture", text = "Select Texture").pnode = self.name
        try:
            layout.template_preview(bpy.data.textures[self.texture])
        except:
            pass

    def update(self):
        pass
    
    def execute(self, refholder):
        print("get texture node execution, texture: " + self.texture)
        print("texture handle: " + str(self.texture_index))
        print(refholder.np2dtextures[self.texture_index])
        
        
    def preExecute(self, refholder):
        #consider saving the result from this
        self.texture_index = refholder.getRefForTexture2d(self.texture)
        
        
class SculptNode(UMOGOutputNode):
    bl_idname = "umog_SculptNode"
    bl_label = "Sculpt Node"

    mesh_name = bpy.props.StringProperty()
    
    mesh_name_index = bpy.props.IntProperty()
    
    #contains the handle for the input texture
    texture_handle = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new("GetTextureSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name


    def update(self):
        pass
    
    def execute(self, refholder):
        print("sculpt node execution, mesh: " + self.mesh_name)
        print("  texture_hanlde is: " + str(self.texture_handle))
        
        
    def preExecute(self, refholder):
        #set the texture handle for use in the execute method
        try:
            fn = self.inputs[0].links[0].from_node
            self.texture_handle = fn.texture_index
        except:
            print("no mesh as input")
            
            
class ModifierNode(UMOGOutputNode):
    bl_idname = "umog_ModifierNode"
    bl_label = "Modifier Node"

    mesh_name = bpy.props.StringProperty()
    mesh_dupl_name = bpy.props.StringProperty()
    
    mesh_name_index = bpy.props.IntProperty()
    
    
    
    mod_list_handle = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new("GetTextureSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name


    def update(self):
        pass
    
    def execute(self, refholder):
        print("sculpt node execution, mesh: " + self.mesh_name)
        print("  texture_hanlde is: " + str(self.texture_handle))
        obj = bpy.data.objects[self.mesh_name]
        
        oname="Remesh"
        obj.modifiers.new(name=oname, type='REMESH')
        bpy.ops.object.modifier_apply(modifier=oname)
        
        oname="Remesh"
        mod = obj.modifiers.new(name=oname, type='DISPLACE')
        dir(mod)
        mod.texture = bpy.data.textures['Tex']
        bpy.ops.object.modifier_apply(modifier=oname)
        
        
        oname="Remesh"
        obj.modifiers.new(name=oname, type='BEVEL')
        bpy.ops.object.modifier_apply(modifier=oname)
        
        
        
    def preExecute(self, refholder):
        #set the texture handle for use in the execute method
        try:
            fn = self.inputs[0].links[0].from_node
            self.texture_handle = fn.texture_index
            #copy the mesh and hid the original
        except:
            print("no mesh as input")
            
            
class BMeshNode(UMOGOutputNode):
    bl_idname = "umog_BMeshNode"
    bl_label = "BMesh Node"

    mesh_name = bpy.props.StringProperty()
    mesh_dupl_name = bpy.props.StringProperty()
    
    mesh_name_index = bpy.props.IntProperty()
    
    
    
    mod_list_handle = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new("GetTextureSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name


    def update(self):
        pass
    
    def execute(self, refholder):
        try:
            print("sculpt node execution, mesh: " + self.mesh_name)
            print("  texture_hanlde is: " + str(self.texture_handle))
        except:
            pass
        
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(bpy.data.meshes[self.mesh_name])
        
        #bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0.4)
        #bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0, depth=-0.5)
        bmesh.ops.poke(bm, faces=bm.faces)
        
        cx, cy =0,0
        tr = bpy.context.scene.TextureResolution -1
        for vert in bm.verts:
            #displace along normal by texture
            factor = (refholder.np2dtextures[self.texture_handle].item(cx,cy,3)) + 0.1
            print("factor: " + str(factor) + " x:" + str(cx) + " y:" + str(cy))
            vert.co = vert.co + (factor * vert.normal )
            if cx == tr:
                cx =0
                cy = cy+1
            else:
                cx = cx +1
                
            if cy == tr:
                cy = 0
            
        #rv = bmesh.ops.subdivide_edges(bm, cuts=1, edges=bm.edges)
        #print(dir(rv))
        #print(rv.keys())
        
        #pydevd.settrace()
        
        
        bm.to_mesh(bpy.data.meshes[self.mesh_name])
        bm.free()
        
    def preExecute(self, refholder):
        #set the texture handle for use in the execute method
        try:
            fn = self.inputs[0].links[0].from_node
            self.texture_handle = fn.texture_index
            #copy the mesh and hid the original
        except:
            print("no texture as input")
    
class Mat3Node(UMOGNode):
    bl_idname = "umog_Mat3Node"
    bl_label = "Matrix"

    #matrix = bpy.props.FloatVectorProperty(size = 16,subtype='MATRIX', default = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))
    matrix = bpy.props.FloatVectorProperty(size = 16, default = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))
    
    
    def init(self, context):
        self.outputs.new("Mat3SocketType", "Output")
        self.inputs.new("Mat3SocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'matrix')

            
    def execute(self, refholder):
        print('begin matrix')
        for elem in self.matrix:
            print(elem)
    
#END: UMOG_NODES
