import UIKit

/// Lightweight haptic feedback helpers (no-op on unsupported platforms).
enum Haptics {
    static func tap() { UIImpactFeedbackGenerator(style: .light).impactOccurred() }
    static func place() { UIImpactFeedbackGenerator(style: .medium).impactOccurred() }
    static func discard() { UIImpactFeedbackGenerator(style: .soft).impactOccurred() }
    static func error() { UINotificationFeedbackGenerator().notificationOccurred(.error) }
    static func win() { UINotificationFeedbackGenerator().notificationOccurred(.success) }
}