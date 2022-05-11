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
ib1bw     =         p16
ib2bw     =         p17
ib3bw     =         p18
ib4bw     =         p19
idel1     =         p20
idel2     =         p21
idel3     =         p22
igain1    =         p23
igain2    =         p24
igain3    =         p25
igain4    =         p26
if2Tog    =         p27
if2Hz     =         p28

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

afdbk      =         ifdbk * (ad1 + ad2+ ad3+ad4)

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
; 1 2 3 4   5 6   7 8 9 10   11    12    131415   16  17   18   19   20   21   22   23   24  25   26  272829303132
i 1 0 5 440 1 0.0001 0 0.4 0 -0.5 10000 0.55 1 0 2000 1000 1000 1000 1000 2.1 4.20 8.1 1 1 1 1 0 5000
e
</CsScore>
</CsoundSynthesizer>    
