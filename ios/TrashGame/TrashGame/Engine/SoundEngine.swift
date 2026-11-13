import AVFoundation

/// Synthesized sound effects (ported from the web build's WebAudio `sfx()`).
/// Plays from in-memory 16-bit WAV data via AVAudioPlayer — avoids the
/// format/state NSExceptions that AVAudioPlayerNode.scheduleBuffer can throw.
@MainActor
final class SoundEngine {
    static let shared = SoundEngine()

    private var muted = false
    private let sampleRate: Double = 44100
    private var cache: [String: AVAudioPlayer] = [:]
    private var fileCache: [String: AVAudioPlayer] = [:]

    private struct Tone { let f0: Double; let f1: Double; let dur: Double; let vol: Double; let delay: Double; let wave: Wave }
    private enum Wave { case sine, square, sawtooth }

    private init() {
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.ambient, options: [.mixWithOthers])
        try? session.setActive(true)
    }

    func setMuted(_ m: Bool) { muted = m }

    /// Theme-flavoured signature sounds layered on top of the core SFX.
    /// theme id → core event ("draw"/"place"/"win") → bundled file base name.
    private static let signatures: [String: [String: String]] = [
        "starwars":  ["place": "starwars_pew", "draw": "starwars_tie"],
        "hp":        ["draw": "hp_wand"],
        "minion":    ["place": "minion_boing"],
        "coco":      ["draw": "coco_strum"],
        "avengers":  ["place": "avengers_thunder"],
        "spiderman": ["place": "spiderman_web"],
        "toystory":  ["draw": "toystory_squeak"],
        "moana":     ["draw": "moana_wave"],
        "princess":  ["place": "princess_fairy"],
        "taylor":    ["win": "taylor_shutter"],
        "mario":     ["draw": "mario_jump", "place": "mario_coin"],
        "frozen":    ["draw": "frozen_gust", "place": "frozen_sparkle"],
        "animal":    ["place": "animal_wiggle"],
        "fairy":     ["place": "fairy_sparkle"],
        "neon":      ["place": "neon_zap"]
    ]

    /// Plays a game sound: the bundled file when present, the synthesized tone
    /// otherwise. `theme` adds the theme's signature sound underneath.
    func play(_ kind: String, theme: String? = nil) {
        guard !muted else { return }
        if let theme, let sig = SoundEngine.signatures[theme]?[kind] {
            _ = playFile(named: "sfx_\(sig)", volume: 0.6)
        }
        if playFile(named: "sfx_\(kind)", volume: 0.95) { return }
        playSynth(kind)
    }

    /// Plays a bundled resource (e.g. `sfx_draw.mp3`). False when it is missing.
    private func playFile(named base: String, volume: Float) -> Bool {
        let player: AVAudioPlayer
        if let p = fileCache[base] {
            player = p
        } else {
            var url: URL?
            for ext in ["mp3", "wav", "m4a", "caf", "aiff"] {
                if let u = Bundle.main.url(forResource: base, withExtension: ext) { url = u; break }
            }
            guard let u = url, let p = try? AVAudioPlayer(contentsOf: u) else { return false }
            p.prepareToPlay()
            fileCache[base] = p
            player = p
        }
        player.currentTime = 0
        player.volume = volume
        player.play()
        return true
    }

    /// Synthesized fallback (kept for themes/sounds without a bundled file).
    private func playSynth(_ kind: String) {
        if let p = cache[kind] {
            p.currentTime = 0
            p.play()
            return
        }
        guard let data = wavData(for: kind), let p = try? AVAudioPlayer(data: data) else { return }
        p.prepareToPlay()
        cache[kind] = p
        p.play()
    }

    // MARK: - Synthesis

    private func tones(for kind: String) -> [Tone] {
        switch kind {
        case "draw":    return [Tone(f0: 300, f1: 540, dur: 0.10, vol: 0.12, delay: 0, wave: .sine)]
        case "place":   return [Tone(f0: 500, f1: 780, dur: 0.11, vol: 0.14, delay: 0, wave: .sine)]
        case "err":     return [Tone(f0: 170, f1: 90, dur: 0.16, vol: 0.12, delay: 0, wave: .sawtooth)]
        case "discard": return [Tone(f0: 280, f1: 160, dur: 0.12, vol: 0.10, delay: 0, wave: .sine)]
        case "win":
            return [
                Tone(f0: 523, f1: 523, dur: 0.14, vol: 0.13, delay: 0, wave: .square),
                Tone(f0: 659, f1: 659, dur: 0.14, vol: 0.13, delay: 0.12, wave: .square),
                Tone(f0: 784, f1: 784, dur: 0.14, vol: 0.13, delay: 0.24, wave: .square),
                Tone(f0: 1046, f1: 1046, dur: 0.32, vol: 0.13, delay: 0.36, wave: .square)
            ]
        default: return []
        }
    }

    private func samples(for kind: String) -> [Float] {
        let ts = tones(for: kind)
        guard let total = ts.map({ $0.delay + $0.dur }).max(), total > 0 else { return [] }
        var out = [Float](repeating: 0, count: Int(total * sampleRate) + 2048)
        for tone in ts {
            let start = Int(tone.delay * sampleRate)
            let count = Int(tone.dur * sampleRate)
            for i in 0..<count {
                let t = Double(i) / sampleRate
                let frac = t / tone.dur
                let f = tone.f0 * pow(tone.f1 / tone.f0, frac)
                let phase = 2 * Double.pi * f * t
                let s: Double
                switch tone.wave {
                case .sine:     s = sin(phase)
                case .square:   s = sin(phase) >= 0 ? 1 : -1
                case .sawtooth: s = 2 * ((f * t).truncatingRemainder(dividingBy: 1)) - 1
                }
                out[start + i] += Float(s * tone.vol * exp(-4 * frac))
            }
        }
        return out
    }

    private func wavData(for kind: String) -> Data? {
        let s = samples(for: kind)
        guard !s.isEmpty else { return nil }
        var pcm = [Int16](repeating: 0, count: s.count)
        for i in 0..<s.count {
            let v = max(-1.0, min(1.0, Double(s[i])))
            pcm[i] = Int16(v * 32767)
        }
        let sr = Int(sampleRate)
        let byteRate = sr * 2
        let dataSize = pcm.count * 2
        var data = Data()
        func u32(_ v: UInt32) { var le = v.littleEndian; withUnsafeBytes(of: &le) { data.append(contentsOf: $0) } }
        func u16(_ v: UInt16) { var le = v.littleEndian; withUnsafeBytes(of: &le) { data.append(contentsOf: $0) } }
        data.append(contentsOf: "RIFF".utf8); u32(UInt32(36 + dataSize))
        data.append(contentsOf: "WAVE".utf8)
        data.append(contentsOf: "fmt ".utf8); u32(16); u16(1); u16(1); u32(UInt32(sr)); u32(UInt32(byteRate)); u16(2); u16(16)
        data.append(contentsOf: "data".utf8); u32(UInt32(dataSize))
        pcm.withUnsafeBufferPointer { buf in
            data.append(Data(bytes: buf.baseAddress!, count: dataSize))
        }
        return data
    }
}