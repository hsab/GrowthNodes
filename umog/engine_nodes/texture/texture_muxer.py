from ..engine_node import *

import bpy
import numpy as np
#import pyximport
#pyximport.install()


class EngineTexture3LatheNode(bpy.types.Node, EngineNode):
    bl_idname = "engine_Texture_Muxer_Node"
    bl_label = "Muxer Node"
    
    red = bpy.props.EnumProperty(items=
            (
            ('-1', 'Ones', ''),
            ('0', 'Zeros', ''),
            ('1', 'Red', ''),
            ('2', 'Green', ''),
            ('3', 'Blue', ''),
            ('4', 'Alpha', ''),
            ),
            default="4")
            
    blue = bpy.props.EnumProperty(items=
            (
            ('-1', 'Ones', ''),
            ('0', 'Zeros', ''),
            ('1', 'Red', ''),
            ('2', 'Green', ''),
            ('3', 'Blue', ''),
            ('4', 'Alpha', ''),
            ),
            default="4")
    green = bpy.props.EnumProperty(items=
            (
            ('-1', 'Ones', ''),
            ('0', 'Zeros', ''),
            ('1', 'Red', ''),
            ('2', 'Green', ''),
            ('3', 'Blue', ''),
            ('4', 'Alpha', ''),
            ),
            default="4")
            
    alpha = bpy.props.EnumProperty(items=
            (
            ('-1', 'Ones', ''),
            ('0', 'Zeros', ''),
            ('1', 'Red', ''),
            ('2', 'Green', ''),
            ('3', 'Blue', ''),
            ('4', 'Alpha', ''),
            ),
            default="-1")
    
    def init(self, context):
        self.inputs.new("ArraySocketType", "A")
        self.outputs.new("ArraySocketType", "A'")
        
        
            
        

    def draw_buttons(self, context, layout):
        layout.prop(self, "red", "Red")
        layout.prop(self, "green", "Green")
        layout.prop(self, "blue", "Blue")
        layout.prop(self, "alpha", "Alpha")

            
    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)
        return engine.Operation(
            engine.MUX_CHANNELS,
            input_types,
            input_types,
            [int(self.red), int(self.green), int(self.blue), int(self.alpha)])

    def get_buffer_values(self):
        return []
