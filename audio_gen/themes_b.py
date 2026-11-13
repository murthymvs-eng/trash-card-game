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
    u = 0.33
    def sax(b, m, beats, g=.42, p=.5):
        B.add(brass(midi_f(m), beats * u + .09, a=.04, r=.1, vib_depth=.008,
                    vib_rate=6), b * u, g, p)
    sax(0, 55, 2)
    for b, m in ((4, 70), (4.5, 67), (5, 70), (5.5, 73), (6, 70),
                 (6.5, 72), (7, 70), (7.5, 67)):
        sax(b, m, .5)
    sax(8, 65, 1); sax(9, 67, 1)
    for b, m in ((10, 70), (10.5, 69), (11, 67), (11.5, 65)):
        sax(b, m, .5)
    sax(12, 67, 1); sax(13, 70, 1); sax(14, 73, 1); sax(15, 70, 1)
    for b, m in ((16, 72), (16.5, 70), (17, 72), (17.5, 69)):
        sax(b, m, .5)
    sax(18, 67, 2)
    for b, m in ((20, 70), (20.5, 72), (21, 70), (21.5, 69), (22, 67),
                 (22.5, 69), (23, 70), (23.5, 72)):
        sax(b, m, .5)
    sax(24, 72, 1); sax(25, 70, 1); sax(26, 69, 1); sax(27, 67, 1)
    for b, m in ((28, 70), (28.5, 69)):
        sax(b, m, .5)
    sax(29, 67, 1); sax(30, 65, 1); sax(31, 67, 1)
    sax(32, 55, 2)
    for b, m in ((36, 70), (36.5, 67), (37, 70), (37.5, 73), (38, 72),
                 (38.5, 73), (39, 72), (39.5, 70)):
        sax(b, m, .5)
    sax(40, 65, 1); sax(41, 67, 1)
    for b, m in ((42, 70), (42.5, 73), (43, 72), (43.5, 70)):
        sax(b, m, .5)
    sax(44, 70, 1); sax(45, 73, 1); sax(46, 72, 1); sax(47, 70, 1)
    for b, m in ((48, 72), (48.5, 74), (49, 72), (49.5, 74)):
        sax(b, m, .5)
    sax(50, 76, 2)
    for b, m in ((52, 74), (52.5, 72), (53, 70), (53.5, 72), (54, 74),
                 (54.5, 76), (55, 74), (55.5, 72)):
        sax(b, m, .5)
    sax(56, 71, 1); sax(57, 69, 1); sax(58, 70, 1); sax(59, 69, 1)
    for b, m in ((60, 69), (60.5, 67)):
        sax(b, m, .5)
    sax(61, 65, 2, g=.46)
    wb = [43, 45, 46, 48, 50, 43, 45, 46, 48, 41, 43, 45, 46, 48, 45, 43]
    for bar, m in enumerate(wb):
        B.add(pizz(midi_f(m), u * 1.3, pick=.3), bar * 4 * u, .3, .42)
        B.add(pizz(midi_f(m + 12 if m < 48 else m), u * 0.7, pick=.2),
              (bar*4 + 2) * u, .18, .58)
    stabs = {0: (55, 58, 62, 65), 2: (53, 56, 60, 63), 4: (46, 50, 55, 58),
             8: (55, 58, 62, 65), 10: (53, 56, 60, 63), 12: (46, 50, 55, 58),
             14: (55, 58, 62, 65)}
    for bar, ms in stabs.items():
        for b in (0, 2.5):
            for m in ms:
                B.add(pluck(midi_f(m), u * 1.2, pick=.1), (bar*4 + b) * u, .14, .5)
    for bar in range(16):
        B.add(kick(), bar*4 * u, .3); B.add(kick(), (bar*4 + 2) * u, .3)
        B.add(brush(), (bar*4 + 1) * u, .25); B.add(brush(), (bar*4 + 3) * u, .25)
        for i in range(4):
            B.add(hat(), (bar*4 + i*2 + 0.9) * u * 0.5, .08)
            B.add(hat(), (bar*4 + i*2 + 1.55) * u * 0.5, .06)

TRACKS = {
    "avengers": dict(fn=avengers, dur=19.5, seed=51),
    "spiderman": dict(fn=spiderman, dur=22.5, seed=61),
}
