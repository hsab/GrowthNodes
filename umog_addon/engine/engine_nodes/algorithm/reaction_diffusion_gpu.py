from ..engine_node import EngineNode
import bpy
from ...engine import types, engine
import numpy as np

class ReactionDiffusionNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_ReactionDiffusionGPUNode"
    bl_label = "Reaction Diffusion GPU"

    feed = bpy.props.FloatProperty(default=0.055, precision=4, soft_min=0.0)
    kill = bpy.props.FloatProperty(default=0.062, precision=4, soft_min=0.0)
    Da = bpy.props.FloatProperty(default=0.1, precision=4, soft_min=0.0)
    Db = bpy.props.FloatProperty(default=0.1, precision=4, soft_min=0.0)
    dt = bpy.props.FloatProperty(default=0.2, precision=4, soft_min=0.0)
    iterations = bpy.props.IntProperty(default=500, soft_min=1)

    def init(self, context):
        self.inputs.new("ArraySocketType", "A")
        self.inputs.new("ArraySocketType", "B")
        self.outputs.new("ArraySocketType", "A'")
        self.outputs.new("ArraySocketType", "B'")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "feed", "Feed")
        layout.prop(self, "kill", "Kill")
        layout.prop(self, "Da", "Da")
        layout.prop(self, "Db", "Db")
        layout.prop(self, "dt", "dt")
        layout.prop(self, "iterations", "iterations")

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.REACTION_DIFFUSION_GPU_STEP,
            [input_types[0], input_types[0], types.Array(6,0,0,0,0,0)],
            input_types,
            [1])

    def get_default_value(self, index, argument_type):
        return np.array([self.Da, self.Db, self.dt, self.iterations, self.feed, self.kill], dtype=np.float32, order="F").reshape((6,1,1,1,1))

    def update(self):
        pass
