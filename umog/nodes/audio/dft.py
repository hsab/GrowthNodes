from ..umog_node import *
from ...engine import types, engine
import bpy
import sys
import numpy as np

class STFTNode(bpy.types.Node, UMOGNode):

    bl_idname = "umog_STFTNode"
    bl_label = "Short-Time Fourier Transform"
    
    temp_texture_prefix = "_umog_dft"
    texture_name_temp = bpy.props.StringProperty()
    
    samples = bpy.props.IntProperty(default = 1000)

    def init(self, context):
        self.inputs.new("ArraySocketType", "Array")
        self.inputs.new("ArraySocketType", "Parameters")
        self.outputs.new("TextureSocketType", "Spectrogram")
        super().init(context)
        
    def draw_buttons(self, context, layout):
        layout.prop(self, "samples", "samples")
        
    def execute(self, refholder):    
        print("Begin DFT Node")
        
        # Grab the audio and sample rate to run stft on
        audio_array = refholder.matrices[self.inputs[0].links[0].from_socket.matrix_ref]
        audio_properties = refholder.matrices[self.inputs[1].links[0].from_socket.matrix_ref]
        sample_rate = audio_properties[2]
        
        # Set up basic stft parameters
        fft_size = self.samples
        overlap = .5
        hop = np.int32(np.floor((1 - overlap)* fft_size))
        segments = np.int32(np.ceil(len(audio_array) / np.float32(hop)))
        
        # Set up window/hanning stuff
        inner = np.zeros(fft_size)
        windows = np.hanning(fft_size)
        process = np.concatenate((audio_array, np.zeros(fft_size)))
        buckets = np.empty((segments, fft_size), dtype = np.float32)
        
        # Apply fourier transform, apply window, and get absolute value for each segment
        for i in range(0, segments):
            current = hop * i
            current_segment = process[current:current + fft_size]
            current_window = current_segment * windows
            padded = np.append(current_window, inner)
            complex = np.fft.fft(padded) / fft_size
            value = complex.real**2 + complex.imag**2
            buckets[i, :] = value[:fft_size]
        buckets = 20 * np.log10(buckets)
        
        
        # Take each window and find magnitude
        magnitude = {}
        min = 0
        max = 0
        buckets = np.clip(buckets, -40, 200)
        for x in range(0, segments):
            magnitude[x] = {}
            for y in range(0, fft_size):
                value = buckets[x][y]
                if value < min:
                    min = value
                if value > max:
                    max = value
                magnitude[x][y] = value        
                
        # Convert magnitude into RGB value
        spectrogram = {}
        for x in range(0, segments):
            spectrogram[x] = {}
            for y in range(0, fft_size):
                r,g,b = self.rgb(min, max, magnitude[x][y])
                spectrogram[x][y] = [r,g,b]
                
        # Set spectrogram down in texture array
        #self.outputs[0].texture_index = refholder.createRefForTexture2d()
        #refholder.fillTextureRGB(self.outputs[0].texture_index, spectrogram, segments, fft_size)  
        

    def rgb(self, minimum, maximum, value):
        minimum = np.float32(minimum)
        maximum = np.float32(maximum)
        ratio = 2*(value-minimum) / (maximum - minimum)
        color = np.int32(max(0, 255*(1 - ratio)))
        return color, color, color




             