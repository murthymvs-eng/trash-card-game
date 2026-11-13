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
}
