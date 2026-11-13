//
//  TrashGameUITests.swift
//  TrashGameUITests
//
//  Created by Murthy Manchiraju on 11/11/26.
//

import XCTest

final class TrashGameUITests: XCTestCase {

    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    /// Smoke test: launch → start screen → tap "1 Player" → game board appears.
    @MainActor
    func testStartOnePlayerGameShowsBoard() throws {
        let app = XCUIApplication()
        app.launch()

        let onePlayer = app.buttons["1 Player"]
        XCTAssertTrue(onePlayer.waitForExistence(timeout: 8), "Start screen should show a 1 Player button")
        onePlayer.tap()

        let banner = app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'Your turn'")).firstMatch
        XCTAssertTrue(banner.waitForExistence(timeout: 5), "Game board should prompt the player to draw")
    }

    /// The in-game exit chip must return to the main screen.
    @MainActor
    func testExitButtonReturnsToMainScreen() throws {
        let app = XCUIApplication()
        app.launch()

        let onePlayer = app.buttons["1 Player"]
        XCTAssertTrue(onePlayer.waitForExistence(timeout: 10), "Start screen should show a 1 Player button")
        onePlayer.tap()

        let banner = app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'Your turn'")).firstMatch
        XCTAssertTrue(banner.waitForExistence(timeout: 8), "Game board should be on screen")

        let exit = app.descendants(matching: .any).matching(identifier: "exit-button").firstMatch
        guard exit.waitForExistence(timeout: 5) else {
            XCTFail("Exit button not found in the hierarchy:\n\(app.debugDescription)")
            return
        }
        print("DIAG exit frame=\(exit.frame) hittable=\(exit.isHittable) label=\(exit.label)")
        print("DIAG app frame=\(app.frame)")
        XCTAssertTrue(exit.isHittable, "Exit button should be tappable")
        exit.tap()

        if !onePlayer.waitForExistence(timeout: 4) {
            print("DIAG after tap:\n\(app.debugDescription)")
        }
        XCTAssertTrue(onePlayer.waitForExistence(timeout: 6), "Should be back on the main screen")
    }

    /// Drag the drawn card onto the matching slot with a single finger movement
    /// (no long press) and verify it lands.
    @MainActor
    func testDragCardOntoSlot() throws {
        let app = XCUIApplication()
        // Force the drawn card so the test is deterministic.
        app.launchArguments = ["-forceCard", "4"]
        app.launch()

        let onePlayer = app.buttons["1 Player"]
        XCTAssertTrue(onePlayer.waitForExistence(timeout: 10), "Start screen should show a 1 Player button")
        onePlayer.tap()

        let ourTurn = app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'Your turn'")).firstMatch
        XCTAssertTrue(ourTurn.waitForExistence(timeout: 8), "Game board should prompt the player to draw")

        let deck = app.descendants(matching: .any)
            .matching(NSPredicate(format: "label BEGINSWITH 'Deck'")).firstMatch
        XCTAssertTrue(deck.waitForExistence(timeout: 8), "Deck pile should be on the board")

        let card = app.descendants(matching: .any).matching(identifier: "hand-card").firstMatch
        deck.tap()
        XCTAssertTrue(card.waitForExistence(timeout: 8), "The forced card should be in hand")

        // The slot that accepts this card: same rank (a Jack may go anywhere).
        let rank = card.label.split(separator: " ").first.map(String.init) ?? "A"
        let target: XCUIElement
        if rank == "J" {
            target = app.descendants(matching: .any).matching(identifier: "slot-0-0").firstMatch
        } else {
            let wanted = "Empty slot for \(rank)"
            let slot = app.descendants(matching: .any)
                .matching(NSPredicate(format: "identifier BEGINSWITH 'slot-0-' AND label == %@", wanted))
                .firstMatch
            XCTAssertTrue(slot.waitForExistence(timeout: 5), "No slot for a \(rank)")
            target = slot
        }

        // Drag the card onto the slot with one continuous finger movement —
        // no long press required.
        card.press(forDuration: 0.05, thenDragTo: target)

        // The card must now be sitting in that slot.
        let filled = NSPredicate(format: "NOT (label BEGINSWITH 'Empty slot')")
        expectation(for: filled, evaluatedWith: target)
        waitForExpectations(timeout: 8)
    }

    /// The in-game Settings chip opens the settings sheet, where the theme can
    /// be switched without leaving the game.
    @MainActor
    func testInGameSettingsChipOffersThemeAndStartOver() throws {
        let app = XCUIApplication()
        app.launch()

        let onePlayer = app.buttons["1 Player"]
        XCTAssertTrue(onePlayer.waitForExistence(timeout: 8), "Start screen should show a 1 Player button")
        onePlayer.tap()

        let banner = app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'Your turn'")).firstMatch
        XCTAssertTrue(banner.waitForExistence(timeout: 8), "Game board should be on screen")

        let settings = app.descendants(matching: .any).matching(identifier: "settings-button").firstMatch
        XCTAssertTrue(settings.waitForExistence(timeout: 5), "Settings chip should be visible in game")
        settings.tap()

        // Both in-game actions are offered: the theme picker and Start Over.
        let themeHeader = app.staticTexts["Card theme"]
        XCTAssertTrue(themeHeader.waitForExistence(timeout: 5), "Theme picker should be offered")
        let startOver = app.buttons["Start Over"]
        XCTAssertTrue(startOver.waitForExistence(timeout: 5), "Start Over should be offered in game")

        // Switch the theme mid-game and leave the sheet back to the board.
        let neonTile = app.buttons["Neon Night"]
        XCTAssertTrue(neonTile.waitForExistence(timeout: 5), "Theme tiles should be visible")
        neonTile.tap()

        let done = app.buttons["Done"]
        XCTAssertTrue(done.waitForExistence(timeout: 5), "Done should close the sheet")
        done.tap()

        XCTAssertTrue(banner.waitForExistence(timeout: 5), "The game should still be on screen")
    }

    /// Start Over from the in-game settings resets the game (full deck again)
    /// and keeps the player ready for a fresh turn.
    @MainActor
    func testStartOverResetsGame() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-forceCard", "4"]
        app.launch()

        let onePlayer = app.buttons["1 Player"]
        XCTAssertTrue(onePlayer.waitForExistence(timeout: 10), "Start screen should show a 1 Player button")
        onePlayer.tap()

        let banner = app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'Your turn'")).firstMatch
        XCTAssertTrue(banner.waitForExistence(timeout: 8), "Game board should be on screen")

        // Draw a card so the deck is no longer full.
        let fullDeck = app.descendants(matching: .any).matching(NSPredicate(format: "label == 'Deck, 52 cards'")).firstMatch
        XCTAssertTrue(fullDeck.waitForExistence(timeout: 8), "The deck should start full")
        fullDeck.tap()
        let hand = app.descendants(matching: .any).matching(identifier: "hand-card").firstMatch
        XCTAssertTrue(hand.waitForExistence(timeout: 8), "The forced card should be in hand")
        let deck51 = app.descendants(matching: .any).matching(NSPredicate(format: "label == 'Deck, 51 cards'")).firstMatch
        XCTAssertTrue(deck51.waitForExistence(timeout: 5), "The deck should be down to 51 after the draw")

        // Start over from the in-game settings.
        let settings = app.descendants(matching: .any).matching(identifier: "settings-button").firstMatch
        XCTAssertTrue(settings.waitForExistence(timeout: 5), "Settings chip should be visible in game")
        settings.tap()
        let startOver = app.buttons["Start Over"]
        XCTAssertTrue(startOver.waitForExistence(timeout: 5), "Start Over should be offered in game")
        startOver.tap()

        XCTAssertTrue(banner.waitForExistence(timeout: 5), "The game should be ready for a fresh turn")
        let resetDeck = app.descendants(matching: .any).matching(NSPredicate(format: "label == 'Deck, 52 cards'")).firstMatch
        XCTAssertTrue(resetDeck.waitForExistence(timeout: 5), "Start Over should reset the deck to full")
    }
}
