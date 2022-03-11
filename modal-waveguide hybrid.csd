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
giFeedback = 0.99
giScatterRate = 0.1
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
opcode scatterjunc, aa, aai
aIn1, aIn2, iScatterRate xin
aSig1 = (aIn1 * (1 - iScatterRate)) + (aIn2 * iScatterRate)
aSig2 = (aIn2 * (1 - iScatterRate)) + (aIn1 * iScatterRate)
aSig1 tone aSig1,5000
aSig2 tone aSig2, 5000
xout aSig1, aSig2

endop

alwayson 2

instr 1
//Excite inputs: Vel, Filt, Att, Dec, Sus, Rel
aSig excite p5, 0.9, 0.1, 0.1, 1, 0.01
gkFreq = p4
gaSig = aSig
endin

instr 2

aSig init 0
aSig5 init 0
aSig4 init 0

aSig = gaSig + aSig
aSig1 waveguide aSig, gkFreq
aSig1, aSig5 scatterjunc aSig1, aSig5, giScatterRate
aSig2 waveguide aSig1, gkFreq
aSig2, aSig4 scatterjunc aSig2, aSig4, giScatterRate
aSig3 waveguide aSig2, gkFreq
aSig4 waveguide aSig3, gkFreq
aSig5 waveguide aSig4, gkFreq
aSig waveguide aSig5, gkFreq
aSig = aSig * giFeedback
outs aSig3, aSig3
gaSig = 0
endin

</CsInstruments>
<CsScore>
;causes Csound to run for about 7000 years...
f0 z
</CsScore>
</CsoundSynthesizer>
