import numpy
from pyo import *
SAMPLERATE = 44100

s = Server(sr=SAMPLERATE, winhost="asio").boot()
s.start()


s.gui(locals())