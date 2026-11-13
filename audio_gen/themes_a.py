"""Music tracks part 1: starwars, hp, minion, coco."""
from dsp import *

def starwars(B):
    u = 60 / 88.0
    def mel(b, m, beats, g=0.5, p=0.5):
        B.add(brass(midi_f(m), beats * u + 0.08, r=0.1), b * u, g, p)
    for b in (0, 1, 2):
        mel(b, 62, 1)
    mel(3, 62, 2)
    for b, m in ((4, 73), (4.5, 74), (5, 70), (6, 69), (6.5, 67), (7, 70), (8, 69),
                 (8.5, 67), (9, 66), (9.5, 69), (10, 67), (10.5, 66), (11, 64),
                 (11.5, 67), (12, 66), (12.5, 64)):
        mel(b, m, 0.5)
    for b in (13, 14, 15):
        mel(b, 62, 1)
    mel(16, 62, 2)
    for b, m in ((18, 69), (18.5, 76), (19, 74), (19.5, 76), (20, 74),
                 (20.5, 73), (21, 70), (21.5, 69)):
        mel(b, m, 0.5)
    mel(22, 74, 1); mel(23, 73, .5); mel(23.5, 70, .5); mel(24, 74, 4, g=.55)
    for m, dt in ((38, 0), (53, .02), (57, .04)):
        B.add(brass(midi_f(m), 2.5, r=.3, a=.08), 24*u + dt, .22, .5)
    pat = [[38, 34, 38, 38]] * 4 + [[33, 28, 33, 28]] * 3 + [[38, 38, 38, 38]]
    for bar, notes in enumerate(pat):
        for i, m in enumerate(notes):
            B.add(tuba(midi_f(m), u * 0.48), (bar*4 + i) * u * 0.99, .3, .5)
    for b in range(0, 27, 2):
        B.add(kick(), b * u, .35)
    for bar in range(7):
        for b in (1, 3):
            B.add(snare(), (bar*4 + b) * u, .28)
    B.add(timpani(midi_f(38), 1.2), 0, .4)
    B.add(timpani(midi_f(38), 1.4), 24 * u, .6)

def hp(B):
    u = 0.48
    for bar in range(12):
        g = .5 if bar < 4 else .22
        for i, m in enumerate((50, 55, 58)):
            B.add(pizz(midi_f(m), u * 1.4, pick=.8 if i == 0 else .3),
                  (bar*3 + i) * u, g, .45)
    def mel(b, m, beats, g=.42, p=.5):
        B.add(brass(midi_f(m), beats * u + 0.1, a=.05, r=.15, vib_depth=.003),
              b * u, g, p)
    mel(12, 70, 1.5); mel(13.5, 69, 1); mel(14.5, 67, 1); mel(15, 67, 1)
    mel(16, 65, 1); mel(17, 67, 1); mel(18, 70, 1); mel(19, 69, 1)
    mel(20, 67, 1); mel(21, 60, 3, .4); mel(24, 72, 1.5); mel(25.5, 70, 1)
    mel(26.5, 72, 1); mel(27, 71, 1); mel(28, 69, 1); mel(29, 70, 1)
    mel(30, 68, 1); mel(31, 69, 1); mel(32, 70, 1); mel(33, 72, 3, .42)
    for bar in range(12):
        notes = (43, 48, 50) if bar < 11 else (43, 43, 43)
        for i, m in enumerate(notes):
            B.add(tuba(midi_f(m), u * 1.1), (bar*3 + i) * u, .32, .5)
    for m, dt in ((43, 0), (58, .02), (62, .04)):
        B.add(brass(midi_f(m), 1.4, a=.06, r=.4), 33.5*u + dt, .3, .5)

def minion(B):
    u = 0.42
    bass = [[36, 43, 36, 36], [41, 41, 36, 43], [36, 43, 36, 36], [36, 36, 43, 43],
            [36, 43, 36, 36], [41, 36, 43, 36], [36, 36, 43, 36], [36, 43, 36, 45]]
    for bar, notes in enumerate(bass):
        for i, m in enumerate(notes):
            B.add(tuba(midi_f(m), u * 0.9), (bar*4 + i) * u, .38, .5)
    xy = [[72, 76, 79, 76, 72, 76, 79, 76], [74, 77, 81, 77, 74, 77, 81, 77],
          [72, 76, 79, 76, 72, 74, 76, 79], [77, 76, 74, 72, 72, 72, 72, 72],
          [72, 76, 79, 76, 72, 76, 79, 76], [74, 77, 81, 77, 74, 77, 81, 77],
          [72, 76, 79, 76, 74, 72, 69, 67], [84, 83, 81, 79, 77, 76, 74, 72]]
    for bar, notes in enumerate(xy):
        for i, m in enumerate(notes):
            B.add(xylo(midi_f(m), u * 0.5), (bar*4 + i * 0.5) * u, .34, .5)
    B.add(osc(150, .7, harm=((1, 1), (2, .4)), dk=4, sweep=1.6, a=.01, r=.2),
          30.5 * u, .3)
    for bar in range(8):
        B.add(kick(), bar*4 * u, .4); B.add(kick(), (bar*4 + 2) * u, .4)
        B.add(clap(), (bar*4 + 1) * u, .22); B.add(clap(), (bar*4 + 3) * u, .22)
        for i in range(8):
            B.add(hat(), (bar*4 + i * 0.5 + 0.25) * u, .1)

def coco(B):
    u = 0.6
    bassm = [36, 36, 41, 43, 36, 36, 38, 41, 36, 36, 41, 43]
    arps = {"Cm": [55, 60, 64, 67, 70, 75],
            "F": [53, 56, 60, 65, 69, 72],
            "G": [55, 58, 60, 62, 65, 67]}
    chords = ["Cm", "Cm", "F", "G"] * 3
    for bar, (bm, ch) in enumerate(zip(bassm, chords)):
        B.add(tuba(midi_f(bm), u * 2.2), bar * 3 * u, .38, .5)
        for i, m in enumerate(arps[ch]):
            B.add(pluck(midi_f(m), u * 0.55, pick=.2), (bar*3 + i * 0.5) * u, .28, .52)
    def mel(b, m, beats, g=.4, p=.5):
        B.add(brass(midi_f(m), beats * u + 0.08, a=.06, r=.15, vib_depth=.0025),
              b * u, g, p)
    mel(0, 72, 1); mel(1, 75, 2); mel(3, 72, 1); mel(4, 70, 1); mel(5, 69, 1)
    mel(6, 72, 1); mel(7, 67, 1); mel(8, 70, 1); mel(9, 69, 1); mel(10, 67, 1)
    mel(11, 60, 2); mel(12, 72, 1); mel(13, 75, 1); mel(14, 77, 1); mel(15, 75, 1)
    mel(16, 74, 1); mel(17, 72, 1); mel(18, 70, 1); mel(19, 69, 1)
    mel(20, 67, 2); mel(22, 70, 1); mel(23, 72, 3)
    mel(24, 75, 1); mel(25, 77, 1); mel(26, 78, 1); mel(27, 77, 1)
    mel(28, 76, 1); mel(29, 74, 1); mel(30, 72, 1); mel(31, 70, 1)
    mel(32, 72, 2); mel(34, 70, 1); mel(35, 67, 3)
    for b in (11, 23, 35):
        B.add(bell(midi_f(84), .9, amp=.5), b * u + .2, .18, .6)
    for m, dt in ((48, 0), (51, .02), (55, .04)):
        B.add(brass(midi_f(m), 1.6, a=.08, r=.5), 35.6 * u + dt, .28, .5)

TRACKS = {
    "starwars": dict(fn=starwars, dur=21.5, seed=11),
    "hp": dict(fn=hp, dur=19.5, seed=21),
    "minion": dict(fn=minion, dur=15.5, seed=31),
    "coco": dict(fn=coco, dur=24.5, seed=41),
}
