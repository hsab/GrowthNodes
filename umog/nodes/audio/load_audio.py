from ..umog_node import *
from ...engine import types, engine
import bpy
import glob
import os
import re
import numpy as np
import wave
import array

class LoadAudioNode(bpy.types.Node, UMOGOutputNode):
    bl_idname = "umog_LoadAudioNode"
    bl_label = "Load Audio Node"

    temp_audio_prefix = "__umog_audio_loader_"
    audio_name_temp = bpy.props.StringProperty()
    file_path = bpy.props.StringProperty(subtype='DIR_PATH')
    file_name = bpy.props.StringProperty(default="*.wav")
    file_name_diff = bpy.props.IntProperty()

    def init(self, context):
        self.outputs.new("ArraySocketType", "Array")
        self.outputs.new("ArraySocketType", "Parameters")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_path", text="Path")
        layout.prop(self, "file_name", text="File Name")

    def execute(self, refholder):
        index = refholder.execution_scratch[self.name]["index"]        
        file_list = refholder.execution_scratch[self.name]["file_list"]
        path = self.file_path + file_list[index]
        
        wv = wave.open(path, 'rb')
        frames = wv.getnframes()
        data = wv.readframes(frames)
        wv.close()
        # Set up the audio converted to a 1D array        
        audio_array = np.zeros(len(data), dtype=np.int)        
        i = 0
        for elem in data:
            audio_array[i] = elem
            i += 1

        # Set up an array storing audio properties, like number of frames and framerate
        audio_properties = np.zeros(4, dtype=np.int)
        audio_properties[0] = wv.getnchannels()
        audio_properties[1] = wv.getsampwidth()
        audio_properties[2] = wv.getframerate()
        audio_properties[3] = wv.getnframes()
        
        self.outputs[0].matrix_ref = refholder.getRefForMatrix(audio_array)
        self.outputs[1].matrix_ref = refholder.getRefForMatrix(audio_properties)
               
    def preExecute(self, refholder):
        def tryint(s):
            try:
                return int(s)
            except:
                return s

        def alphanum_key(s):
            """ Turn a string into a list of string and number chunks.
                "z23a" -> ["z", 23, "a"]
            """
            return [ tryint(c) for c in re.split('([0-9]+)', s) ]
        pre = os.getcwd()
        os.chdir(self.file_path)
        refholder.execution_scratch[self.name] = {}
        refholder.execution_scratch[self.name]["file_list"] = glob.glob(self.file_name)
        
        #make sure the files are naturally sorted
        #file names with more than one set of digits may fail
        refholder.execution_scratch[self.name]["file_list"] = sorted(refholder.execution_scratch[self.name]["file_list"], key=alphanum_key)
        refholder.execution_scratch[self.name]["index"] = 0
        os.chdir(pre)
        pass
