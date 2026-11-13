#!/usr/bin/env python3
"""Generate all game audio: movie-evoking music themes + SFX.
Writes WAV masters under ../audio/{music,sfx} and MP3 mirrors under ../audio/mp3.
"""
import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from dsp import Bus, room, soft, wav, SR
from themes_a import TRACKS as TA
from themes_b import TRACKS as TB
from themes_c import TRACKS as TC
from themes_d import TRACKS as TD
from sfx_b import CORE, THEME_SFX

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, "audio", "music")
SFX = os.path.join(ROOT, "audio", "sfx")
MP3 = os.path.join(ROOT, "audio", "mp3")
for d in (MUSIC, SFX, MP3):
    os.makedirs(d, exist_ok=True)

TRACKS = {}
for mod in (TA, TB, TC, TD):
    TRACKS.update(mod)

report = []

def stats(name, l):
    m = l if l.ndim > 1 else np.abs(l)
    peak = float(np.max(np.abs(m))) if len(m) else 0.0
    rms = float(np.sqrt(np.mean(np.square(m)))) if len(m) else 0.0
    dur = (m.shape[1] if m.ndim > 1 else len(m)) / SR
    return dur, peak, rms

def write_mp3(wav_path, mp3_path, bitrate):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
         "-codec:a", "libmp3lame", "-b:a", bitrate, mp3_path],
        check=True)

print("=== MUSIC ===")
for name, spec in TRACKS.items():
    B = Bus(spec["dur"])
    spec["fn"](B)
    L, R = B.out(fade=1.6, fadein=0.08)
    L, R = room(soft(L), soft(R), amt=0.2, seed=spec["seed"])
    p = max(np.max(np.abs(L)), np.max(np.abs(R))) or 1
    k = 0.88 / p
    L, R = L * k, R * k
    path = os.path.join(MUSIC, name + ".wav")
    wav(path, L, R)
    dur, pk, rms = stats(name, np.stack([L, R]))
    mp3dir = os.path.join(MP3, "music")
    os.makedirs(mp3dir, exist_ok=True)
    write_mp3(path, os.path.join(mp3dir, name + ".mp3"), "96k")
    report.append(("music/%s.wav" % name, dur, pk, rms))
    print("  %-12s %5.1fs  peak %.2f" % (name, dur, pk))

print("=== SFX ===")
os.makedirs(os.path.join(MP3, "sfx"), exist_ok=True)
os.makedirs(os.path.join(MP3, "music"), exist_ok=True)

def emit(relpath, arr, mono=True):
    arr = soft(arr)
    p = np.max(np.abs(arr)) or 1
    arr = arr * (0.85 / p)
    path = os.path.join(ROOT, "audio", relpath + ".wav")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wav(path, arr, None if mono else arr)
    dur, pk, rms = stats(relpath, arr)
    mpath = os.path.join(MP3, relpath + ".mp3")
    os.makedirs(os.path.dirname(mpath), exist_ok=True)
    write_mp3(path, mpath, "64k")
    report.append((relpath + ".wav", dur, pk, rms))
    print("  %-40s %5.2fs" % (relpath, dur))

for name, fn in CORE.items():
    emit("sfx/" + name, np.asarray(fn(), dtype=np.float64))
for theme, sounds in THEME_SFX.items():
    for name, fn in sounds.items():
        emit("sfx/%s/%s" % (theme, name), np.asarray(fn(), dtype=np.float64))

print("=== REPORT ===")
bad = []
for rel, dur, pk, rms in report:
    flag = ""
    if rms < 0.004:
        flag = "  !! too quiet"
        bad.append(rel)
    print("  %-42s %6.2fs  pk %.2f rms %.3f%s" % (rel, dur, pk, rms, flag))
print("Total files: WAV %d  (+%d MP3)" % (len(report), len(report)))
if bad:
    print("WARNING low-level files:", bad)
