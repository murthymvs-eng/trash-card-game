import AVFoundation

/// Procedural per-theme background (menu) and gameplay music.
/// Synthesizes a short loopable track per theme/mode and loops it via AVAudioPlayer.
@MainActor
final class MusicEngine {
    static let shared = MusicEngine()

    enum Mode { case menu, game }

    private enum Wave { case sine, triangle, square, sawtooth }
    private struct MusicSpec {
        let rootMidi: Int
        let minor: Bool
        let menuBPM: Double
        let gameBPM: Double
        let leadWave: Wave
        let progression: [Int]
    }

    private var muted = false
    private let sampleRate: Double = 44100
    private var cache: [String: AVAudioPlayer] = [:]
    private var current: AVAudioPlayer?
    private var currentKey: String?

    private init() {
        let s = AVAudioSession.sharedInstance()
        try? s.setCategory(.ambient, options: [.mixWithOthers])
        try? s.setActive(true)
    }

    func setMuted(_ m: Bool) {
        muted = m
        if m { current?.pause() } else { current?.play() }
    }

    func play(theme: String, mode: Mode) {
        let key = "\(theme)-\(mode == .menu ? "menu" : "game")"
        if key == currentKey, let cur = current {
            if !cur.isPlaying && !muted { cur.play() }
            return
        }
        current?.stop(); current = nil; currentKey = key
        guard !muted else { return }
        let player: AVAudioPlayer
        if let p = cache[key] { player = p }
        else if let p = makePlayer(theme: theme, mode: mode) { cache[key] = p; player = p }
        else { return }
        player.currentTime = 0
        player.numberOfLoops = -1
        player.volume = mode == .menu ? 0.42 : 0.5
        player.play()
        current = player
    }

    func stop() { current?.stop(); current = nil; currentKey = nil }

    private func makePlayer(theme: String, mode: Mode) -> AVAudioPlayer? {
        let m = mode == .menu ? "menu" : "game"
        // Prefer a bundled track. Accept a few naming patterns:
        //   music_<theme>_<menu|game>  per-mode track (e.g. user-supplied music)
        //   music_<theme>              one track used for both modes
        for th in [theme, fallbackTheme(theme)] {
            let bases = ["music_\(th)_\(m)", "music_\(th)", "\(th)_\(m)", "\(th)"]
            for base in bases {
                for ext in ["m4a", "mp3", "caf", "wav", "aiff"] {
                    if let url = Bundle.main.url(forResource: base, withExtension: ext),
                       let p = try? AVAudioPlayer(contentsOf: url) {
                        p.prepareToPlay()
                        print("[Music] bundled track: \(base).\(ext)")
                        return p
                    }
                }
            }
        }
        // Fallback: procedurally synthesized loop
        guard let samples = renderMusic(theme: theme, mode: mode), !samples.isEmpty,
              let data = wavData(samples), let p = try? AVAudioPlayer(data: data) else { return nil }
        p.prepareToPlay()
        print("[Music] synth fallback: \(theme) \(m)")
        return p
    }

    /// The SVG-only themes share the cheerful classic track.
    private func fallbackTheme(_ theme: String) -> String {
        switch theme {
        case "animal", "fairy", "neon", "wood": return "classic"
        default: return theme
        }
    }

    private func renderMusic(theme: String, mode: Mode) -> [Float]? {
        let spec = musicSpec(theme)
        let bpm = mode == .menu ? spec.menuBPM : spec.gameBPM
        let spb = 60.0 / bpm
        let bars = spec.progression.count
        guard bars > 0 else { return nil }
        let n = Int(Double(bars * 4) * spb * sampleRate)
        guard n > 0 else { return nil }
        var buf = [Float](repeating: 0, count: n)
        let third = spec.minor ? 3.0 : 4.0
        let chord = [0.0, third, 7.0, 12.0]
        for b in 0..<bars {
            let barStart = Int(Double(b) * 4 * spb * sampleRate)
            let rootMidi = Double(spec.rootMidi + spec.progression[b])
            addNote(&buf, start: barStart, dur: Int(4 * spb * sampleRate), midi: rootMidi - 12, wave: .triangle, amp: 0.16)
            let notesPerBar = mode == .menu ? 4 : 8
            let noteDur = Int((4 * spb / Double(notesPerBar)) * sampleRate)
            for k in 0..<notesPerBar {
                addNote(&buf, start: barStart + k * noteDur, dur: noteDur, midi: rootMidi + chord[k % chord.count], wave: spec.leadWave, amp: mode == .menu ? 0.09 : 0.12)
            }
            if mode == .game {
                for beat in 0..<4 { addPulse(&buf, start: barStart + Int(Double(beat) * spb * sampleRate)) }
            }
        }
        for i in 0..<buf.count { buf[i] = Float(tanh(Double(buf[i]) * 1.4)) }
        return buf
    }

    private func freq(_ midi: Double) -> Double { 440.0 * pow(2.0, (midi - 69.0) / 12.0) }

    private func addNote(_ buffer: inout [Float], start: Int, dur: Int, midi: Double, wave: Wave, amp: Double) {
        guard dur > 0 else { return }
        let f = freq(midi)
        for i in 0..<dur {
            let idx = start + i
            if idx < 0 { continue }
            if idx >= buffer.count { break }
            let t = Double(i) / sampleRate
            let phase = 2 * Double.pi * f * t
            let s: Double
            switch wave {
            case .sine: s = sin(phase)
            case .triangle: s = (2 / Double.pi) * asin(sin(phase))
            case .square: s = sin(phase) >= 0 ? 1 : -1
            case .sawtooth: s = 2 * ((f * t).truncatingRemainder(dividingBy: 1)) - 1
            }
            let attack = min(1.0, t / 0.012)
            let frac = Double(i) / Double(dur)
            buffer[idx] += Float(s * amp * attack * exp(-3.5 * frac))
        }
    }

    private func addPulse(_ buffer: inout [Float], start: Int) {
        let dur = Int(0.09 * sampleRate)
        for i in 0..<dur {
            let idx = start + i
            if idx < 0 { continue }
            if idx >= buffer.count { break }
            let t = Double(i) / sampleRate
            let f = 120.0 * exp(-16.0 * t) + 50
            buffer[idx] += Float(sin(2 * Double.pi * f * t) * exp(-28.0 * t) * 0.15)
        }
    }

    private func wavData(_ samples: [Float]) -> Data? {
        var pcm = [Int16](repeating: 0, count: samples.count)
        for i in 0..<samples.count { pcm[i] = Int16(max(-1, min(1, Double(samples[i]))) * 32767) }
        let sr = Int(sampleRate); let byteRate = sr * 2; let dataSize = pcm.count * 2
        var data = Data()
        func u32(_ v: UInt32) { var le = v.littleEndian; withUnsafeBytes(of: &le) { data.append(contentsOf: $0) } }
        func u16(_ v: UInt16) { var le = v.littleEndian; withUnsafeBytes(of: &le) { data.append(contentsOf: $0) } }
        data.append(contentsOf: "RIFF".utf8); u32(UInt32(36 + dataSize)); data.append(contentsOf: "WAVE".utf8)
        data.append(contentsOf: "fmt ".utf8); u32(16); u16(1); u16(1); u32(UInt32(sr)); u32(UInt32(byteRate)); u16(2); u16(16)
        data.append(contentsOf: "data".utf8); u32(UInt32(dataSize))
        pcm.withUnsafeBufferPointer { b in data.append(Data(bytes: b.baseAddress!, count: dataSize)) }
        return data
    }

    private func musicSpec(_ theme: String) -> MusicSpec {
        switch theme {
        case "classic":   return MusicSpec(rootMidi: 60, minor: false, menuBPM: 84, gameBPM: 108, leadWave: .triangle, progression: [0, 7, 9, 5])
        case "animal":    return MusicSpec(rootMidi: 62, minor: false, menuBPM: 96, gameBPM: 124, leadWave: .triangle, progression: [0, 5, 7, 5])
        case "minion":    return MusicSpec(rootMidi: 67, minor: false, menuBPM: 100, gameBPM: 132, leadWave: .square, progression: [0, 7, 9, 5])
        case "fairy":     return MusicSpec(rootMidi: 69, minor: true, menuBPM: 78, gameBPM: 96, leadWave: .triangle, progression: [0, 8, 3, 10])
        case "neon":      return MusicSpec(rootMidi: 69, minor: true, menuBPM: 104, gameBPM: 128, leadWave: .sawtooth, progression: [0, 3, 8, 10])
        case "wood":      return MusicSpec(rootMidi: 62, minor: false, menuBPM: 92, gameBPM: 112, leadWave: .triangle, progression: [0, 5, 9, 7])
        case "hp":        return MusicSpec(rootMidi: 64, minor: true, menuBPM: 80, gameBPM: 100, leadWave: .triangle, progression: [0, 8, 10, 3])
        case "avengers":  return MusicSpec(rootMidi: 60, minor: true, menuBPM: 96, gameBPM: 116, leadWave: .square, progression: [0, 3, 8, 10])
        case "starwars":  return MusicSpec(rootMidi: 62, minor: true, menuBPM: 88, gameBPM: 110, leadWave: .sawtooth, progression: [0, 5, 3, 7])
        case "spiderman": return MusicSpec(rootMidi: 65, minor: false, menuBPM: 108, gameBPM: 132, leadWave: .square, progression: [0, 7, 9, 5])
        case "coco":      return MusicSpec(rootMidi: 69, minor: true, menuBPM: 96, gameBPM: 120, leadWave: .triangle, progression: [0, 8, 3, 10])
        case "princess":  return MusicSpec(rootMidi: 65, minor: false, menuBPM: 84, gameBPM: 104, leadWave: .triangle, progression: [0, 5, 7, 9])
        case "taylor":    return MusicSpec(rootMidi: 67, minor: false, menuBPM: 104, gameBPM: 126, leadWave: .triangle, progression: [0, 9, 5, 7])
        case "moana":     return MusicSpec(rootMidi: 62, minor: false, menuBPM: 96, gameBPM: 118, leadWave: .triangle, progression: [0, 5, 9, 7])
        case "toystory":  return MusicSpec(rootMidi: 60, minor: false, menuBPM: 100, gameBPM: 126, leadWave: .square, progression: [0, 7, 5, 9])
        default:          return MusicSpec(rootMidi: 60, minor: false, menuBPM: 90, gameBPM: 110, leadWave: .triangle, progression: [0, 7, 9, 5])
        }
    }
}