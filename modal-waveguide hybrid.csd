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

gaSig init 0
gkFreq init 0
;opcodes

;exciter 
opcode excite, a, iiiiii
iVel, iFilt, iAtt, iDec, iSus, iRel xin
aNoise noise iVel, iFilt
kEnv madsr iAtt, iDec, iSus, iRel
aOut = aNoise * kEnv
xout aOut
endop

;waveguide
opcode waveguide, a, ak
aIn, kFreq xin

if kFreq <= 0 then
    kFreq = 1
endif
kFreq = 1 / kFreq
aBuffout delayr 1
aSig deltapi kFreq
delayw aIn

xout aSig
endop

;scattering junction
opcode scatterjunc, a, a
endop

;filter
opcode filter, a, a
endop

alwayson 2

instr 1
//Excite inputs: Vel, Filt, Att, Dec, Sus, Rel
aSig excite p5, -0.5, 0.1, 0.1, 1, 0.01
gkFreq = p4
gaSig = aSig
endin

instr 2

aSig init 0
aSig = gaSig + aSig
aSig1 waveguide aSig, gkFreq 
aSig1 = aSig1* 0.98
aSig waveguide aSig1, gkFreq
out aSig1
gaSig = 0
endin

</CsInstruments>
<CsScore>
;causes Csound to run for about 7000 years...
f0 z
</CsScore>
</CsoundSynthesizer>
