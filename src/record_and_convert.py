import pyaudio
import wave
import time

# from mido import MidiFile
import os
import sys

module_path = os.path.abspath(os.path.join("."))
if module_path not in sys.path:
    sys.path.append(module_path)

from audio2midi import Audio2Midi

from roll import MidiFile

WAVE_OUTPUT_FILENAME = "output.wav"
MIDI_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME + ".midi"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()


print("pause 3 seconds")
time.sleep(3)

audio_2_midi = Audio2Midi()
audio_2_midi.run(WAVE_OUTPUT_FILENAME, MIDI_OUTPUT_FILENAME)
print("pause 3 seconds")
time.sleep(3)

mid = MidiFile(MIDI_OUTPUT_FILENAME)
print("mid")
print(mid)

mid.draw_roll()
