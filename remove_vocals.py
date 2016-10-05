import sys
import wave
import contextlib
import pygame
import audioop
import sound
import pygraphics

def length(file_name):
    with contextlib.closing(wave.open(file_name,'r')) as f:
    	frames = f.getnframes()
    	return frames

def read_samples(file_name, nb_frames):
        f = wave.open(file_name,"rb")
        frame_data = f.readframes(nb_frames)
        frame_data = str(frame_data)
        sample_width = f.getsampwidth()
        nb_samples = len(frame_data) // sample_width
        return nb_samples
    
def open_file(file_path):
    return sound.load_sound(file_path)

def remove_vocals(sound_obj,file_name):
    num_frames = length(file_name)
    num_samples = read_samples(file_name,num_frames)
    new_sound = sound.create_pygame_sound(num_samples)
    for i in range(num_samples):
        orig_samp = sound.get_sample(sound_obj,i)
        new_samp = sound.get_sample(new_sound,i)
        left_ch = sound.get_left(orig_samp)
        right_ch = sound.get_right(orig_samp)
        result = int( (left_ch - right_ch) / 2.0 )
        sound.set_left(new_samp,result)
        sound.set_right(new_samp,result)
    return new_samp

file_name = sys.argv[1]
with contextlib.closing(wave.open(file_name,'r')) as sound_obj:
#sound_obj = open(file_name,"rb")
	new_sound = remove_vocals(sound_obj,file_name)
new_file_name = file_name_split[0] + '_novoice' + '.wav' 
new_sound.save_as(new_file_name)


