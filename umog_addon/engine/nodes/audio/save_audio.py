from ..engine_node import *
from ...engine import types, engine
import bpy
import numpy as np
import array
import wave


class SaveAudioNode(bpy.types.Node, EngineOutputNode):
    bl_idname = "engine_SaveAudioNode"
    bl_label = "Save Audio"

    temp_audio_prefix = "__engine_audio_saver_"
    audio_name_temp = bpy.props.StringProperty()

    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="wav")
    file_name_diff = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new("ArraySocketType", "Array")
        # self.inputs.new("ArraySocketType", "Parameters")
        super().init(context)
        
    def draw_buttons(self, context, layout):
        layout.prop(self, "file_path", text="Path")
        layout.prop(self, "file_name", text="File Name")

    def get_operation(self, input_types):
        types.assert_type(input_types[0], types.ARRAY)

        return engine.Operation(
            engine.OUT,
            input_types,
            [],
            [])

    def output_value(self, value):
        audio_array = value.array
        data = array.array('i')
        
        for i in range(audio_array.shape[4]):
            sample = audio_array[0,0,0,0,i]
            data.append(int(sample * 127))
        
        path = self.file_path + self.file_name + str(self.file_name_diff) + ".wav"
        
        output = wave.open(bpy.path.abspath(path), 'w')
        output.setparams((1, 2, 44100, audio_array.shape[4], 'NONE', 'not compressed'))
        output.writeframes(data.tobytes())
        output.close()

        self.file_name_diff = self.file_name_diff + 1
