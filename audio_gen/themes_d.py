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
    # Iconic SMB overworld theme — transcribed from the reference recording
    # (basic-pitch: midi/mario/track_basic_pitch.csv). NES-style voices:
    # triangle bass + two greedy-split pulse melody voices (square1/square2).
    import csv, os
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, 'midi', 'mario', 'track_basic_pitch.csv')
    rows = list(csv.DictReader(open(p)))
    lo = 56  # notes below this go to the triangle bass voice
    bass, mel = [], []
    for r in rows:
        (bass if int(r['pitch_midi']) < lo else mel).append(r)
    # monophonic bass: drop overlaps (keep the earlier note)
    bass.sort(key=lambda r: (float(r['start_time_s']), -float(r['end_time_s'])))
    kept, end = [], 0.0
    for r in bass:
        t0 = float(r['start_time_s'])
        if t0 >= end - 0.02:
            kept.append(r); end = float(r['end_time_s'])
    bass = kept
    # greedy two-voice polyphony: prefer a free voice, tie-break by pitch proximity
    mel.sort(key=lambda r: (float(r['start_time_s']), -float(r['end_time_s'])))
    va, vb = [0.0, -99], [0.0, -99]
    out = []
    for r in mel:
        t0 = float(r['start_time_s']); m = int(r['pitch_midi'])
        cands = [n for n, v in (('A', va), ('B', vb)) if v[0] <= t0 + 0.02]
        if cands:
            name = min(cands, key=lambda n: abs((va if n == 'A' else vb)[1] - m))
        else:
            name = min(('A', 'B'), key=lambda n: (va if n == 'A' else vb)[0])
        (va if name == 'A' else vb)[1] = m
        (va if name == 'A' else vb)[0] = float(r['end_time_s'])
        out.append((name, r))
    for r in bass:
        t0, t1 = float(r['start_time_s']), float(r['end_time_s'])
        g = 0.30 + 0.50 * int(r['velocity']) / 127.0
        B.add(tri(midi_f(int(r['pitch_midi'])), (t1 - t0) + 0.06, amp=1.0), t0, g, 0.5)
    for name, r in out:
        t0, t1 = float(r['start_time_s']), float(r['end_time_s'])
        g = (0.22 + 0.40 * int(r['velocity']) / 127.0) * (1.0 if name == 'A' else 0.92)
        B.add(square(midi_f(int(r['pitch_midi'])), (t1 - t0) + 0.03, amp=1.0, r=0.02),
              t0, g, 0.47 if name == 'A' else 0.53)
    # pad the tail with silence so the bus fade rides on silence, not notes
    t_last = max(float(r['end_time_s']) for r in rows)
    B.add(np.zeros(int(2.0 * SR)), t_last + 0.1, 1.0, 0.5)

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

def frozen(B):
    # "Let It Go" — transcribed from the reference recording (basic-pitch:
    # midi/frozen/track_basic_pitch.csv). Frozen-style voices: celesta/bell
    # attack + string pad for the melody, soft triangle bass, icy shimmer on
    # the high notes.
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    songFromCSV(B, os.path.join(here, 'midi', 'frozen', 'track_basic_pitch.csv'))

TRACKS = {
    "princess": dict(fn=princess, dur=20.5, seed=91),
    "taylor": dict(fn=taylor, dur=18.5, seed=101),
    "mario": dict(fn=mario, dur=82.0, seed=111),
    "frozen": dict(fn=frozen, dur=220.0, seed=131),
    "classic": dict(fn=classic, dur=18.5, seed=121),
}
