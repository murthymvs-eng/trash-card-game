"""SFX part 1: core game sounds + first half of theme SFX."""
import numpy as np
from dsp import *

def put(y, seg, t=0.0, g=1.0):
    i = int(t * SR)
    L = min(len(seg), len(y) - i)
    if L > 0:
        y[i:i + L] += seg[:L] * g
    return y

def trim(y, tail=0.12, floor=0.004):
    m = np.max(np.abs(y)) or 1
    idx = np.where(np.abs(y) > m * floor)[0]
    if len(idx):
        end = min(len(y), int(idx[-1]) + int(tail * SR))
        y = y[:end]
    y = y.copy()
    n = int(0.02 * SR)
    y[-min(n, len(y)):] *= np.linspace(1, 0, min(n, len(y)))
    m = np.max(np.abs(y)) or 1
    return y / m * 0.85

def core_click():
    y = np.zeros(int(0.08 * SR))
    put(y, osc(700, .05, harm=((1, 1), (2, .3)), a=.0005, r=.03, amp=.5))
    put(y, noise(.015, high=6000, dk=80, seed=2), 0, .25)
    return trim(y)

def core_draw():
    y = np.zeros(int(0.26 * SR))
    for i, (fc, d) in enumerate(((600, .07), (1500, .07), (3600, .08))):
        put(y, noise(d, amp=.5, f0=fc, q=.8, dk=8, a=.01, seed=i), i * .055)
    for j, (tt_, s) in enumerate(((.05, 10), (.08, 11), (.11, 12))):
        put(y, noise(.02, amp=.35, f0=4200, q=.6, dk=90, seed=s), tt_)
    put(y, osc(900, .05, harm=((1, 1), (2, .3)), a=.001, r=.02, amp=.3))
    return trim(y)

def core_place():
    y = np.zeros(int(0.8 * SR))
    put(y, kick(f0=160, f1=60, dur=.14), 0, .95)
    put(y, noise(.03, amp=.3, f0=2500, q=.7, dk=60, seed=4), 0)
    put(y, bell(784, .5, amp=.5), .1, .3)
    put(y, bell(1047, .7, amp=.5), .16, .3)
    put(y, bell(1568, .9, amp=.3), .16, .14)
    return trim(y)

def core_discard():
    y = np.zeros(int(0.4 * SR))
    put(y, noise(.04, amp=.8, f0=2000, q=.9, dk=50, seed=6))
    put(y, osc(300, .18, harm=((1, 1), (2, .3)), a=.002, r=.08, amp=.5), 0)
    y = y * np.exp(-t(len(y)) * 4)
    for j, (tt_, s) in enumerate(((.12, 13), (.16, 14))):
        put(y, noise(.02, amp=.3, f0=3800, q=.6, dk=90, seed=s), tt_)
    return trim(y)

def core_err():
    y = np.zeros(int(0.4 * SR))
    put(y, square(105, .1, amp=.5, a=.004, r=.02), 0)
    put(y, square(98, .12, amp=.45, a=.004, r=.03), .14)
    put(y, kick(f0=70, f1=40, dur=.16), .02, .5)
    return trim(y)

def core_win():
    y = np.zeros(int(2.6 * SR))
    for tt_, f in ((0, 523.25), (.12, 659.25), (.24, 783.99)):
        put(y, square(f, .16, amp=.5, r=.03), tt_)
    put(y, square(1046.5, .5, amp=.5, r=.1), .36)
    put(y, pad_chord([523.25, 659.25, 783.99, 1046.5], 1.4, a=.1), .55, .3)
    put(y, timpani(65.4, 1.0, amp=.6), .5, .5)
    put(y, shimmer(1.0, amp=.12, seed=9), 1.0)
    return trim(y)

def sw_pew():
    y = np.zeros(int(0.4 * SR))
    n = int(0.2 * SR)
    f = np.exp(np.log(2400) + (np.log(160) - np.log(2400)) * np.arange(n) / n)
    y[:n] = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-np.arange(n) / SR * 14)
    y *= 1 + .3 * np.sin(2 * np.pi * 8 * t(len(y)))
    put(y, noise(.02, amp=.3, f0=2200, q=1, dk=60, seed=3), 0)
    put(y, kick(f0=70, f1=45, dur=.15), 0, .4)
    return trim(y)

def sw_tie():
    y = np.zeros(int(1.1 * SR))
    dur = 1.0
    e = t(dur)
    env = np.exp(-e * 1.8) * (1 + .4 * np.sin(2 * np.pi * 32 * e))
    put(y, noise(1.1, low=140, tilt=-12, dk=.8, a=.15, seed=17), 0, .7)
    put(y, osc(55, dur, harm=((1, 1), (2, .3)), dk=.9, a=.1, amp=.5) * env, 0)
    return trim(y)

def hp_wand():
    y = np.zeros(int(0.7 * SR))
    for i, (fc, d) in enumerate(((500, .08), (1600, .08), (4200, .1))):
        put(y, noise(d, amp=.55, f0=fc, q=.9, dk=10, a=.01, seed=i + 20), i * .07)
    for j, (tt_, m) in enumerate(((.22, 91), (.26, 93), (.3, 96), (.34, 93))):
        put(y, bell(midi_f(m), .5, amp=.6), tt_, .18)
    put(y, noise(.012, amp=.3, f0=6000, q=.5, dk=120, seed=31), .3)
    return trim(y)

def minion_boing():
    y = np.zeros(int(1.0 * SR))
    n = int(.8 * SR)
    tt2 = np.arange(n) / SR
    ft = 850 - (850 - 120) * np.arange(n) / n
    ft *= 1 + .18 * np.exp(-tt2 * 5) * np.sin(2 * np.pi * 16 * tt2)
    y[:n] = np.sin(2 * np.pi * np.cumsum(ft) / SR) * np.exp(-tt2 * 3)
    put(y, noise(.03, amp=.2, f0=900, q=.8, dk=60, seed=40), 0)
    return trim(y)

def coco_strum():
    y = np.zeros(int(1.0 * SR))
    for j, m in enumerate((48, 51, 55, 58, 64)):
        put(y, pluck(midi_f(m), .5, pick=.4), j * .02, .3)
    put(y, pluck(midi_f(36), .6, pick=.3), 0, .35)
    put(y, noise(.04, amp=.25, f0=2800, q=.8, dk=50, seed=44))
    return trim(y)

def av_thunder():
    y = np.zeros(int(2.2 * SR))
    put(y, noise(2.2, low=90, tilt=-12, dk=.7, a=.2, seed=50), 0, .7)
    put(y, timpani(midi_f(41), 1.2, amp=.5), 0, .5)
    for m, dt in ((49, .5), (57, .52), (60, .54)):
        put(y, brass(midi_f(m), 1.0, a=.03, r=.3), dt, .35)
    return trim(y)

def sp_web():
    y = np.zeros(int(0.5 * SR))
    n = int(.1 * SR)
    f = np.exp(np.log(1500) + (np.log(260) - np.log(1500)) * np.arange(n) / n)
    y[:n] = np.sin(2 * np.pi * np.cumsum(f) / SR) * .6
    m2 = int(.4 * SR)
    tt2 = np.arange(m2) / SR
    ft = 400 * (1 + .25 * np.exp(-tt2 * 10) * np.sin(2 * np.pi * 14 * tt2))
    y[n:n + m2] += np.sin(2 * np.pi * np.cumsum(ft) / SR) * np.exp(-tt2 * 8) * .3
    put(y, noise(.02, amp=.25, f0=3000, q=.8, dk=80, seed=60), 0)
    return trim(y)
