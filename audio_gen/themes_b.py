"""Music tracks part 2: avengers, spiderman."""
from dsp import *

def avengers(B):
    u = 0.5
    def mel(b, m, beats, g=.5, p=.5):
        B.add(brass(midi_f(m), beats * u + 0.07, r=.1), b * u, g, p)
    for b, m in ((0, 65), (.5, 65), (1, 65), (1.5, 69)):
        mel(b, m, .5)
    mel(2, 72, 2)
    for b, m in ((4, 70), (4.5, 69), (5, 70), (5.5, 72)):
        mel(b, m, .5)
    mel(6, 70, 1); mel(7, 67, 1)
    for b, m in ((8, 65), (8.5, 65), (9, 67), (9.5, 69), (10, 72),
                 (10.5, 70), (11, 69), (11.5, 67)):
        mel(b, m, .5)
    mel(12, 65, 1); mel(13, 72, 3)
    for m, dt in ((41, 0), (49, .02), (57, .04)):
        B.add(brass(midi_f(m), 4 * u, a=.08, r=.5), 16 * u + dt, .26, .5)
    for b, m in ((20, 77), (20.5, 77), (21, 77), (21.5, 81)):
        mel(b, m, .5)
    mel(22, 84, 2)
    for b, m in ((24, 82), (24.5, 81), (25, 82), (25.5, 84)):
        mel(b, m, .5)
    mel(26, 82, 1); mel(27, 79, 1)
    for b, m in ((28, 77), (28.5, 77), (29, 79), (29.5, 81), (30, 84),
                 (30.5, 82), (31, 81), (31.5, 79)):
        mel(b, m, .5)
    mel(32, 77, 1); mel(33, 84, 3, g=.55)
    bass = [[41, 48, 41, 48], [41, 48, 41, 48], [41, 44, 43, 45], [41, 41, 48, 41],
            [41, 44, 43, 45], [41, 41, 48, 41], [41, 44, 43, 45], [41, 48, 41, 48],
            [41, 41, 41, 41]]
    for bar, notes in enumerate(bass):
        for i, m in enumerate(notes):
            B.add(tuba(midi_f(m), u * 0.9), (bar*4 + i) * u, .34, .5)
    for b in range(0, 36, 2):
        B.add(kick(), b * u, .38)
    for bar in range(9):
        for b in (1, 3):
            B.add(snare(), (bar*4 + b) * u, .3)
    B.add(timpani(midi_f(41), 1.2), 0, .5)
    B.add(timpani(midi_f(41), 1.4), 32 * u, .7)
    B.add(noise(0.9, low=300, dk=3, a=.1, seed=5), 33 * u, .4)
    for m, dt in ((49, 0), (57, .02), (60, .04)):
        B.add(brass(midi_f(m), 1.6, a=.07, r=.5), 33.4 * u + dt, .3, .5)

def spiderman(B):
    # "Spider-Man 1967 Cartoon Theme Song" — transcribed from the reference
    # recording (basic-pitch: midi/spiderman/track_basic_pitch.csv). The 60s
    # synth-cartoon lead, rendered as vibrato brass over tuba bass.
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    songFromCSV(B, os.path.join(here, 'midi', 'spiderman', 'track_basic_pitch.csv'),
                bass=tuba, mel=brass, shimmer=bell)

TRACKS = {
    "avengers": dict(fn=avengers, dur=19.5, seed=51),
    "spiderman": dict(fn=spiderman, dur=62.0, seed=61),
}
