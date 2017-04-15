bl_info = {
    "name": "UMOG",
    "author": "Hirad Sabaghian, Micah Johnston, Marsh Poulson, Jacob Luke",
    "version": (0, 0, 2),
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
from bpy.types import NodeTree, Node, NodeSocket
import mathutils

import numpy as np


#begining of code for debugging
#https://wiki.blender.org/index.php/Dev:Doc/Tools/Debugging/Python_Eclipse
#make this match your current installation
try:
    PYDEV_SOURCE_DIR = "/usr/lib/eclipse/plugins/org.python.pydev_5.6.0.201703221358/pysrc"
    import sys
    if PYDEV_SOURCE_DIR not in sys.path:
        sys.path.append(PYDEV_SOURCE_DIR)
    import pydevd
    print("debugging enabled")
except:
    print("no debugging enabled")
#end code for debugging

#will create a breakpoint
#pydevd.settrace()

###############################
#START: PROPERTIES

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

#END: PROPERTIES
################################

################################
# START: PANEL
class HelloWorldPanel(bpy.types.Panel):
    bl_idname = "panel.panel3"
    bl_label = "UMOG"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UMOG"

    def draw(self, context):
        self.layout.operator("umog.bake_meshes", icon='RENDER_RESULT', text="Bake Mesh(es)")
        self.layout.operator("umog.add_keyframe_sample", icon='RENDER_ANIMATION', text="Render Animation")
        self.layout.prop(bpy.context.scene, 'StartFrame')
        self.layout.prop(bpy.context.scene, 'EndFrame')
        self.layout.prop(bpy.context.scene, 'SubFrames')
        self.layout.prop(bpy.context.scene, 'TextureResolution')

# END: PANEL
################################

################################
# START: Sockets
class GetTextureSocket(NodeSocket):
    # Description string
    '''Custom Texture socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'GetTextureSocketType'
    # Label for nice name display
    bl_label = 'Get Texture Socket'
    
    def init(self, context):
        pass
        
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
#        if self.is_output or self.is_linked:
#            layout.label(text)
#        else:
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1, 1, 1, 0.5)
    
class GetObjectSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'GetObjectSocketType'
    # Label for nice name display
    bl_label = 'Get Object Socket'
    
    def init(self, context):
        pass
        
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
#        if self.is_output or self.is_linked:
#            layout.label(text)
#        else:
        layout.label(text=text)

    # Socket colorblender python Property
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
    
class Mat3Socket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Mat3SocketType'
    # Label for nice name display
    bl_label = 'Mat3 Socket'
    
    def init(self, context):
        pass
        
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
#        if self.is_output or self.is_linked:
#            layout.label(text)
#        else:
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 0.0, 1.0, 0.5)
# END: Sockets
################################


################################
# START: Nodes for Firday
#class GetObjectNode(bpy.types.Node):
    #bl_idname = "umog_GetObjectNode"
    #bl_label = "Get Object Node"
    
    ## Enum items list
    #my_items = []
    
    #for ob in bpy.data.objects:
        #my_items.append((ob.name, ob.name, "Type is: " + ob.type))

    #SceneObjectsEnum = bpy.props.EnumProperty(name="Objects", description="Scene objects", items=my_items) 

    #def init(self, context):
        #self.outputs.new("GetObjectSocketType", "Output")
 
    #def draw_buttons(self, context, layout):
        #layout.prop(self, "SceneObjectsEnum")
    
    #def update(self):
        #pass
            
    #def execute(self, refholder):
        #pass

#class ModiferSubdivNode(bpy.types.Node):
    #bl_idname = "umog_SubdivModifier"
    #bl_label = "Subdivision Modifier"
    
    #subdivPreviewCount = bpy.props.IntProperty(default=1)
    #subdivRenderCount = bpy.props.IntProperty(default=1)
    
    #def init(self, context):
        #self.inputs.new("GetObjectSocketType", "Input")

    #def draw_buttons(self, context, layout):
        #layout.prop(self, "subdivPreviewCount", text="Preview")
        #layout.prop(self, "subdivRenderCount", text="Render")

    #def update(self):
        #if self.inputs["Input"].is_linked:
            #print("From Subdiv Update", self.inputs["Input"].links[0].from_node.SceneObjectsEnum)
            #objectName = self.inputs["Input"].links[0].from_node.SceneObjectsEnum
            #bpy.context.scene.objects.active = bpy.data.objects[objectName]
            #if "Subsurf" not in bpy.context.object.modifiers:
                #bpy.ops.object.modifier_add(type='SUBSURF')
                #bpy.ops.object.modifier_move_up(modifier='SUBSURF')
            #if "Subsurf" in bpy.context.object.modifiers:
                #bpy.ops.object.modifier_move_up(modifier='Subsurf')
                #bpy.data.objects[objectName].modifiers["Subsurf"].levels = self.subdivPreviewCount
                #bpy.data.objects[objectName].modifiers["Subsurf"].render_levels = self.subdivRenderCount

            
    #def execute(self, refholder):
        #if self.inputs["Input"].is_linked:
            #print("From Displace Exe", self.inputs["Input"].links[0].from_socket.SelectObjectProp)

#class ModiferDisplaceNode(bpy.types.Node):
    #bl_idname = "umog_ModifierDisplace"
    #bl_label = "Displace Modifier"
    
    #def init(self, context):
        #self.inputs.new("GetObjectSocketType", "Input")
        #self.inputs.new("GetObjectSocketType", "Reference Object")
        #self.inputs.new("GetTextureSocketType", "Texture")
    
    #def update(self):
        #if self.inputs["Input"].is_linked:
            #objectName = self.inputs["Input"].links[0].from_node.SceneObjectsEnum
            #bpy.context.scene.objects.active = bpy.data.objects[objectName]
            #if "Displace" not in bpy.context.object.modifiers:
                #bpy.ops.object.modifier_add(type='DISPLACE')
                #bpy.ops.object.modifier_move_down(modifier='DISPLACE')
        
        #if self.inputs["Texture"].is_linked:
            #objectName = self.inputs["Input"].links[0].from_node.SceneObjectsEnum
            #textureName = self.inputs["Texture"].links[0].from_node.SceneTexturesEnum
            #if "Displace" in bpy.data.objects[objectName].modifiers:
                #bpy.data.objects[objectName].modifiers["Displace"].texture = bpy.data.textures[textureName]
                #bpy.data.objects[objectName].modifiers["Displace"].texture_coords = 'OBJECT'
            
        #if self.inputs["Reference Object"].is_linked:
            #objectName = self.inputs["Input"].links[0].from_node.SceneObjectsEnum
            #referenceName = self.inputs["Reference Object"].links[0].from_node.SceneObjectsEnum
            #if "Displace" in bpy.data.objects[objectName].modifiers:
                #bpy.data.objects[objectName].modifiers["Displace"].texture_coords_object = bpy.data.objects[referenceName]

    #def execute(self, refholder):
        #if self.inputs["Input"].is_linked:
            #print("From Displace Exe", self.inputs["Input"].links[0].from_socket.SelectObjectProp)


# END: Nodes for Friday
################################

class MyItem(bpy.types.PropertyGroup):
    pass

class WM_UL_my_list(bpy.types.UIList):
    pass

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
        print(refholder.np2dtextures[self.texture_index])
        
        
    def preExecute(self, refholder):
        #consider saving the result from this
        self.texture_index = refholder.getRefForTexture2d(self.texture)
    
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


class UMOGNodeTree(bpy.types.NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"
    
    def __init__(self):
        self.refs = UMOGReferenceHolder()
        #if the current scene has parameters do nothing otherwise adde the global start and end frames
        print('initializing umog node tree')
        super().__init__()
        
    def execute(self, refholder):
        print('executing node tree');
        

def drawMenu(self, context):
    if context.space_data.tree_type != "umog_UMOGNodeTree": return
    
    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"
    layout.menu("umog_mesh_menu", text="Mesh", icon = "MESH_DATA")
# from animation nodes
def insertNode(layout, type, text, settings = {}, icon = "NONE"):
    operator = layout.operator("node.add_node", text = text, icon = icon)
    operator.type = type
    operator.use_transform = True
    for name, value in settings.items():
            item = operator.settings.add()
            item.name = name
            item.value = value
    return operator
    
#todo create the menu class
class UMOGMeshMenu(bpy.types.Menu):
    bl_idname = "umog_mesh_menu"
    bl_label = "Mesh Menu"
    
    def draw(self, context):
            layout = self.layout
            insertNode(layout, "umog_MeshInputNode", "Input Mesh")
            insertNode(layout, "umog_PrintNode", "Print")
            insertNode(layout, "umog_GetTextureNode", "Texture")
            #insertNode(layout, "umog_GetObjectNode", "Object")
            #insertNode(layout, "umog_ModifierDisplace", "Displace Modifier")
            #insertNode(layout, "umog_SubdivModifier", "Subdivision Modifier")
            insertNode(layout, "umog_NoiseGenerationNode", "Noise Generator")
            insertNode(layout, "umog_Mat3Node", "Matrix 3x3")

def register():
    print("begin resitration")
    # see for types to register https://docs.blender.org/api/2.78b/bpy.utils.html?highlight=register_class#bpy.utils.register_class
    bpy.types.NODE_MT_add.append(drawMenu)
    bpy.utils.register_class(HelloWorldPanel)
    bpy.utils.register_class(UMOGNodeTree)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(UMOGNodeTree)
    bpy.utils.unregister_module(__name__)
    
