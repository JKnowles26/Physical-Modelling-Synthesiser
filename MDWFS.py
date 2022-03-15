from pyo import *

SAMPLERATE = 44100

def exciter(noiseType='std'):
    if noiseType == 'std':
        n = Noise(.1)
    if noiseType == 'brown':
        n = PinkNoise(.1)
    if noiseType == 'pink':
        n = BrownNoise(.1)
    return n

def waveguide(inp, freq):
    x = 1

def scatterJunc():
    x = 0

s = Server(sr=SAMPLERATE, winhost="asio").boot()
s.start()

notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)  
notes.keyboard()
freqs = MToF(notes["pitch"])

exc = exciter()

tab = NewTable(5000)

def noteon(voice):
    "Print pitch and velocity for noteon event."
    pit = notes["pitch"].get(all=True)[voice]
    pit = midiToHz(pit)
    vel = int(notes["velocity"].get(all=True)[voice] * 127)
    tableLen = (1 / pit) * SAMPLERATE
    print(tableLen)
    TableRec(exc, tab)
    a = TableRead(tab).out()
    print("Noteon: voice = %d, pitch = %f, velocity = %d" % (voice, pit, vel))


tfon = TrigFunc(notes["trigon"], noteon, arg=list(range(10)))
s.gui(locals())