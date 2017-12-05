from ...base_types import UMOGOutputNode
import bpy
import numpy as np
from mathutils import Vector


class DisplaceNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_DisplaceNode"
    bl_label = "Displace"

    assignedType = "Object"

    mesh_name = bpy.props.StringProperty()
    mesh_dupl_name = bpy.props.StringProperty()

    texture_name_temp = bpy.props.StringProperty()

    mesh_name_index = bpy.props.IntProperty()

    # use_subdiv = bpy.props.BoolProperty(default=True)
    mod_midlevel = bpy.props.FloatProperty(min = 0.0, max = 1.0, default = 0.5)
    mod_strength = bpy.props.FloatProperty(default = 1.0)

    def create(self):
        self.newInput(self.assignedType, "Object")
        self.newInput("VertexGroup", "Vertex Group")
        socket = self.newInput("Texture2", "Texture")
        self.newInput("Float", "Midlevel", value = 0.5)
        self.newInput("Float", "Strength", value = 0.1)
        socket = self.newOutput(self.assignedType, "Output")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False
        socket = self.newOutput("VertexGroup", "Vertex Group")
        socket.display.refreshableIcon = False
        socket.display.packedIcon = False

    def refresh(self):
        if self.inputs[0].value == '':
            self.inputs[1].value = ''
            self.inputs[1].object = ''
        else:
            self.inputs[1].object = self.inputs[0].value

        self.outputs[0].value = self.inputs[0].value
        self.outputs[0].refresh()

        self.outputs[1].value = self.inputs[1].value
        self.outputs[1].refresh()

    def execute(self, refholder):
        self.inputs[0].setViewObjectMode()
        self.inputs[0].setSelected()

        obj = self.inputs[0].getObject()
        vertexGroup = self.inputs[1].value
        texture = self.inputs[2].getTexture()
        midLevel = self.inputs[3].value
        strength = self.inputs[4].value

        # Is Object and Texture are Linked
        if self.inputs[0].is_linked and self.inputs[2].value != '':
            objData = obj.data
            # objData.calc_normals_split()
            shapeKeys = None
            hasShapes = objData.shape_keys is not None

            if hasShapes:
                shapeKeys = objData.shape_keys.key_blocks
                keyNorms = shapeKeys[-1].normals_vertex_get()
                print(shapeKeys[-1].name)
                npNorms = np.asarray(keyNorms, dtype="float")
                npNorms = npNorms.reshape((len(objData.vertices), 3))

                objData.normals_split_custom_set_from_vertices(npNorms)
                objData.use_auto_smooth = True

                shapeKeys[-1].value = 0
            else:
                self.resetNormals(objData)

            oname = "DISPLACE"
            mod = obj.modifiers.new(name = oname, type = 'DISPLACE')
            mod.texture = texture
            mod.mid_level = midLevel
            mod.strength = strength
            if hasShapes:
                mod.direction = 'CUSTOM_NORMAL'
            else:
                mod.direction = 'NORMAL'

            if vertexGroup != '':
                mod.vertex_group = vertexGroup

            bpy.ops.object.modifier_apply(modifier = oname, apply_as = "SHAPE")

            if shapeKeys is None:
                shapeKeys = objData.shape_keys.key_blocks

            soFarShape = shapeKeys[-2]
            soFarShape.value = 1

            dispShape = shapeKeys[-1]
            dispShape.value = 1

            bpy.ops.object.shape_key_add(from_mix = True)
            obj.shape_key_remove(dispShape)
            soFarShape.value = 0
            accumShape = shapeKeys[-1]

            accumShape.value = 1

            bakeCount = self.nodeTree.properties.bakeCount
            accumShape.name = "baked_umog_" + str(bakeCount) + "_displace_" + str(
                bpy.context.scene.frame_current)

            obj.update_from_editmode()

            obj.hasUMOGBaked = True
            obj.bakeCount = bakeCount

            if bakeCount not in obj.data.bakedKeys:
                obj.data.bakedKeys[bakeCount] = []

            obj.data.bakedKeys[bakeCount].append(accumShape)
        else:
            print("no texture specified")

    def write_keyframe(self, refholder, frame):
        pass
        # obj = bpy.data.objects[self.mesh_name]
        # for vertex in obj.data.vertices:
        #     vertex.keyframe_insert(data_path='co', frame=frame)

    def preExecute(self, refholder):
        self.inputs[0].setSelected()
        obj = self.inputs[0].getObject()
        objData = obj.data
        hasShapes = objData.shape_keys is not None

        if hasShapes:
            shapeKeys = objData.shape_keys.key_blocks
            bpy.ops.object.shape_key_add(from_mix = True)

            while len(shapeKeys) > 0:
                obj.active_shape_key_index = 0
                bpy.ops.object.shape_key_remove(all = False)

    def postBake(self, refholder):
         obj = self.inputs[0].getObject()
         self.resetNormals(obj.data)

    def resetNormals(self, objData):
        objData.use_auto_smooth = False
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
