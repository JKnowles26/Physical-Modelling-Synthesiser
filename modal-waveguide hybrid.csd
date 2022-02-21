<Cabbage>
form caption("Modal-Waveguide Synthesiser") size(600, 500), guiMode("queue"), pluginId("def1")
keyboard bounds(8, 158, 381, 95)
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-n -d -+rtmidi=NULL -M0 -m0d --midi-key-cps=4 --midi-velocity-amp=5
</CsOptions>
<CsInstruments>
; Initialize the global variables. 
ksmps = 32
nchnls = 2
0dbfs = 1

gaExc init 0
gaOut init 0
;opcodes

;exciter 
opcode excite, a, iiiiii
iVel, iFilt, iAtt, iDec, iSus, iRel xin
aNoise noise iVel, iFilt
kEnv adsr iAtt, iDec, iSus, iRel
aOut = aNoise * kEnv
xout aOut
endop

;waveguide
opcode waveguide, a, ai
aIn, iFreq xin
if iFreq >= 0 then
    iFreq = 1
endif
aBuffout delayr 1
afreq = 1 / iFreq
atap deltapi afreq
delayw aIn
xout atap
endop

;scattering junction
opcode scatterjunc, a, a
endop

;filter
opcode filter, a, a
endop

alwayson 2
;instrument will be triggered by keyboard widget
instr 1
gaExc excite p5, -0.9, 0.65, 1, 0, 5

outs gaOut, gaOut
endin

instr 2
aSigA = gaExc
aSigB waveguide aSigA, p4
aSigA waveguide aSigB, p4
gaOut = aSigB
endin
</CsInstruments>
<CsScore>
;causes Csound to run for about 7000 years...
f0 z
</CsScore>
</CsoundSynthesizer>
