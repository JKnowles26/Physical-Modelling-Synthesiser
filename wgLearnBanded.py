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
    -d -o dac -m0
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
  if1Tog    =         p14
  if1Hz     =         p15
  ib1cf     =         p16
  ib1bw     =         p17
  ib2cf     =         p18
  ib2bw     =         p19
  ib3cf     =         p20
  ib3bw     =         p21
  ib4cf     =         p22
  ib4bw     =         p23
  idel1     =         p24
  idel2     =         p25
  idel3     =         p26
  igain1    =         p27
  igain2    =         p28
  igain3    =         p29
  igain4    =         p30
  if2Tog    =         p31
  if2Hz     =         p32

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

  if (if1Tog == 1) then
    a2      tone      a1, if1Hz
  else
    a2      =         a1
  endif

  ab1       resonr    a2, ib1cf, ib1bw
  ab2       resonr    a2, ib2cf, ib2bw
  ab3       resonr    a2, ib3cf, ib3bw
  ab4       resonr    a2, ib4cf, ib4bw

  agarb     delayr    1
  agarb     delayr    1
  agarb     delayr    1
  agarb     delayr    1

  ad1       deltapi   isec * idel1
  ad2       deltapi   isec * idel2
  ad3       deltapi   isec * idel3
  ad4       deltapi   isec
  
            delayw    ab1
            delayw    ab2
            delayw    ab3
            delayw    ab4

  afdbk      =         ifdbk * (ad1 + ad2 + ad3 + ad4)

  a1         =         a1 + afdbk

  adg1       =         ad1 * igain1
  adg2       =         ad2 * igain2
  adg3       =         ad3 * igain3
  adg4       =         ad4 * igain4
  if (if2Tog == 1) then
    aout     tone      (adg1 + adg2 + adg3 + adg4), if2Hz
  else 
    aout     =         adg1 + adg2 + adg3 + adg4
  endif

            outs      aout, aout
            endin
  </CsInstruments>

  <CsScore>
  ; 1 2 3  4  5   6   7 8 9  10  11   12   131415   16   17  18   19  20   21  22   23  24  25   26  27   28   29   30   3132
  i 1 0 5 440 '''
  for parameter in p:
      csd += str(parameter) + " "
  csd += "\n"
  csd += '''
  e
  </CsScore>
  </CsoundSynthesizer>      
    '''

  return csd

def initModel():
  p = [0.6, 0.1, 0, 0, 0, -0.5, 5000, 0.99, 1, 1, 2000, 2000, 200, 2000, 200, 2000, 200, 2000, 200, 0.1, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 1, 5000]
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
wavFname = os.path.join(dataDir, 'tromboneA3Piano.wav')
trainData, sr = librosa.load(wavFname, sr=44100)
trainLen = trainData.shape[0]
trainSpecs = librosa.feature.melspectrogram(y=trainData, sr=sr, hop_length=512)

#Machine Learning Loop
epochs = 150
learningRate = 10

prevDist = 100000
losses = []
newP = p
cs = ctcsound.Csound()  


# for x in range(epochs):
#   #CODE TO RENDER CSOUND FILE
#   csd = setParams(newP)
#   ret = cs.compileCsdText(csd)
#   cs.createMessageBuffer(toStdOut=False)
#   test = []
#   if ret == ctcsound.CSOUND_SUCCESS:
#       cs.start()
#       cs.perform()
#       cs.reset()
#   print(x)
#   #Get current Estimate
#   currInst, sr = librosa.load('Render.wav', sr=44100)
#   currInstTrim = currInst[0:trainLen]

#   #Calculate Mfccs
#   learnSpecs = librosa.feature.melspectrogram(y=currInstTrim, sr=sr, hop_length=512)

#   #Calculate Euclidian distance (loss)
#   dist = np.linalg.norm(trainSpecs - learnSpecs)

#   #Adjust Parameters randomly
#   print(dist, " ~ ", prevDist)
#   if dist < prevDist:
#     pLoss = dist
#     print("saved Dist")
#     p = copy.deepcopy(newP)
#     prevDist = dist

#   newP = adjustParams(p, learningRate)
#   losses.append(pLoss)
#   learningRate *= 0.99
#   print(learningRate)

# plt.plot(losses)
# plt.show()
# print(p)
csd = setParams(p)
cs = ctcsound.Csound()  
# display.specshow(trainSpecs)
# plt.show()
# display.specshow(learnSpecs)
# plt.show()
# cs.createMessageBuffer(toStdOut=False)
ret = cs.compileCsdText(csd)
test = []
if ret == ctcsound.CSOUND_SUCCESS:
    cs.start()
    cs.perform()