from ... base_types import UMOGOutputNode
import bpy

class SculptNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SculptNode"
    bl_label = "Sculpt Node"

    mesh_name = bpy.props.StringProperty()
    stroke_pressure = bpy.props.FloatProperty(min=0.0001, max=2.0, default=1.0)
    stroke_size = bpy.props.IntProperty(default=44)
    dyntopo_detail = bpy.props.FloatProperty(min=0.1, max=5, default=1.5, precision=1)

    def init(self, context):
        # self.inputs.new("BaseInputSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        # layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")
        layout.prop(self, "stroke_pressure", text="Stroke Pressure")
        layout.prop(self, "stroke_size", text="Stroke Size")
        layout.prop(self, "dyntopo_detail", text="Precision Level")

    def update(self):
        pass

    def execute(self, refholder):
        # print("sculpt node execution, mesh: " + self.mesh_name)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[self.mesh_name].select = True
        bpy.context.scene.objects.active = bpy.data.objects[self.mesh_name]

        for area in bpy.context.screen.areas:
            # print(area.type)
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]

                bpy.ops.view3d.view_selected(ctx)

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.normals_make_consistent()

                bpy.ops.object.mode_set(mode='SCULPT')

                bpy.data.brushes["SculptDraw"].stroke_method = "DOTS"
                bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False

                if not bpy.context.sculpt_object.use_dynamic_topology_sculpting:
                    bpy.ops.sculpt.dynamic_topology_toggle()
                    bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
                    bpy.context.scene.tool_settings.sculpt.constant_detail = self.dyntopo_detail

                obj = bpy.context.active_object
                verts = list(obj.data.vertices)

                mouse_width = int(area.width / 2)
                mouse_height = int(area.height / 2)

                for vert in verts:
                    bpy.ops.sculpt.brush_stroke(ctx, stroke=[{
                        "name": "first",
                        "mouse": (mouse_width, mouse_height),
                        "is_start": True,
                        "location": obj.matrix_world * vert.co,
                        "pressure": self.stroke_pressure,
                        'pen_flip': False,
                        'time': 1.0,
                        "size": self.stroke_size}])
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.view3d.view_selected(ctx)
                print("SCULPT DYNAMIC FINISHED")

    def preExecute(self, refholder):
        pass