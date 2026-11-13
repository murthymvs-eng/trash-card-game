"""Music tracks part 3: toystory, moana."""
from dsp import *

def toystory(B):
    u = 0.5
    roots = [36, 43, 45, 41, 36, 43, 45, 41, 36, 36, 43, 36]
    arps = {"C": [55, 60, 64, 60, 55, 60, 64, 60],
            "G": [62, 67, 71, 67, 62, 67, 71, 67],
            "Am": [57, 60, 64, 60, 57, 60, 64, 60],
            "F": [53, 60, 65, 60, 53, 65, 60, 65]}
    chords = ["C", "G", "Am", "F", "C", "G", "Am", "F", "C", "C", "G", "C"]
    for bar, (rt, ch) in enumerate(zip(roots, chords)):
        B.add(pluck(midi_f(rt), u * 1.6, pick=.25), bar*4 * u, .4, .42)
        B.add(pluck(midi_f(rt), u * 1.6, pick=.25), (bar*4 + 2) * u, .3, .42)
        for i, m in enumerate(arps[ch]):
            B.add(pluck(midi_f(m), u * 0.5, pick=.15), (bar*4 + i * 0.5) * u, .18, .5)
    def mel(b, m, beats, g=.45, p=.5):
        B.add(pluck(midi_f(m), beats * u + .25, pick=.2), b * u, g, p)
    mel(0, 72, 1); mel(1, 76, 1); mel(2, 72, 1); mel(3, 76, 1)
    mel(4, 74, 1); mel(5, 72, 1); mel(6, 71, 1); mel(7, 72, 1)
    mel(8, 69, 1); mel(9, 71, 1); mel(10, 72, 1); mel(11, 74, 1)
    mel(12, 76, 1.5); mel(13.5, 72, 2.5)
    mel(16, 72, 1); mel(17, 76, 1); mel(18, 74, 1); mel(19, 76, 1)
    mel(20, 79, 1); mel(21, 76, 1); mel(22, 74, 1); mel(23, 76, 1)
    mel(24, 72, 1); mel(25, 71, 1); mel(26, 69, 1); mel(27, 67, 1)
    mel(28, 64, 2); mel(30, 67, 2)
    mel(32, 84, 1); mel(33, 88, 1); mel(34, 84, 1); mel(35, 88, 1)
    mel(36, 86, 1); mel(37, 84, 1); mel(38, 83, 1); mel(39, 84, 1)
    mel(40, 81, 1); mel(41, 83, 1); mel(42, 84, 1); mel(43, 86, 1)
    mel(44, 88, 1.5, g=.5); mel(45.5, 84, 2.5, g=.5)
    for bar in range(12):
        B.add(kick(), bar*4 * u, .22); B.add(kick(), (bar*4 + 2) * u, .22)
        B.add(brush(), (bar*4 + 1) * u, .2); B.add(brush(), (bar*4 + 3) * u, .2)
    for bar in range(8, 12):
        for i in range(8):
            B.add(hat(), (bar*4 + i * 0.5 + 0.25) * u, .07)

def moana(B):
    e = 0.18
    am, F, G, C = [45, 52, 57, 60, 64, 69], [41, 48, 53, 57, 60, 65], \
        [43, 50, 55, 59, 62, 67], [48, 55, 60, 64, 67, 72]
    bars = [am, am, F, G] * 4
    for bar, notes in enumerate(bars):
        for i, m in enumerate(notes):
            B.add(pluck(midi_f(m), e * 0.9, pick=.25), (bar*6 + i) * e, .26, .5)
    def mel(eb, m, beats, g=.38, p=.5):
        B.add(bell(midi_f(m), beats * e + .3, amp=.8), eb * e, g, p)
    mel(24, 69, 2); mel(26, 72, 2); mel(28, 76, 2)
    mel(30, 74, 2); mel(32, 72, 2); mel(34, 69, 2)
    mel(36, 69, 2); mel(38, 71, 2); mel(40, 72, 2)
    mel(42, 74, 4, g=.42); mel(46, 69, 2)
    mel(48, 72, 2); mel(50, 74, 2); mel(52, 76, 2)
    mel(54, 79, 2, g=.42); mel(56, 76, 2); mel(58, 74, 2)
    mel(60, 72, 2); mel(62, 74, 2); mel(64, 76, 2)
    mel(66, 79, 6, g=.44)
    mel(72, 76, 2); mel(74, 74, 2); mel(76, 72, 2)
    mel(78, 71, 2); mel(80, 69, 2); mel(82, 67, 2)
    mel(84, 69, 2); mel(86, 71, 2); mel(88, 72, 2)
    mel(90, 69, 6, g=.44)
    B.add(pad_chord([midi_f(m) for m in (45, 52, 57, 60, 64)], 3.0, a=.4),
          90 * e, .3, .5)

TRACKS = {
    "toystory": dict(fn=toystory, dur=26.5, seed=71),
    "moana": dict(fn=moana, dur=19.5, seed=81),
}
