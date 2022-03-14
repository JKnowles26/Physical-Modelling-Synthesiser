from pyo import *

def exciter(adsr, noiseType='std'):
    if noiseType == 'std':
        n = Noise(adsr)
    if noiseType == 'brown':
        n = PinkNoise(.1)
    if noiseType == 'pink':
        n = BrownNoise(.1)
    return n

def waveguide(inp, freq):
    x = 1

def scatterJunc():
    x = 0

s = Server(winhost="asio").boot()
s.start()

notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)  
notes.keyboard()

adsr = Adsr(0.01, 0.05, 0.707, 0.1, 2,0.5)


s.gui(locals())