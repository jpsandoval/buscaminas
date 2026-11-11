import re

import pytest
from playwright.sync_api import expect

SEED = 123
FIRST_CLICK = (0, 0)
DEFAULT_MINES = 10


def test_shows_the_start_prompt_before_the_first_click(page):
    page.goto(f"/?seed={SEED}")

    expect(page.get_by_test_id("game-status")).to_have_text(
        "Haz click en una casilla para empezar."
    )
    expect(page.get_by_test_id("mines-remaining")).to_have_text(str(DEFAULT_MINES).zfill(3))


def test_the_first_click_is_always_safe(page):
    page.goto(f"/?seed={SEED}")

    row, col = FIRST_CLICK
    page.get_by_test_id(f"cell-{row}-{col}").click()

    expect(page.get_by_test_id("game-status")).to_have_text(
        "Click izquierdo para revelar, click derecho para marcar."
    )
    expect(page.get_by_test_id(f"cell-{row}-{col}")).to_have_attribute("data-state", "revealed")


def test_right_clicking_a_hidden_cell_flags_it_and_updates_the_counter(page):
    page.goto(f"/?seed={SEED}")

    cell = page.get_by_test_id("cell-8-8")
    cell.click(button="right")

    expect(cell).to_have_attribute("data-state", "flagged")
    expect(page.get_by_test_id("mines-remaining")).to_have_text(str(DEFAULT_MINES - 1).zfill(3))

    cell.click(button="right")
    expect(cell).to_have_attribute("data-state", "hidden")


def test_switching_difficulty_rebuilds_the_board(page):
    page.goto(f"/?seed={SEED}")

    page.get_by_test_id("difficulty-expert").click()

    expect(page.get_by_test_id("board").locator("button")).to_have_count(16 * 30)


def test_the_reset_button_returns_the_game_to_ready_status(page):
    page.goto(f"/?seed={SEED}")

    row, col = FIRST_CLICK
    page.get_by_test_id(f"cell-{row}-{col}").click()
    expect(page.get_by_test_id("game-status")).not_to_have_text(
        "Haz click en una casilla para empezar."
    )

    page.get_by_test_id("reset-button").click()

    expect(page.get_by_test_id("game-status")).to_have_text("Haz click en una casilla para empezar.")


def _mine_positions(page):
    """Reads the current board back through the same session-bound API the
    page itself uses, to discover the mine layout without duplicating the
    placement algorithm in the test."""
    row, col = FIRST_CLICK
    response = page.context.request.post(
        "/api/reveal", data={"row": row, "col": col}
    )
    board = response.json()["board"]
    return [
        (r, c)
        for r, cells in enumerate(board)
        for c, cell in enumerate(cells)
        if cell["hasMine"]
    ]


def test_hitting_a_mine_ends_the_game_and_reveals_every_mine(page):
    page.goto(f"/?seed={SEED}")
    row, col = FIRST_CLICK
    with page.expect_response(re.compile(r"/api/reveal$")):
        page.get_by_test_id(f"cell-{row}-{col}").click()

    mine_positions = _mine_positions(page)
    target_row, target_col = mine_positions[0]
    page.get_by_test_id(f"cell-{target_row}-{target_col}").click()

    expect(page.get_by_test_id("game-status")).to_have_text("Perdiste. Inténtalo de nuevo.")

    for r, c in mine_positions:
        expect(page.get_by_test_id(f"cell-{r}-{c}")).to_have_attribute("data-state", "revealed")


def test_revealing_every_safe_cell_wins_the_game(page):
    page.goto(f"/?seed={SEED}")
    row, col = FIRST_CLICK
    with page.expect_response(re.compile(r"/api/reveal$")):
        page.get_by_test_id(f"cell-{row}-{col}").click()

    mine_positions = set(_mine_positions(page))
    rows, cols = 9, 9
    safe_positions = [
        (r, c) for r in range(rows) for c in range(cols) if (r, c) not in mine_positions
    ]

    for r, c in safe_positions:
        locator = page.get_by_test_id(f"cell-{r}-{c}")
        if locator.get_attribute("data-state") == "hidden":
            # Reveals round-trip through /api/reveal; wait for that response
            # (and the render it triggers) before checking the next cell, or
            # a flood-reveal from this click can race the next iteration's check.
            with page.expect_response(re.compile(r"/api/reveal$")):
                locator.click()

    expect(page.get_by_test_id("game-status")).to_have_text("¡Ganaste! 🎉")
