# Theme music — drop in your own tracks

The app plays **per-theme** music with two moods: **menu** (start screen) and **game** (during play).
If a bundled audio file exists it is used; otherwise a procedural fallback plays.

## Where to put files
Put audio files here:

```
ios/TrashGame/TrashGame/Music/
```

They are flattened into the app bundle root automatically, so name them exactly as below.

## Naming
```
music_<theme>_<mode>.<ext>
```
- `<theme>`: `classic, animal, minion, fairy, neon, wood, hp, avengers, starwars, spiderman, coco, princess, taylor, moana, toystory`
- `<mode>`: `menu` or `game`
- `<ext>`: `m4a` (recommended), `mp3`, `caf`, `wav`, `aiff`

Examples:
```
music_starwars_menu.m4a
music_starwars_game.m4a
music_hp_game.m4a
music_minion_menu.m4a
```

Accepted alternates (loader is forgiving): `<theme>_<mode>.<ext>`, `<theme>_<mode>_music.<ext>`, `<theme>-<mode>.<ext>`

## Behaviour
- `menu` track plays on the start screen; `game` track plays during a game.
- Loops indefinitely. Volume ~0.42 (menu) / ~0.5 (game). Silenced by the in-app 🔊 toggle.
- Console logs `[Music] bundled track: <name>` when a file is used, or `[Music] synth fallback: ...` otherwise.
- You are responsible for having the rights to any tracks you add (this repo doesn't include copyrighted audio).

## Note
`music_minion_menu.wav` is a small procedural placeholder included to demonstrate/verify the pipeline —
replace it with your own file when you have one.
