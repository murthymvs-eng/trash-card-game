"""SFX part 2: remaining theme SFX + registries."""
import numpy as np
from dsp import *
from sfx_a import put, trim, core_click, core_draw, core_place, core_discard, \
    core_err, core_win, sw_pew, sw_tie, hp_wand, minion_boing, coco_strum, \
    av_thunder, sp_web

def toys_squeak():
    y = np.zeros(int(0.6 * SR))
    for k, tt_ in enumerate((0, .22)):
        n = int(.14 * SR)
        tt2 = np.arange(n) / SR
        f = (190 + 90 * tt2 / (n / SR)) * (1 + .35 * np.sin(2 * np.pi * 26 * tt2))
        seg = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt2 * 18)
        seg = np.tanh(2.2 * seg) / np.tanh(2.2)
        put(y, seg, tt_, .35)
    put(y, noise(.25, low=500, dk=8, a=.02, seed=70), .3, .2)
    return trim(y)

def moana_wave():
    y = np.zeros(int(1.6 * SR))
    for i, (fc, d) in enumerate(((220, .5), (420, .5), (700, .6))):
        put(y, noise(d, low=fc, tilt=-8, dk=1.2, a=.3, seed=80 + i), i * .45, .5)
    put(y, noise(.3, amp=.2, f0=3200, q=.6, dk=10, a=.1, seed=90), .7)
    return trim(y)

def pr_fairy():
    y = np.zeros(int(2.4 * SR))
    rng = np.random.default_rng(100)
    for j in range(9):
        tt_ = j * .09 + rng.uniform(0, .04)
        m = int(rng.choice([84, 88, 91, 96]))
        put(y, bell(midi_f(m), 1.4, amp=.7), tt_, .22)
    put(y, pad_chord([midi_f(m) for m in (60, 64, 67, 72)], 2.0, a=.4), 0, .16)
    return trim(y)

def taylor_shutter():
    y = np.zeros(int(1.5 * SR))
    for tt_ in (0, .07):
        put(y, osc(2400, .02, harm=((1, 1), (3, .4)), a=.0005, r=.02, amp=.5), tt_)
        put(y, noise(.015, high=4000, dk=90, seed=int(tt_ * 100) + 1), tt_)
    put(y, osc(800, .08, harm=((1, 1), (2, .3)), a=.002, r=.04, amp=.3), 0)
    put(y, noise(1.2, f0=950, q=.5, tilt=-3, dk=.8, a=.5, seed=110), .1, .3)
    return trim(y)

def mario_jump():
    y = np.zeros(int(0.35 * SR))
    n = int(.18 * SR)
    f = np.exp(np.log(660) + (np.log(1760) - np.log(660)) * np.arange(n) / n)
    y[:n] = np.sin(2 * np.pi * np.cumsum(f) / SR) * \
        (1 - np.exp(-np.arange(n) / SR * 60)) * .7
    put(y, osc(1760, .12, harm=((1, 1), (3, .3)), a=.004, r=.05, amp=.3), .18)
    return trim(y)

def mario_coin():
    y = np.zeros(int(0.45 * SR))
    put(y, square(987, .07, amp=.5, r=.02), 0)
    put(y, square(1319, .3, amp=.45, r=.08), .07)
    return trim(y)

def fairy_sparkle():
    y = np.zeros(int(1.2 * SR))
    rng = np.random.default_rng(200)
    for j in range(6):
        tt_ = j * .07 + rng.uniform(0, .03)
        m = int(rng.choice([89, 92, 96, 99]))
        put(y, bell(midi_f(m), .8, amp=.6), tt_, .25)
    put(y, pad_chord([midi_f(m) for m in (64, 67, 71, 76)], 1.0, a=.3), 0, .14)
    return trim(y)

def neon_zap():
    y = np.zeros(int(0.4 * SR))
    n = int(.12 * SR)
    f = np.exp(np.log(5200) + (np.log(300) - np.log(5200)) * np.arange(n) / n)
    y[:n] = np.sin(2 * np.pi * np.cumsum(f) / SR) * .6
    put(y, noise(.08, high=5000, dk=30, a=.01, seed=130), 0, .3)
    put(y, osc(70, .2, harm=((1, 1), (2, .4)), dk=10, a=.01, amp=.4), 0)
    return trim(y)

def animal_wiggle():
    y = np.zeros(int(0.5 * SR))
    n = int(.3 * SR)
    tt2 = np.arange(n) / SR
    f = 520 + 120 * np.sin(2 * np.pi * 9 * tt2)
    y[:n] = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt2 * 5) * .5
    put(y, osc(880, .12, harm=((1, 1), (2, .4)), a=.01, r=.05, amp=.3), .28)
    return trim(y)

CORE = {
    "click": core_click, "draw": core_draw, "place": core_place,
    "discard": core_discard, "err": core_err, "win": core_win,
}
THEME_SFX = {
    "starwars": {"starwars_pew": sw_pew, "starwars_tie": sw_tie},
    "hp": {"hp_wand": hp_wand},
    "minion": {"minion_boing": minion_boing},
    "coco": {"coco_strum": coco_strum},
    "avengers": {"avengers_thunder": av_thunder},
    "spiderman": {"spiderman_web": sp_web},
    "toystory": {"toystory_squeak": toys_squeak},
    "moana": {"moana_wave": moana_wave},
    "princess": {"princess_fairy": pr_fairy},
    "taylor": {"taylor_shutter": taylor_shutter},
    "mario": {"mario_jump": mario_jump, "mario_coin": mario_coin},
    "fairy": {"fairy_sparkle": fairy_sparkle},
    "neon": {"neon_zap": neon_zap},
    "animal": {"animal_wiggle": animal_wiggle},
}
