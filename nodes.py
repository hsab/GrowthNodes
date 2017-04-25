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

class GetTextureNode(UMOGNode):
    bl_idname = "umog_GetTextureNode"
    bl_label = "Get Texture Node"

    texture = bpy.props.StringProperty()
    
    texture_index = bpy.props.IntProperty()

    def init(self, context):
        self.outputs.new("BaseInputSocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        #layout.operator("umog.select_texture", text = "Select Texture").pnode = self.name
        layout.prop_search(self, "texture", bpy.data, "textures", icon="TEXTURE_DATA", text="")
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
    stroke_pressure = bpy.props.FloatProperty(min=0.0001, max=2.0, default=1.0)
    stroke_size = bpy.props.IntProperty(default=44)
    dyntopo_detail = bpy.props.FloatProperty(min=0.1, max=5, default=1.5, precision=1)
    
    def init(self, context):
        #self.inputs.new("BaseInputSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        #layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")
        layout.prop(self, "stroke_pressure", text="Stroke Pressure")
        layout.prop(self, "stroke_size", text="Stroke Size")
        layout.prop(self, "dyntopo_detail", text="Precision Level")

    def update(self):
        pass
    
    def execute(self, refholder):
        print("sculpt node execution, mesh: " + self.mesh_name)

        for area in bpy.context.screen.areas:
            print(area.type)
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = bpy.data.objects[self.mesh_name]

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.normals_make_consistent()
                
                bpy.ops.object.mode_set(mode = 'SCULPT')
                
                bpy.data.brushes["SculptDraw"].stroke_method = "DOTS"
                bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
                
                if not bpy.context.sculpt_object.use_dynamic_topology_sculpting:
                    bpy.ops.sculpt.dynamic_topology_toggle()
                    bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
                    bpy.context.scene.tool_settings.sculpt.constant_detail = self.dyntopo_detail

                obj = bpy.context.active_object
                verts = list(obj.data.vertices)

                mouse_width = int(area.width/2)
                mouse_height = int(area.height/2)

                for vert in verts:
                    bpy.ops.sculpt.brush_stroke(ctx, stroke=[{
                        "name": "first",
                        "mouse" : (mouse_width , mouse_height),
                        "is_start": True,
                        "location": obj.matrix_world * vert.co,
                        "pressure": self.stroke_pressure,
                        'pen_flip': False,
                        'time': 1.0,
                        "size": self.stroke_size}])
                bpy.ops.object.mode_set(mode = 'OBJECT')
                print("SCULPT DYNAMIC FINISHED")
        
    def preExecute(self, refholder):
        #set the texture handle for use in the execute method
        try:
            fn = self.inputs[0].links[0].from_node
            #self.texture_handle = fn.texture_index
        except:
            print("no mesh as input")

class SculptNDNode(UMOGOutputNode):
    bl_idname = "umog_SculptNDNode"
    bl_label = "Sculpt ND Node"

    mesh_name = bpy.props.StringProperty()
    stroke_pressure = bpy.props.FloatProperty(min=0.0001, max=2.0, default=1.0)
    stroke_size = bpy.props.IntProperty(default=44)

    def init(self, context):
        # self.inputs.new("BaseInputSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        # layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")
        layout.prop(self, "stroke_pressure", text="Stroke Pressure")
        layout.prop(self, "stroke_size", text="Stroke Size")


    def update(self):
        pass
    
    def execute(self, refholder):
        print("sculpt node execution, mesh: " + self.mesh_name)

        for area in bpy.context.screen.areas:
            print(area.type)
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = bpy.data.objects[self.mesh_name]

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.normals_make_consistent()
                
                bpy.ops.object.mode_set(mode = 'SCULPT')
                
                bpy.data.brushes["SculptDraw"].stroke_method = "DOTS"
                bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
                
                if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
                    bpy.ops.sculpt.dynamic_topology_toggle()

                obj = bpy.context.active_object
                verts = list(obj.data.vertices)
                print(str(len(verts)))

                mouse_width = int(area.width/2)
                mouse_height = int(area.height/2)

                for vert in verts:
                    bpy.ops.sculpt.brush_stroke(ctx, stroke=[{
                        "name": "first",
                        "mouse" : (mouse_width , mouse_height),
                        "is_start": True,
                        "location": obj.matrix_world * vert.co,
                        "pressure": self.stroke_pressure,
                        'pen_flip': False,
                        'time': 1.0,
                        "size": self.stroke_size}])
                bpy.ops.object.mode_set(mode = 'OBJECT')
                print("ALL GOOD!")
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.object.mode_set(mode='OBJECT')
        
    def preExecute(self, refholder):
        #set the texture handle for use in the execute method
        try:
            fn = self.inputs[0].links[0].from_node
            #self.texture_handle = fn.texture_index
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
        self.inputs.new("BaseInputSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        #layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")


    def update(self):
        pass
    
    def execute(self, refholder):
        print("sculpt node execution, mesh: " + self.mesh_name)
        print("  texture_hanlde is: " + str(self.texture_handle))
        obj = bpy.data.objects[self.mesh_name]

        if self.inputs["Input"].is_linked:
            texture_name = self.inputs["Input"].links[0].from_node.texture

            oname="SUBDIV"
            mod = obj.modifiers.new(name=oname, type='SUBSURF')
            bpy.ops.object.modifier_apply(modifier=oname)

            oname="DSIPLACE"
            mod = obj.modifiers.new(name=oname, type='DISPLACE')
            dir(mod)
            mod.texture = bpy.data.textures[texture_name]
            bpy.ops.object.modifier_apply(modifier=oname)

            oname="BEVEL"
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
        self.inputs.new("BaseInputSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        #layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")


    def update(self):
        pass
    
    def execute(self, refholder):
        try:
            print("sculpt node execution, mesh: " + self.mesh_name)
            print("  texture_hanlde is: " + str(self.texture_handle))
        except:
            pass
        
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(bpy.data.meshes[bpy.data.objects[self.mesh_name].data.name])
        
        #bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0.4)
        #bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0, depth=-0.5)
        bmesh.ops.poke(bm, faces=bm.faces)
        
        cx, cy =0,0
        tr = bpy.context.scene.TextureResolution -1
        for vert in bm.verts:
            #displace along normal by texture
            factor = (refholder.np2dtextures[self.texture_handle].item(cx,cy,3)) + 0.1
            print("factor: " + str(factor) + " x:" + str(cx) + " y:" + str(cy))
            print("vertex: " + str(vert.co.x) + "," + str(vert.co.y) + "," + str(vert.co.z))
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
        
        
        bm.to_mesh(bpy.data.meshes[bpy.data.objects[self.mesh_name].data.name])
        bm.free()
        
    def preExecute(self, refholder):
        #set the texture handle for use in the execute method
        try:
            fn = self.inputs[0].links[0].from_node
            self.texture_handle = fn.texture_index
            #copy the mesh and hid the original
        except:
            print("no texture as input")

class BMeshCurlNode(UMOGOutputNode):
    bl_idname = "umog_BMeshCurlNode"
    bl_label = "BMesh Curl Node"

    mesh_name = bpy.props.StringProperty()
    mesh_dupl_name = bpy.props.StringProperty()
    
    mesh_name_index = bpy.props.IntProperty()
    
    
    
    mod_list_handle = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new("BaseInputSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        #layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")


    def update(self):
        pass
    
    def execute(self, refholder):
        try:
            print("sculpt node execution, mesh: " + self.mesh_name)
            print("  texture_hanlde is: " + str(self.texture_handle))
        except:
            pass
        
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(bpy.data.meshes[bpy.data.objects[self.mesh_name].data.name])
        
        #bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0.4)
        #bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0, depth=-0.5)
        bmesh.ops.poke(bm, faces=bm.faces)
        
        cx, cy =0,0
        tr = bpy.context.scene.TextureResolution -1
        for vert in bm.verts:
            #displace along normal by texture
            factor = (refholder.np2dtextures[self.texture_handle].item(cx,cy,3)) + 0.1
            #print("factor: " + str(factor) + " x:" + str(cx) + " y:" + str(cy))
            print("shell factor: " + str(vert.calc_shell_factor()))
            if vert.calc_shell_factor() > 1.01:
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
        
        
        bm.to_mesh(bpy.data.meshes[bpy.data.objects[self.mesh_name].data.name])
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
