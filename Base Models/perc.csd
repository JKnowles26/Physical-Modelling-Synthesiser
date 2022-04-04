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

afdbk      =         ifdbk * (d1 + d2 + d3 + d4)

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
i 1 0 5 440 0.1 0.1 0 0 0 -0.5 5000 5 1 1 2000 2000 200 2000 200 2000 200 2000 200 0.1 0.25 0.5 0.25 0.25 0.25 0.25 1 5000
e
</CsScore>
</CsoundSynthesizer>    