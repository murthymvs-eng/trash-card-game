# Trash — Game Audio

Synthesized movie-theme music + game SFX for the Trash card game. All audio is
rendered from written note data (numpy synth in `../audio_gen/`) — original
evocations of the film soundtracks, except **Mario**: a transcription of the
SMB overworld theme from a reference recording (basic-pitch →
`../audio_gen/midi/mario/`, rendered with NES-style chiptune voices).

## Layout

| Path | What |
|---|---|
| `music/<theme>.wav` | Loopable theme track per deck (stereo 44.1 kHz, fade in/out for seamless looping) |
| `sfx/*.wav` | Core game SFX: `click`, `draw`, `place`, `discard`, `err`, `win` |
| `sfx/<theme>/<name>.wav` | Signature SFX per movie theme (mono) |
| `mp3/…` | MP3 mirrors (music 96 kbps, SFX 64 kbps) — smaller for web |

## Theme → music map

| Theme id | Track | Evokes |
|---|---|---|
| `starwars` | `music/starwars.wav` | Star Wars main title (1977) — transcribed from a reference recording (brass over tuba bass + timpani, ~88 s) |
| `hp` | `music/hp.wav` | Hedwig's Theme — G-minor waltz, pizzicato riff |
| `minion` | `music/minion.wav` | Goofy Despicable-Me style: tuba + xylophone |
| `coco` | `music/coco.wav` | "Remember Me" / Bésame Mucho waltz, nylon guitar |
| `avengers` | `music/avengers.wav` | Avengers Assembled — heroic brass march |
| `spiderman` | `music/spiderman.wav` | 60s TV theme — jazzy sax, walking bass, swing |
| `toystory` | `music/toystory.wav` | "You've Got a Friend in Me" folk guitar |
| `moana` | `music/moana.wav` | Pacific 6/8 waltz, ukulele + marimba melody |
| `princess` | `music/princess.wav` | Disney-fairy waltz — celesta, strings, sparkle |
| `taylor` | `music/taylor.wav` | Arena-pop anthem: four-on-floor, pad, crowd |
| `mario` | `music/mario.wav` | SMB overworld theme — transcribed from a reference recording (2 pulse melody + triangle bass, full ~82s song) |
| `classic` (also fallback for `animal`/`fairy`/`neon`/`wood`) | `music/classic.wav` | Cheerful piano/celesta card-game jingle |

## SFX map

Core (matches `sfx(kind)` in `index.html`): `draw` (whoosh+paper), `place`
(thock + ching), `discard` (flick), `err` (buzz), `win` (fanfare), `click`.

Signature SFX per theme (play on theme-appropriate moments, or as the
`draw`/`place` flavor when that theme is active):

| Theme | SFX |
|---|---|
| starwars | `starwars_pew` (laser), `starwars_tie` (flyby rumble) |
| hp | `hp_wand` (whoosh + sparkle) |
| minion | `minion_boing` |
| coco | `coco_strum` (guitar strum) |
| avengers | `avengers_thunder` |
| spiderman | `spiderman_web` (zip + boing) |
| toystory | `toystory_squeak` (pull-string) |
| moana | `moana_wave` (ocean) |
| princess | `princess_fairy` (fairy dust) |
| taylor | `taylor_shutter` (camera + crowd) |
| mario | `mario_jump`, `mario_coin` |
| fairy / neon / animal | `fairy_sparkle` / `neon_zap` / `animal_wiggle` |

## Using in the web game

1. Copy or keep the `audio/` folder next to `index.html`.
2. Replace the WebAudio `sfx(kind)` with preloaded buffers (or `<audio>`
   elements), e.g.:

```js
const SFX = {draw:'audio/mp3/sfx/draw.mp3', place:'audio/mp3/sfx/place.mp3',
             discard:'audio/mp3/sfx/discard.mp3', err:'audio/mp3/sfx/err.mp3',
             win:'audio/mp3/sfx/win.mp3'};
```

3. Theme music: load `audio/mp3/music/<themeId>.mp3` as a looping track;
   start on theme select / game start, duck ~6 dB under SFX. The SVG themes
   (`animal`, `fairy`, `neon`, `wood`) fall back to `classic.mp3`.

iOS: WAV masters work as-is; for smaller bundles use the MP3s (or re-mux to
.m4a/CAF).

## Regenerating

```
python3 audio_gen/run.py   # needs numpy + ffmpeg; writes WAV + MP3, prints report
```

Tweak note data in `audio_gen/themes_*.py` (midi numbers, beats) or SFX
shapes in `audio_gen/sfx_a.py` / `sfx_b.py`, then re-run.
