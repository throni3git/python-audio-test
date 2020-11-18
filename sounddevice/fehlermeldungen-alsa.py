Auf T495 Fedora 32

Framerate: 48000
    0 HD-Audio Generic: HDMI 0 (hw: 0, 3), ALSA (0 in, 8 out)
    1 HD-Audio Generic: HDMI 1 (hw: 0, 7), ALSA (0 in, 8 out)
    2 HD-Audio Generic: HDMI 2 (hw: 0, 8), ALSA (0 in, 8 out)
    3 HD-Audio Generic: ALC257 Analog (hw: 1, 0), ALSA (2 in, 2 out)
* 4 Scarlett Solo USB: Audio (hw: 2, 0), ALSA (2 in, 2 out)
    5 hdmi, ALSA (0 in, 8 out)
    6 pulse, ALSA (32 in, 32 out)
    7 default, ALSA (32 in, 32 out)
ALSA lib pcm.c: 8545: (snd_pcm_recover) underrun occurred
output underflow
output underflow
output underflow
output underflow
ALSA lib pcm.c: 8545: (snd_pcm_recover) underrun occurred
output underflow
output underflow
output underflow
output underflow
ALSA lib pcm.c: 8545: (snd_pcm_recover) underrun occurred
Expression 'err' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 3350
Expression 'ContinuePoll( self, StreamDirection_In, &pollTimeout, &pollCapture )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 3876
Expression 'PaAlsaStream_WaitForFrames( stream, &framesAvail, &xrun )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 4248
python: src/hostapi/alsa/pa_linux_alsa.c: 3382: OnExit: Assertion `data' failed.
Abgebrochen(Speicherabzug geschrieben)


Framerate: 48000
    0 HD-Audio Generic: HDMI 0 (hw: 0, 3), ALSA (0 in , 8 out)
    1 HD-Audio Generic: HDMI 1 (hw: 0, 7), ALSA (0 in , 8 out)
    2 HD-Audio Generic: HDMI 2 (hw: 0, 8), ALSA (0 in , 2 out)
    3 HD-Audio Generic: ALC257 Analog (hw: 1, 0), ALSA (2 in , 2 out)
    4 hdmi, ALSA (0 in , 8 out)
    5 pulse, ALSA (32 in , 32 out)
* 6 default, ALSA (32 in , 32 out)
ALSA lib pcm.c: 8545: (snd_pcm_recover) underrun occurred
Expression 'err' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 3350
Expression 'ContinuePoll( self, StreamDirection_In, &pollTimeout, &pollCapture )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 3876
Expression 'PaAlsaStream_WaitForFrames( stream, &framesAvail, &xrun )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 4248
python: src/hostapi/alsa/pa_linux_alsa.c: 3382: OnExit: Assertion `data' failed.
Abgebrochen(Speicherabzug geschrieben)
