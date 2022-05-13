<Cabbage> bounds(0, 0, 0, 0)
form caption("main") size(400, 300), guiMode("queue"), pluginId("def1")
keyboard bounds(8, 166, 381, 95)
rslider bounds(34, 92, 70, 60) channel("cutoff1") range(0, 10000, 1000, 1, 100) text("Exciter Cutoff") popupText("Exciter Cutoff") textColour(0, 0, 0, 255)

signaldisplay bounds(22, 8, 254, 57) channel("master") colour(255, 255, 255, 255) displayType("waveform") colour:0(255, 255, 255, 255), signalVariable("gaSig")
rslider bounds(108, 94, 60, 60) channel("cutoff2") range(100, 10000, 2300, 1, 100) text("Loop Cutoff") popupText("Loop Cutoff") textColour(0, 0, 0, 255)
rslider bounds(180, 92, 60, 60) channel("feedback1") range(-3, 3, 1.23, 1, 0.01) text("Feedback") popupText("feedback") textColour(0, 0, 0, 255)
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-n -d -+rtmidi=NULL -M0 -m0d --midi-key-cps=4 --midi-velocity-amp=5 --displays
</CsOptions>
    <CsInstruments>
    ; Initialize the global variables. 
    ksmps = 1000
    nchnls = 2
    0dbfs = 1
    
    gaSig init 0
    
                opcode      delayMod, aa, aai
    aSigA, aSigB, ifreq xin
    afreq   =               1/ifreq
    kCutoff     chnget      "filterSlider"
    aBuffOut    delayr      1
    atap        deltapi     afreq
    aFiltered   tone        atap, kCutoff
    gaSig       =           aFiltered* 2
                delayw      aSigA + aSigB + aFiltered * 0.995
                xout        aFiltered, aFiltered
    endop
    
    alwayson 2
    ;instrument will be triggered by keyboard widget
    instr 1
    asig        noise       0.1, -0.9
    kenv        madsr       0.65, 0.1, 0, 0
    kCutoff1    chnget      "cutoff1"
    asig        tone        asig, kCutoff1
    aBuffOut    delayr      1
    afreq       =           1 / p4
    atap        deltapi     afreq
    kCutoff2    chnget      "cutoff2"
    afiltered   tone        atap, kCutoff2
    kFeedback   chnget      "feedback1"
                printk      1, kFeedback 
                delayw asig + tanh(afiltered * kFeedback)
    gaSig       =           afiltered
                out         afiltered
    endin
    
    instr 2 
                display     gaSig, .001, 300
    endin
    </CsInstruments>
<CsScore>
;causes Csound to run for about 7000 years...
f0 z
</CsScore>
</CsoundSynthesizer>