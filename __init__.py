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

class Mat3(bpy.types.PropertyGroup):
    mat00 = bpy.props.FloatProperty(default = 1.0)
    mat01 = bpy.props.FloatProperty()
    mat02 = bpy.props.FloatProperty()
    mat10 = bpy.props.FloatProperty() 
    mat11 = bpy.props.FloatProperty(default = 1.0) 
    mat12 = bpy.props.FloatProperty() 
    mat20 = bpy.props.FloatProperty()
    mat21 = bpy.props.FloatProperty()
    mat22 = bpy.props.FloatProperty(default = 1.0)
    
    def draw(self, context, layout):
        layout.prop(self, "mat00")
        layout.prop(self, "mat01")
        layout.prop(self, "mat02")
        layout.prop(self, "mat10")
        layout.prop(self, "mat11")
        layout.prop(self, "mat12")
        layout.prop(self, "mat20")
        layout.prop(self, "mat21")
        layout.prop(self, "mat22")
        

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

    # Socket color
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
            
    #def execute(self):
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

            
    #def execute(self):
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

    #def execute(self):
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
            
class UMOGReferenceHolder:
    def __init__(self):
        self.references = {}
        
    def getRef(self, key):
        return references[key]
    
    def addRef(self, key, obj):
        references[key] = obj

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
        print(bpy.context.active_node)
        print(bpy.context.selected_nodes)
        bpy.context.active_node.execute()
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

    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout

        layout.template_list(
            "WM_UL_my_list", "",
            self, "collection", self, "collection_index")

    def execute(self, context):
        print("texture selected: " + self.collection[self.collection_index].name)
        print(bpy.context.active_node)
        try:
            bpy.context.active_node.texture = self.collection[self.collection_index].name
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
        self.inputs.new("CustomSocketType", "My Input")
        self.outputs.new("CustomSocketType", "My Output")
        super().init(context)

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

class PrintNode(UMOGNode):
    bl_idname = "umog_PrintNode"
    bl_label = "Print Node"
    
    def init(self, context):
        print('initializing umog print node')
        self.inputs.new("NodeSocketString", "Print String")
        super().init(context)

    def execute(self):
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

    def init(self, context):
        self.outputs.new("GetTextureSocketType", "Output")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.operator("umog.select_texture", text = "Select Texture")

    def update(self):
        pass
            
    def execute(self):
        pass
    
#class Mat3Node(UMOGNode):
    #bl_idname = "umog_Mat3Node"
    #bl_label = "Matrix"

    #matrix = bpy.props.PointerProperty(type=Mat3)

    #def init(self, context):
        #self.outputs.new("Mat3SocketType", "Output")
        #self.inputs.new("Mat3SocketType", "Input")
        #super().init(context)

    #def draw_buttons(self, context, layout):
        #self.matrix.draw(context, layout)

    #def update(self):
        #pass
            
    #def execute(self):
        #pass
    
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
        
    def execute(self):
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
    bpy.utils.register_class(Mat3)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(UMOGNodeTree)
    bpy.utils.unregister_class(Mat3)
    bpy.utils.unregister_module(__name__)
    
