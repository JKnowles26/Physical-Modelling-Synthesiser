<Cabbage> bounds(0, 0, 0, 0)
form caption("main") size(400, 300), guiMode("queue"), pluginId("def1")
keyboard bounds(8, 166, 381, 95)
rslider bounds(36, 90, 60, 60) channel("filterSlider") range(0, 10000, 1500, 1, 100) text("String Resonance") popupText("String Resonance")

signaldisplay bounds(122, 24, 254, 93) channel("master") colour(255, 255, 255, 255) displayType("waveform") colour:0(255, 255, 255, 255), signalVariable("gaSig")
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
    
    alwayson 2
    ;instrument will be triggered by keyboard widget
    
    instr 1
    ifreq=1/p4
    kenv madsr 0.0000001, ifreq, 0, 1
    asig noise p5, -.9
    asig = asig * kenv
    afreq = 1/p4
    kfreq = afreq
    printk 1, kfreq
    aBuffOut delayr 1
    atap deltapi afreq
    kCutoff chnget "filterSlider"
    aFiltered tone atap, kCutoff
    gaSig = aFiltered* 2
    delayw asig + aFiltered * 0.997
    
    outs aFiltered, aFiltered
    endin
    
    instr 2 
    display gaSig, .001, 300
    endin
    </CsInstruments>
<CsScore>
;causes Csound to run for about 7000 years...
f0 z
</CsScore>
</CsoundSynthesizer>