from tkinter import N
from pyo import *
def exciter(noiseType='white', mul=1, add=0):
    if noiseType == 'white':
        n = Noise(mul, add)
    elif noiseType == 'pink':
        n = PinkNoise(mul, add)
    elif noiseType == 'brown':
        n = BrownNoise(mul, add)
    return n

def getPitch(voice):
    pitch = int(note["pitch"].get(all=True)[voice])
    print(pitch)
    return pitch
SAMPLERATE = 44100
BUFFERSIZE = 128

#Set server settings and boot
s = Server(sr=SAMPLERATE, buffersize=256, duplex=0)
s.setMidiInputDevice(99)
s.boot()
s.start()

note = Notein(poly=10, scale=0, first=0, last=127)
note.keyboard()

pit = note["pitch"]
freqs = MToF(pit)
amp = MidiAdsr(note["velocity"], attack=0.001, decay=0.1, sustain=0.7, release=0, mul=0.1,)

exc = exciter(noiseType='white', mul=amp)

d = Delay(exc, 1/freqs, 0)
filt = exc + (0.99*d)
d.setInput(filt)
d.out()
s.gui(locals())

