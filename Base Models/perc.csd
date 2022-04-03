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


          outs      a1, a1
          endin
</CsInstruments>

<CsScore>
; 1 2 3   4    5   6 7 8 9   10   11    121314  151617
i 1 0 20 440 0.05 0.1 0 0 -0.5, 5000, 0.99
e
</CsScore>
</CsoundSynthesizer>    