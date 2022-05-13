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
if1Tog    =         p14
if1Hz     =         p15
ib1bw     =         p16
ib2bw     =         p17
ib3bw     =         p18
ib4bw     =         p19
ib5bw     =         p20
idel1     =         p21
idel2     =         p22
idel3     =         p23
idel4     =         p24
igain1    =         p25
igain2    =         p26
igain3    =         p27
igain4    =         p28
igain5    =         p29
if2Tog    =         p30
if2Hz     =         p31

afdbk init 0
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

a2 = a2 + afdbk
ab1       butterbp    a2, ifreq, ib1bw
ab2       butterbp    a2, ifreq*idel1, ib2bw
ab3       butterbp    a2, ifreq*idel2, ib3bw
ab4       butterbp    a2, ifreq*idel3, ib4bw
ab5       butterbp    a2, ifreq*idel4, ib5bw

agarb     delayr    1
ad1       deltapi   isec
          delayw    ab1 

agarb     delayr    1
ad2       deltapi   isec  * (1/idel1)
          delayw    ab2

agarb     delayr    1
ad3       deltapi   isec * (1/idel2)
          delayw    ab3

agarb     delayr    1
ad4       deltapi   isec * (1/idel3)
          delayw    ab4 

agarb     delayr    1
ad5       deltapi   isec * (1/idel3)
          delayw    ab5

afdbk      =         ifdbk * (ad1 + ad2+ ad3+ad4)

adg1       =         ad1 * igain1
adg2       =         ad2 * igain2
adg3       =         ad3 * igain3
adg4       =         ad4 * igain4
adg5       =         ad5 * igain5
if (if2Tog == 1) then
  aout     tone      (adg1 + adg2 + adg3 + adg4 + adg5), if2Hz
else 
  aout     =         adg1 + adg2 + adg3 + adg4 + adg5
endif

          outs      aout, aout
          endin
</CsInstruments>

<CsScore>
; 1 2 3 4   5 6      7 8   9 10   11    12   131415   16  17    18   19   20   21   22  23  24  25262728293031
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
  p = [1, 0.0001, 0, 0.4, 0, -0.5, 10000, 0.5, 1, 0, 2000, 1000, 1000, 1000, 1000, 1000, 2.1, 3.2, 4.1, 4.9, 1, 1, 1, 1, 1, 0, 5000]
  p = np.array(p)
  return p

def adjustParams(p, learnRate):
  newP = copy.deepcopy(p)
  #Amplitude
  newP[0] += random.uniform(-0.05, 0.05) * learnRate
  if newP[0] <= 0.5:
    newP[0] = 0.5 
  #Attack
  newP[1] += random.uniform(-0.001, 0.001) * learnRate
  if newP[1] <= 0:
    newP[1] = 0.0001
  #Sustain
  newP[2] += random.uniform(-0.001, 0.001) * learnRate
  if newP[2] < 0:
    newP[2] = 0
  newP[2] = 0
  #Release
  newP[3] += random.uniform(-0.001, 0.001) * learnRate
  if newP[3] < 0:
    newP[3] = 0
  newP[3] = 0
  #Noise Type
  newP[4] += random.randrange(-1, 1) * learnRate
  if newP[4] > 2:
    newP[4] = 2
  elif newP[4] < 0:
    newP[4] = 0
  #Noise Filter
  newP[5] += random.uniform(-0.1, 0.1) * learnRate
  if newP[5] > 0.99:
    newP[5] = 0.99
  elif newP[5] < -0.99:
    newP[5] = -0.99
#Loop Filter
  newP[6] += random.randrange(-10, 10) * learnRate
  if newP[6] < 0:
    newP[6] = 0
  elif newP[6] > 10000:
    newP[6] = 10000
#Feedback
  newP[7] += random.uniform(-0.001, 0.001) * learnRate
  if random.randint(0, 100) > 90:
    newP[7] *= -1
#Input Gain
  newP[8] += random.uniform(-0.1, 0.1) * learnRate
#Toggle filter 1
  if random.randint(0, 100) > 90:
    if newP[9] == 0:
      newP[9] = 1
    else:
      newP[9] = 0
#Filter 1 Hz
  newP[10] += random.randrange(-10, 10) * learnRate
  if newP[10] < 0:
    newP[10] = 0
  elif newP[10] > 10000:
    newP[10] = 10000
#Filter 1 Bandwidth
  newP[11] += random.randrange(-10, 10) * learnRate
  if newP[11] < 100:
    newP[11] = 100
  elif newP[11] > 2000:
    newP[11] = 2000
#Filter 2 Bandwidth
  newP[12] += random.randrange(-10, 10) * learnRate
  if newP[12] < 100:
    newP[12] = 100
  elif newP[12] > 3000:
    newP[12] = 3000
#Filter 3 Bandwidth
  newP[13] += random.randrange(-10, 10) * learnRate
  if newP[13] < 100:
    newP[13] = 100
  elif newP[13] > 3000:
    newP[13] = 3000
#Filter 4 Bandwidth
  newP[14] += random.randrange(-10, 10) * learnRate
  if newP[14] < 100:
    newP[14] = 100
  elif newP[14] > 3000:
    newP[14] = 3000
#Filter 5 Bandwidth
  newP[15] += random.randrange(-10, 10) * learnRate
  if newP[15] < 100:
    newP[15] = 100
  elif newP[15] > 3000:
    newP[15] = 3000
#Del1 Ratio
  newP[16] += random.uniform(0.01, 0.01) * learnRate
  if newP[16] > 1.5:
    newP[16] = 1.5
#Del2 Ratio
  newP[17] += random.uniform(0.01, 0.01) * learnRate
  if newP[17] > 2.5:
    newP[17] = 2.
#Del3 Ratio
  newP[18] += random.uniform(0.01, 0.01) * learnRate
  if newP[18] > 3.5:
    newP[18] = 3.5
#Del4 Ratio
  newP[19] += random.uniform(0.01, 0.01) * learnRate
  if newP[19] > 4.5:
    newP[19] = 4.5
#Del1 Gain
  newP[20] += random.uniform(0.001, 0.001) * learnRate
  if newP[20] > 1:
    newP[20] = 1
  elif newP[20] < 0:
    newP[20] = 0
#Del2 Gain
  newP[21] += random.uniform(0.001, 0.001) * learnRate
  if newP[21] > 1:
    newP[21] = 1
  elif newP[21] < 0:
    newP[21] = 0
#Del3 Gain
  newP[22] += random.uniform(0.001, 0.001) * learnRate
  if newP[22] > 1:
    newP[22] = 1
  elif newP[22] < 0:
    newP[22] = 0
#Del4 Gain
  newP[23] += random.uniform(0.001, 0.001) * learnRate
  if newP[23] > 1:
    newP[23] = 1
  elif newP[23] < 0:
    newP[23] = 0
#Del5 Gain
  newP[24] += random.uniform(0.001, 0.001) * learnRate
  if newP[24] > 1:
    newP[24] = 1
  elif newP[24] < 0:
    newP[24] = 0
#Toggle filter 2
  if random.randint(0, 100) > 90:
    if newP[25] == 0:
      newP[25] = 1
    else:
      newP[25] = 0
#Filter 1 Hz
  newP[26] += random.randrange(-10, 10) * learnRate
  if newP[26] < 0:
    newP[26] = 0
  elif newP[26] > 10000:
    newP[26] = 10000
  return newP

#Initialisation
p = initModel()
csd = setParams(p)
#Get training data
dataDir = os.path.join(os.getcwd(), 'SoundFiles', 'Idiophones')
wavFname = os.path.join(dataDir, 'cowbell.wav')
trainData, sr = librosa.load(wavFname, sr=44100)
trainLen = trainData.shape[0]
trainSpecs = librosa.feature.melspectrogram(y=trainData, sr=sr, hop_length=512)

#Machine Learning Loop
epochs = 100
learningRate = 100

prevDist = 100000
losses = []
newP = p
cs = ctcsound.Csound()  

for x in range(epochs):
  #CODE TO RENDER CSOUND FILE
  print(x)
  csd = setParams(newP)
  ret = cs.compileCsdText(csd)
  cs.createMessageBuffer(toStdOut=False)
  test = []
  if ret == ctcsound.CSOUND_SUCCESS:
      cs.start()
      cs.perform()
      cs.reset()
  #Get current Estimate
  currInst, sr = librosa.load('Render.wav', sr=44100)
  currInstTrim = currInst[0:trainLen]

  #Calculate Mfccs
  learnSpecs = librosa.feature.melspectrogram(y=currInstTrim, sr=sr, hop_length=512)

  #Calculate Euclidian distance (loss)
  dist = np.linalg.norm(trainSpecs - learnSpecs)

  #Adjust Parameters randomly
  print(dist, " ~ ", prevDist)
  if dist < prevDist:
    pLoss = dist
    print("saved Dist")
    p = copy.deepcopy(newP)
    prevDist = dist

  newP = adjustParams(p, learningRate)
  losses.append(pLoss)
  learningRate *= 0.99
  print(learningRate)

plt.plot(losses)
plt.show()
print(p)
csd = setParams(p)
cs = ctcsound.Csound()  
display.specshow(trainSpecs)
plt.show()
display.specshow(learnSpecs)
plt.show()
cs.createMessageBuffer(toStdOut=False)
ret = cs.compileCsdText(csd)
test = []
if ret == ctcsound.CSOUND_SUCCESS:
    cs.start()
    cs.perform()