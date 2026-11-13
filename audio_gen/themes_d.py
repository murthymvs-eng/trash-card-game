"""Music tracks part 4: princess, taylor, mario, classic."""
from dsp import *

def princess(B):
    u = 0.5
    arps = {"C": [60, 64, 67, 72, 76, 79], "F": [57, 60, 64, 69, 72, 77],
            "C7": [55, 59, 62, 67, 71, 74], "Am": [57, 60, 64, 69, 72, 76]}
    chords = ["C", "F", "C7", "Am"] * 3
    basses = {"C": [48, 43, 52], "F": [41, 43, 45], "C7": [43, 48, 50],
              "Am": [45, 43, 52]}
    for bar, ch in enumerate(chords):
        for i, m in enumerate(arps[ch]):
            B.add(bell(midi_f(m), u * 0.55, amp=.6), (bar*3 + i * 0.5) * u, .2, .52)
        for i, m in enumerate(basses[ch]):
            B.add(tuba(midi_f(m), u * 1.1), (bar*3 + i) * u, .28, .45)
    def mel(b, m, beats, g=.4, p=.5):
        B.add(brass(midi_f(m), beats * u + .1, a=.06, r=.2, vib_depth=.002),
              b * u, g, p)
    mel(0, 76, 2); mel(2, 79, 1); mel(3, 77, 1); mel(4, 76, 2)
    mel(6, 74, 1.5); mel(7.5, 72, 1.5); mel(9, 74, 1); mel(10, 72, 2)
    mel(12, 79, 2); mel(14, 77, 1); mel(15, 76, 1); mel(16, 74, 1)
    mel(17, 76, 2); mel(18, 72, 1); mel(19, 74, 1); mel(20, 76, 1)
    mel(21, 77, 1); mel(22, 76, 3)
    mel(24, 79, 2); mel(26, 77, 1); mel(27, 76, 1); mel(28, 74, 1)
    mel(29, 76, 2); mel(30, 72, 1); mel(31, 74, 1); mel(32, 76, 1)
    mel(33, 77, 1); mel(34, 76, 3, g=.44)
    for b, m in ((.5, 87), (10.5, 91), (22.5, 87)):
        B.add(bell(midi_f(m), 1.2, amp=.7), b * u, .16, .62)
    B.add(pad_chord([midi_f(m) for m in (60, 64, 67, 72)], 2.2, a=.3),
          35.4 * u, .28, .5)

def taylor(B):
    u = 0.5
    pads = [(57, 61, 64), (59, 62, 65), (55, 59, 62), (57, 60, 64)] * 2
    for bar, ms in enumerate(pads):
        B.add(pad_chord([midi_f(m) for m in ms], 2.0, a=.3), bar*4 * u, .24, .5)
    arps = [[74, 78, 81, 86, 81, 78, 74, 78], [76, 80, 83, 88, 83, 80, 76, 80],
            [74, 78, 81, 86, 89, 86, 81, 78], [76, 80, 83, 86, 84, 80, 76, 80]] * 2
    for bar, notes in enumerate(arps):
        for i, m in enumerate(notes):
            B.add(square(midi_f(m), u * 0.45, amp=.5, r=.02),
                  (bar*4 + i * 0.5) * u, .14, .5)
    def mel(b, m, beats, g=.42, p=.5):
        B.add(brass(midi_f(m), beats * u + .08, a=.05, r=.12, vib_depth=.003),
              b * u, g, p)
    mel(0, 77, 1); mel(1, 81, 1); mel(2, 85, 1); mel(3, 84, 1)
    mel(4, 74, 1); mel(5, 77, 1); mel(6, 78, 1); mel(7, 81, 3)
    mel(8, 81, 1); mel(9, 85, 1); mel(10, 89, 1); mel(11, 87, 1)
    mel(12, 81, .5); mel(12.5, 85, .5); mel(13, 89, .5); mel(13.5, 92, .5)
    mel(14, 92, 3, g=.48)
    for bar in range(8):
        B.add(kick(), bar*4 * u, .4); B.add(kick(), (bar*4 + 2) * u, .4)
        B.add(clap(), (bar*4 + 1) * u, .25); B.add(clap(), (bar*4 + 3) * u, .25)
        for i in range(8):
            B.add(hat(), (bar*4 + i * 0.5 + 0.25) * u, .09)
    B.add(kick(), 31.75 * u, .4)
    B.add(noise(9.0, f0=900, q=.6, tilt=-3, dk=.35, a=1.2, seed=13), 4 * u, .16, .5)
    for tt_, f in ((13.4, 700), (13.7, 900)):
        B.add(noise(0.12, f0=f, q=1.2, dk=25, a=.005, seed=int(f)),
              tt_ * u, .18, .5)
    B.add(shimmer(1.2, amp=.14, seed=7), 14 * u, .8, .55)

def mario(B):
    u = 0.3
    pat0 = [(0, 72, .5), (.5, 74, .5), (1, 76, .5), (1.5, 79, .5), (2, 76, .5),
            (2.5, 74, .5), (3, 72, 1)]
    pat1 = [(4, 72, .5), (4.5, 74, .5), (5, 76, .5), (5.5, 79, .5), (6, 81, .5),
            (6.5, 79, .5), (7, 76, 1)]
    pat2 = [(8, 77, .5), (8.5, 79, .5), (9, 81, .5), (9.5, 84, .5), (10, 81, .5),
            (10.5, 79, .5), (11, 77, 1)]
    pat3 = [(12, 76, .5), (12.5, 77, .5), (13, 79, .5), (13.5, 76, .5), (14, 72, 2)]
    pats = [pat0, pat1, pat2, pat3]
    for half in range(2):
        off = half * 16 * u
        for p in range(4):
            shift = 12 if (half == 1 and p >= 2) else 0
            for b, m, d in pats[p]:
                B.add(square(midi_f(m + shift), d * u + .05, amp=.5, r=.03),
                      off + b * u, .3, .5)
    for half in range(2):
        off = half * 16
        for bar in range(4):
            for i, m in enumerate([36, 43, 45, 48]):
                B.add(tri(midi_f(m), u * 0.9, amp=.6), (off + bar*4 + i) * u, .3, .45)
    for bar in range(16):
        B.add(kick(), bar*4 * u, .3); B.add(kick(), (bar*4 + 2) * u, .3)
        B.add(snare(), (bar*4 + 1) * u, .14); B.add(snare(), (bar*4 + 3) * u, .14)
        for i in range(4):
            B.add(hat(), (bar*4 + i * 2 + 1) * u * 0.5, .07)

def classic(B):
    u = 0.5
    rows = [
        [72, 76, 79, 84, 81, 79, 76, 74],
        [72, 76, 79, 84, 87, 87, 86, 86],
        [74, 78, 81, 86, 84, 82, 81, 79],
        [76, 74, 72, 74, 71, 71, 72, 72],
        [77, 81, 84, 89, 87, 84, 82, 79],
        [80, 84, 87, 89, 91, 91, 89, 89],
        [81, 85, 88, 93, 92, 91, 89, 88],
        [84, 84, 84, 84, 72, 72, 67, 67],
    ]
    for bar, notes in enumerate(rows):
        for i, m in enumerate(notes):
            B.add(bell(midi_f(m), u * 0.6, amp=.7), (bar*4 + i * 0.5) * u, .3, .5)
    B.add(pad_chord([midi_f(m) for m in (60, 64, 67, 72)], 2.2, a=.3),
          31 * u, .3, .5)
    for bar in range(8):
        B.add(kick(), bar*4 * u, .25); B.add(kick(), (bar*4 + 2) * u, .25)
        B.add(brush(), (bar*4 + 1) * u, .18); B.add(brush(), (bar*4 + 3) * u, .18)
        for i in range(8):
            B.add(hat(), (bar*4 + i * 0.5 + 0.25) * u, .07)

TRACKS = {
    "princess": dict(fn=princess, dur=20.5, seed=91),
    "taylor": dict(fn=taylor, dur=18.5, seed=101),
    "mario": dict(fn=mario, dur=21.5, seed=111),
    "classic": dict(fn=classic, dur=18.5, seed=121),
}
