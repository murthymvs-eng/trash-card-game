import SwiftUI

/// Loads a bundled image by resource name (searches bundle root; nil if missing).
func bundleImage(_ name: String, ext: String = "jpg") -> UIImage? {
    Bundle.main.url(forResource: name, withExtension: ext).flatMap { UIImage(contentsOfFile: $0.path) }
}

/// Face-up playing card.
struct CardFaceView: View {
    let card: Card
    let theme: Theme

    var body: some View {
        Group {
            if case .image(let dir) = theme.face, let img = bundleImage("\(dir)_\(card.suit.fileName)_\(card.rank)") {
                Image(uiImage: img).resizable()
            } else {
                // Image deck not present yet -> fall back to the drawn classic face.
                NativeCardFace(card: card, style: .classic)
            }
        }
        .aspectRatio(5.0 / 7.0, contentMode: .fit)
        .clipShape(RoundedRectangle(cornerRadius: 5, style: .continuous))
    }
}

/// Card back (per-theme JPEG with a drawn fallback).
struct CardBackView: View {
    let theme: Theme

    var body: some View {
        Group {
            if let img = bundleImage("back_\(theme.id)") {
                Image(uiImage: img).resizable()
            } else {
                DrawnBack(theme: theme)
            }
        }
        .aspectRatio(5.0 / 7.0, contentMode: .fit)
        .clipShape(RoundedRectangle(cornerRadius: 5, style: .continuous))
    }
}

/// Simple drawn card back used when a theme's JPEG is missing.
struct DrawnBack: View {
    let theme: Theme

    var body: some View {
        GeometryReader { geo in
            let w = geo.size.width
            ZStack {
                LinearGradient(colors: [theme.accentDeep, theme.accentDeep.opacity(0.65)],
                               startPoint: .topLeading, endPoint: .bottomTrailing)
                RoundedRectangle(cornerRadius: w * 0.06)
                    .strokeBorder(theme.accent, lineWidth: w * 0.045)
                    .padding(w * 0.07)
                Text("🗑️").font(.system(size: w * 0.5))
            }
        }
    }
}