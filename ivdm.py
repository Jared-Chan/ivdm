#!/usr/bin/env python3

import sys
import math
import librosa
import soundfile as sf
import numpy as np
import scipy

# Loads and processes audio file
# path: path to audio file
# beats: segment length in beats
# returns: sample rate, numpy array of processed audio
def tile_segments(path, beats, debug=False):

  y_duo, sr = librosa.load(path, sr=None, mono=False)

  combined_duo = []
  for y in y_duo:
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_samples = librosa.frames_to_samples(beat_frames)

    # Find the number of samples between two beats
    intervals = [beat_samples[0]]
    for i in range(1, len(beat_samples)):
      intervals = np.append(intervals, beat_samples[i] - beat_samples[i-1])
    interval = scipy.stats.mode(intervals)

    interval = interval[0][0] * beats
    num_of_seg = math.floor(y.shape / interval)

    # Split audio into segments and tile each segment
    tiled_segments = []
    for i in range(0, num_of_seg):
      start = interval * i
      end = start + interval
      seg = y[start : end]
      if (i == 0):
        lenseg = len(seg)
      elif (lenseg != len(seg)):
        # this part should not be reached
        if (debug):
          print(f'len not equal, {i}, {lenseg}, {len(seg)}, {num_of_seg}')
          input()
        elif (lenseg < len(seg)):
          seg = seg[:lenseg]
        else:
          add_padding = np.zeros(lenseg)
          add_padding[:len(seg)] = seg
          seg = add_padding


      tiled = np.tile(np.array(seg), num_of_seg)
      tiled_segments.append(tiled)


    # Adjust the volume of each loop of a segment
    for i in range(len(tiled_segments)):
      for j in range(len(tiled_segments)):
        distance = min(abs(i - j), abs(len(tiled_segments) + i - j))
        factor = 1 - distance / (len(tiled_segments)/2)
        start = interval * j
        end = start + interval
        tiled_segments[i][ start: end] *= factor**3


    combined_segments = np.sum(np.array(tiled_segments), axis=0)
    combined_duo.append(combined_segments)

  if (len(combined_duo[0]) < len(combined_duo[1])):
    combined_duo[1] = combined_duo[1][:len(combined_duo[0])]
  elif (len(combined_duo[1]) < len(combined_duo[0])):
    combined_duo[0] = combined_duo[0][:len(combined_duo[1])]

  return sr, combined_duo

# Processes audio file and stores result
# input_path: input path
# output_path: output path
# segment_length: length of each segment in number of beats
def process_audio(input_path, output_path, segment_length):
  sample_rate, audio_array = tile_segments(input_path, segment_length)
  audio_array = np.transpose(audio_array)
  sf.write(output_path, audio_array, sample_rate)



if __name__=='__main__':
    help_message = """
    ivdm -- makes 4-Dimensional music
    Usage:
        ivdm.py <input> <output> <segment_length>

    Usage (Windows):
        python3 ivdm.py <input> <output> <segment_length>

    Options:
        <input>             Input audio file.
        <output>            Output audio file. Should be WAV or FLAC.
                            Default is './ivdm_out.wav'
        <segment_length>    Length of segments used in making 4-D music. Measured in the number of beats.
                            Default is 32. Longer sengment lengths give cleaner music that resembles the
                            input more. Shorter segment lengths give music with more sounds at any moment.
        -h                  Show this message.

    Examples:
        ivdm.py ./music.wav
        ivdm.py ./music2.mp3 ./musictwo.wav 64

    Examples (Windows):
        python3 ivdm.py ./music.wav
        python3 ivdm.py ./music2.mp3 ./musictwo.wav 64

    """
    args = len(sys.argv)
    if (args == 1 or sys.argv[1] == "help" or sys.argv[1] == "-h"):
        print(help_message)
    elif (args == 2):
        process_audio(sys.argv[1], './ivdm_out.wav', 32)
    elif (args == 4):
        process_audio(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    else:
        print(help_message)
