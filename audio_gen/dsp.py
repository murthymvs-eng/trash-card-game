"""Tiny vectorized synth toolkit (numpy only). Stereo Bus + instrument primitives."""
import math
import numpy as np

SR = 44100

def _n(dur):
    return max(2, int(round(dur * SR)))

def t(n):
    return np.arange(n) / SR

def midi_f(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)

def _attack(tt, a):
    return 1.0 - np.exp(-tt / max(a, 1e-4))

def osc(freq, dur=0.5, amp=1.0, harm=((1, 1.0),), dk=0.0, a=0.002, r=0.05,
        vib_rate=0.0, vib_depth=0.0, detune=0.0, sweep=0.0, p0=0.0):
    """Stack of sines. harm = (ratio, amp) or (ratio, amp, dk_mult).
    sweep: pitch ratio at start (e.g. 1.02 = slight drop-in), settles fast.
    dk: overall exponential decay rate (0 = none)."""
    n = _n(dur); tt = np.arange(n) / SR
    f0 = freq * (1 + detune / 100)
    if sweep:
        ft = f0 * (1 + (sweep - 1) * np.exp(-tt / 0.05))
    else:
        ft = np.full(n, f0)
    if vib_rate > 0 and vib_depth > 0:
        vr = np.clip((tt - 0.12) / 0.3, 0, 1)
        ft = ft * (1 + vib_depth * vr * np.sin(2 * np.pi * vib_rate * tt))
    y = np.zeros(n)
    for h in harm:
        k, ah = h[0], h[1]
        dk_h = h[2] if len(h) > 2 else dk
        ph = 2 * np.pi * np.cumsum(ft * k) / SR + p0
        y += ah * np.sin(ph) * (np.exp(-tt * dk_h) if dk_h > 0 else 1.0)
    env = _attack(tt, a)
    rn = int(r * SR)
    if rn < n:
        env[-rn:] *= np.linspace(1, 0, rn)
    return y * env * amp

def pluck(freq, dur=0.9, amp=1.0, harm=((1, 1, 5), (2, .45, 7), (3, .22, 9),
                                          (4, .12, 11), (5, .05, 13)),
          a=0.001, r=0.06, detune=0.0, pick=0.12, sweep=0.997):
    y = osc(freq, dur, harm=harm, a=a, r=r, detune=detune, sweep=sweep, amp=amp)
    if pick > 0:
        nz = noise(0.012, tilt=-4, seed=7)
        L = min(len(nz), len(y))
        y[:L] += nz[:L] * (pick * 3) * np.linspace(1, 0, L)
    return y

def bell(freq, dur=1.2, amp=1.0, harm=((1, 1, 2.5), (2.003, .45, 3.5), (2.98, .28, 4.5),
                                         (4.16, .15, 5.5), (5.43, .08, 6.5)), a=0.001):
    return osc(freq, dur, harm=harm, a=a, amp=amp)

def brass(freq, dur=0.4, amp=1.0, a=0.035, r=0.12, vib_rate=5.5, vib_depth=0.004,
          sweep=1.006):
    y = osc(freq, dur, harm=((1, 1), (2, .5), (3, .3), (4, .2), (5, .12), (6, .07), (7, .04)),
            a=a, r=r, vib_rate=vib_rate, vib_depth=vib_depth, sweep=sweep, amp=amp)
    y = np.tanh(1.6 * y) / np.tanh(1.6)
    return y

def pizz(freq, dur=0.5, amp=1.0, pick=0.5):
    return pluck(freq, dur, amp=amp, harm=((1, 1, 6), (2, .5, 8), (3, .28, 10), (4, .15, 12)),
                 a=0.001, r=0.04, pick=pick, sweep=0.994)

def xylo(freq, dur=0.3, amp=1.0):
    return pluck(freq, dur, amp=amp, harm=((1, 1, 7), (2.01, .3, 9), (3.02, .15, 11)),
                 a=0.001, r=0.02, pick=0.5, sweep=0.995)

def tuba(freq, dur=0.5, amp=1.0):
    return osc(freq, dur, harm=((1, 1), (2, .3), (3, .12)), a=0.06, r=0.1, dk=1.2, amp=amp)

def square(freq, dur=0.3, amp=1.0, a=0.004, r=0.04, dk=0.0):
    return osc(freq, dur, harm=((1, 1), (3, .3), (5, .18), (7, .1), (9, .06)),
               a=a, r=r, dk=dk, amp=amp)

def tri(freq, dur=0.4, amp=1.0):
    return osc(freq, dur, harm=((1, 1), (3, .28), (5, .12)), a=0.01, r=0.08, dk=1.5, amp=amp)

def pad_chord(freqs, dur=1.0, amp=1.0, a=0.25):
    n = int(dur * SR) + SR // 10
    y = np.zeros(n)
    for f in freqs:
        for dt in (-0.15, 0, 0.15):
            y += osc(f, n / SR, harm=((1, 1), (2, .25)), a=a, r=0.3,
                     detune=dt, amp=amp / (3 * len(freqs)))
    m = np.max(np.abs(y)) or 1
    return y / m * amp

def noise(dur, amp=1.0, a=0.002, dk=6.0, low=None, high=None, f0=None, q=1.0,
          tilt=-6.0, seed=0):
    n = _n(dur); tt = t(n)
    x = np.random.default_rng(seed).standard_normal(n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if tilt:
        g *= np.power(np.maximum(f, 20) / 1000, tilt / 20)
    if low is not None:
        g *= low / np.hypot(f, low)
    if high is not None:
        g *= high / np.hypot(f, high)
    if f0 is not None:
        g *= np.exp(-0.5 * (np.log(np.maximum(f, 20) / f0) / (1.0 / (2 * max(q, 0.05)))) ** 2)
    y = np.fft.irfft(X * g, n)
    m = np.max(np.abs(y)) or 1
    env = _attack(tt, a) * np.exp(-tt * dk)
    return y / m * env * amp

def kick(amp=1.0, f0=120, f1=44, dur=0.22):
    n = _n(dur); tt = t(n)
    f = np.exp(np.log(f0) + (np.log(f1) - np.log(f0)) * np.minimum(tt / dur, 1))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 16)
    th = noise(0.05, amp=.5, low=150, dk=40, seed=3)
    y[:len(th)] += th * np.exp(-t(len(th)) * 25)
    m = np.max(np.abs(y)) or 1
    return y / m * amp

def snare(amp=1.0):
    y = noise(0.22, amp=1, f0=1800, q=1.4, dk=22, a=0.001, seed=5)
    body = osc(190, 0.16, harm=((1, 1), (2, .3)), a=0.001, r=0.05, dk=28, amp=0.35)
    y[:len(body)] += body
    return y * amp

def hat(amp=1.0):
    return noise(0.05, amp=1, high=7500, dk=55, a=0.001, seed=9) * amp

def clap(amp=1.0):
    y = np.zeros(int(0.5 * SR))
    for off, g in ((0, 1.0), (12, 0.7), (21, 0.5)):
        n = off * SR // 1000
        seg = noise(0.12, amp=g, f0=1100, q=1.8, dk=28, a=0.001, seed=off)
        L = min(len(seg), len(y) - n)
        y[n:n + L] += seg[:L]
    th = noise(0.4, amp=.35, f0=1000, q=1.2, dk=6, a=0.02, seed=44)
    y[:len(th)] += th
    return y * amp

def timpani(freq, dur=1.0, amp=1.0):
    y = osc(freq, dur, harm=((1, 1), (2, .25)), a=0.004, r=0.4, dk=2.4, amp=amp)
    th = noise(0.12, amp=.5, low=180, dk=30, seed=8)
    y[:len(th)] += th
    return y

def brush(amp=1.0):
    return noise(0.14, amp=1, f0=4200, q=0.7, dk=16, a=0.01, tilt=-4, seed=11) * amp

def shimmer(dur=1.4, amp=0.2, seed=0):
    rng = np.random.default_rng(seed)
    out = np.zeros(int(dur * SR))
    for _ in range(5):
        pos = int(rng.integers(0, int(dur * 0.55 * SR)))
        m = int(rng.choice([87, 89, 91, 93]))
        seg = bell(midi_f(m), 0.8, amp=amp)
        L = min(len(seg), len(out) - pos)
        if L > 0:
            out[pos:pos + L] += seg[:L]
    return out

class Bus:
    def __init__(self, dur):
        n = _n(dur) + SR * 3
        self.l = np.zeros(n); self.r = np.zeros(n)
        self.n = 0

    def add(self, sig, t=0.0, gain=1.0, pan=0.5):
        i = int(t * SR)
        if i + len(sig) > self.l.size:
            ext = np.zeros(i + len(sig) - self.l.size)
            self.l = np.concatenate([self.l, ext])
            self.r = np.concatenate([self.r, ext])
        self.n = max(self.n, i + len(sig))
        ang = (pan - 0.5) * 1.5708
        gl, gr = math.cos(ang), math.sin(ang)
        L, Rr = sig * (gain * gl), sig * (gain * gr)
        self.l[i:i + len(sig)] += L
        self.r[i:i + len(sig)] += Rr

    def out(self, fade=1.0, fadein=0.08, peak=0.88):
        n = self.n
        L, R = self.l[:n].copy(), self.r[:n].copy()
        fi = int(fadein * SR)
        ramp = np.linspace(0, 1, fi)
        L[:fi] *= ramp; R[:fi] *= ramp
        fo = int(fade * SR)
        if fo < n:
            ramp = np.linspace(1, 0, fo)
            L[-fo:] *= ramp; R[-fo:] *= ramp
        p = max(np.max(np.abs(L)), np.max(np.abs(R))) or 1
        k = peak / p
        return L * k, R * k

def soft(x):
    return np.tanh(x * 1.15) / np.tanh(1.15)

def _make_ir(dur, decay, seed):
    n = _n(dur)
    ir = np.random.default_rng(seed).standard_normal(n) * np.exp(-t(n) * decay)
    X = np.fft.rfft(ir)
    f = np.fft.rfftfreq(n, 1 / SR)
    ir = np.fft.irfft(X * (350 / np.hypot(f, 350) + 0.15), n)
    return ir / (np.linalg.norm(ir) / 8.0)

def room(l, r, amt=0.22, ir_dur=1.5, decay=3.2, seed=0):
    il, ir_ = _make_ir(ir_dur, decay, seed), _make_ir(ir_dur, decay, seed + 1)
    n = len(l) + len(il) - 1
    cl = np.fft.irfft(np.fft.rfft(l, n) * np.fft.rfft(il, n), n)[:len(l)]
    cr = np.fft.irfft(np.fft.rfft(r, n) * np.fft.rfft(ir_, n), n)[:len(r)]
    return l + cl * amt, r + cr * amt

import wave

def wav(path, l, r=None):
    if r is None:
        data = (l * 32767).astype('<i2')
        with wave.open(path, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(data.tobytes())
        return
    n = len(l)
    data = np.empty(n * 2, dtype='<i2')
    data[0::2] = (l * 32767).astype('<i2')
    data[1::2] = (r * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
