from ..umog_node import *
from ...engine import types, engine
import bpy
import numpy as np
import array
import wave


class SaveAudioNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_SaveAudioNode"
    bl_label = "Save Audio"

    temp_audio_prefix = "__umog_audio_saver_"
    audio_name_temp = bpy.props.StringProperty()

    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="wav")
    file_name_diff = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new("ArraySocketType", "Array")
        self.inputs.new("ArraySocketType", "Parameters")
        super().init(context)
        
    def draw_buttons(self, context, layout):
        layout.prop(self, "file_path", text="Path")
        layout.prop(self, "file_name", text="File Name")

    def execute(self, refholder):
    
        print("Begin Save Audio")
        
        audio_array = refholder.matrices[self.inputs[0].links[0].from_socket.matrix_ref]
        audio_properties = refholder.matrices[self.inputs[1].links[0].from_socket.matrix_ref]        
        data = array.array('B')
        
        for elem in audio_array:
            data.append(elem)
        
        path = self.file_path + self.file_name + str(self.file_name_diff) + ".wav"
        
        output = wave.open(path, 'w')
        output.setparams((audio_properties[0], audio_properties[1], audio_properties[2], audio_properties[3], 'NONE', 'not compressed'))
        output.writeframes(data.tostring())

        self.file_name_diff = self.file_name_diff + 1
        pass

    def preExecute(self, refholder):
        self.file_name_diff = 0
        pass
