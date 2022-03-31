from scipy import rand
import ctcsound
import librosa
from librosa import display
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import SGDRegressor
import random
import copy
#Load waveguide models

def setParams(p):
  csd = '''
  <CsoundSynthesizer>

  <CsOptions>
    -d -o render.wav -m0
  </CsOptions>

  <CsInstruments>
  sr     = 48000
  kr     = 4800
  nchnls = 2
  0dbfs  = 1
            instr 1
  ifreq     =         p4
  iamp      =         p5
  iatt      =         p6
  isus      =         p7
  irel      =         p8
  inType    =         p9
  inFilt    =         p10
  ifilt     =         p11
  ifdbk     =         p12
  inGain    =         p13
  ifltr1Tog =         p14
  ifltr1Cut =         p15
  inlTog    =         p16
  ifltr2Tog =         p17
  ifltr2Cut =         p18


  isec      =         1 / ifreq
  asec      =         1 / ifreq

  if (inType == 0) then
    a1      noise     iamp, inFilt
  elseif (inType == 1) then
    a1      fractalnoise  iamp, 2
  elseif (inType == 2) then
    a1      oscil     iamp, ifreq
  endif

  kenv      madsr     iatt, isec, isus, irel 

  a1        =         a1 * inGain
  a1        =         a1 * kenv

  if (ifltr1Tog == 1) then
    a1      tone      a1, ifltr1Cut
  endif

  a2        delayr    1
  a3        deltapi   asec
  a4        tone      a3, ifilt
  if (inlTog == 1) then
    a4      tanh      a4
  endif
            delayw    a1 + (a4 * ifdbk)
  if (ifltr2Tog == 1) then
    a4      tone      a4, ifltr2Cut
  endif
            outs      a4, a4
            endin
  </CsInstruments>
  <CsScore>
  ; 1 2 3 4   5    6   7 8 9 10 11    12    131415  161718
  i 1 0 12 220 '''
  for parameter in p:
    csd += str(parameter) + " "
  csd += "\n"
  csd += '''
  </CsScore>
  </CsoundSynthesizer>    
  '''

  return csd

def initModel():
  p = [0.05, 0.1, 0, 0, 0, 0.3, 3000, 0.997, 1, 1, 500, 1, 1, 4000]
  p = np.array(p)
  return p

def adjustParams(p, learnRate):
  newP = copy.deepcopy(p)
  newP[0] += random.uniform(-0.01, 0.01) * learnRate
  if newP[0] <= 0:
    newP[0] = 0.01
  newP[1] += random.uniform(-0.1, 0.1) * learnRate
  if newP[1] <= 0:
    newP[1] = 0.01
  newP[2] += random.uniform(-0.1, 0.1) * learnRate
  if newP[2] < 0:
    newP[2] = 0
  newP[3] += random.uniform(-0.1, 0.1) * learnRate
  if newP[3] < 0:
    newP[3] = 0
  newP[4] += random.randrange(-1, 1) * learnRate
  if newP[4] > 2:
    newP[4] = 2
  elif newP[4] < 0:
    newP[4] = 0
  newP[5] += random.uniform(-0.1, 0.1) * learnRate
  if newP[5] > 0.99:
    newP[5] = 0.99
  elif newP[5] < -0.99:
    newP[5] = -0.99
  newP[6] += random.randrange(-10, 10) * learnRate
  if newP[6] < 0:
    newP[6] = 0
  elif newP[6] > 10000:
    newP[6] = 10000
  newP[7] += random.uniform(-0.001, 0.001) * learnRate
  if random.randint(0, 100) > 90:
    newP[7] *= -1
  newP[8] += random.uniform(-0.1, 0.1) * learnRate
  if random.randint(0, 100) > 90:
    if newP[9] == 0:
      newP[9] = 1
    else:
      newP[9] = 0
  newP[10] += random.randrange(-10, 10) * learnRate
  if newP[10] < 0:
    newP[10] = 0
  elif newP[10] > 10000:
    newP[10] = 10000
  if random.randint(0, 100) > 90:
    if newP[11] == 0:
      newP[11] = 1
    else:
      newP[11] = 0
  if random.randint(0, 100) > 90:
    if newP[12] == 0:
      newP[12] = 1
    else:
      newP[12] = 0
  newP[13] += random.randrange(-10, 10) * learnRate
  if newP[13] < 0:
    newP[13] = 0
  elif newP[13] > 10000:
    newP[13] = 10000
  return newP

#Initialisation
p = initModel()
csd = setParams(p)
#Get training data
dataDir = os.path.join(os.getcwd(), 'SoundFiles', 'Strings')
wavFname = os.path.join(dataDir, 'bassDrumHit.wav')
trainData, sr = librosa.load(wavFname, sr=44100)
trainLen = trainData.shape[0]
trainMfccs = librosa.feature.mfcc(y=trainData, sr=sr, n_mfcc= 50)

#Machine Learning Loop
epochs = 50
learningRate = 10

prevDist = 100000
losses = []
newP = p

for x in range(epochs):
  #CODE TO RENDER CSOUND FILE
  csd = setParams(newP)
  cs = ctcsound.Csound()  
  cs.createMessageBuffer(toStdOut=False)
  ret = cs.compileCsdText(csd)
  test = []
  if ret == ctcsound.CSOUND_SUCCESS:
      cs.start()
      cs.perform()
      #cs.reset()
  print(x)
  #Get current Estimate
  currInst, sr = librosa.load('Render.wav', sr=44100)
  currInstTrim = currInst[0:trainLen]

  #Calculate Mfccs
  learnMfccs = librosa.feature.mfcc(y=currInstTrim, sr=sr, n_mfcc= 50)

  #Calculate Euclidian distance (loss)
  dist = np.linalg.norm(trainMfccs - learnMfccs)

  #Adjust Parameters randomly
  print(dist, " ~ ", prevDist)
  if dist < prevDist:
    pLoss = dist
    print("saved Dist")
    p = copy.deepcopy(newP)
    prevDist = dist

  newP = adjustParams(p, learningRate)
  losses.append(pLoss)
  learningRate *= 0.95
  print(learningRate)

plt.plot(losses)
plt.show()
print(p)
csd = setParams(p)
cs = ctcsound.Csound()  
cs.createMessageBuffer(toStdOut=False)
ret = cs.compileCsdText(csd)
test = []
if ret == ctcsound.CSOUND_SUCCESS:
    cs.start()
    cs.perform()