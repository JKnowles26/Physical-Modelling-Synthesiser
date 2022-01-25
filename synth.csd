<Cabbage>
    form caption("main") size(400, 300), guiMode("queue"), pluginId("def1")
    keyboard bounds(8, 166, 381, 95)
rslider bounds(40, 90, 60, 60) channel("filterSlider") range(0, 3000, 1500, 1, 100) text("String Resonance") popupText("String Resonance")
signaldisplay bounds(122, 16, 260, 100) channel("sigDisplay")
</Cabbage>
<CsoundSynthesizer>
    <CsOptions>
        -n -d -+rtmidi=NULL -M0 -m0d --midi-key-cps=4 --midi-velocity-amp=5
    </CsOptions>
    <CsInstruments>
        ; Initialize the global variables. 
        ksmps = 1000
        nchnls = 2
        0dbfs = 1
        
        gasig init 0
        gafreq init 1/200
        gifreq init 1/200
        
        alwayson 2
        ;instrument will be triggered by keyboard widget
        instr 1
        gifreq=1/p4
        kenv madsr 0.01, gifreq, 0, 0
        asig noise p5, -.5 
        gafreq = 1/p4
        vincr gasig, (asig * kenv)	
        endin
        
        instr 2
        aBuffOut delayr 1
        atap deltapi gafreq
        kCutoff chnget "filterSlider"
        aFiltered tone atap, kCutoff
        delayw gasig + aFiltered
        outs aFiltered + gasig, aFiltered + gasig
        clear gasig
        endin
    </CsInstruments>
    <CsScore>
    ;causes Csound to run for about 7000 years...
    f0 z
    </CsScore>
</CsoundSynthesizer>