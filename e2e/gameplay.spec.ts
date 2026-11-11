import { expect, test } from "@playwright/test";
import { DEFAULT_DIFFICULTY } from "../src/domain/minesweeper";
import { simulateFirstClick } from "./support/simulateGame";

const SEED = 123;
const FIRST_CLICK = { row: 0, col: 0 };

test.describe("Minesweeper gameplay", () => {
  test("shows the start prompt before the first click", async ({ page }) => {
    await page.goto(`/?seed=${SEED}`);

    await expect(page.getByTestId("game-status")).toHaveText(
      "Haz click en una casilla para empezar.",
    );
    await expect(page.getByTestId("mines-remaining")).toHaveText(
      String(DEFAULT_DIFFICULTY.mines).padStart(3, "0"),
    );
  });

  test("the first click is always safe", async ({ page }) => {
    await page.goto(`/?seed=${SEED}`);

    await page.getByTestId(`cell-${FIRST_CLICK.row}-${FIRST_CLICK.col}`).click();

    await expect(page.getByTestId("game-status")).toHaveText(
      "Click izquierdo para revelar, click derecho para marcar.",
    );
    await expect(page.getByTestId(`cell-${FIRST_CLICK.row}-${FIRST_CLICK.col}`)).toHaveAttribute(
      "data-state",
      "revealed",
    );
  });

  test("right-clicking a hidden cell flags it and updates the mine counter", async ({ page }) => {
    await page.goto(`/?seed=${SEED}`);

    const cell = page.getByTestId("cell-8-8");
    await cell.click({ button: "right" });

    await expect(cell).toHaveAttribute("data-state", "flagged");
    await expect(page.getByTestId("mines-remaining")).toHaveText(
      String(DEFAULT_DIFFICULTY.mines - 1).padStart(3, "0"),
    );

    await cell.click({ button: "right" });
    await expect(cell).toHaveAttribute("data-state", "hidden");
  });

  test("switching difficulty rebuilds the board", async ({ page }) => {
    await page.goto(`/?seed=${SEED}`);

    await page.getByTestId("difficulty-expert").click();

    await expect(page.getByTestId("board").locator("button")).toHaveCount(16 * 30);
  });

  test("the reset button returns the game to ready status", async ({ page }) => {
    await page.goto(`/?seed=${SEED}`);

    await page.getByTestId(`cell-${FIRST_CLICK.row}-${FIRST_CLICK.col}`).click();
    await expect(page.getByTestId("game-status")).not.toHaveText(
      "Haz click en una casilla para empezar.",
    );

    await page.getByTestId("reset-button").click();

    await expect(page.getByTestId("game-status")).toHaveText(
      "Haz click en una casilla para empezar.",
    );
  });

  test("hitting a mine ends the game and reveals every mine", async ({ page }) => {
    const afterFirstClick = simulateFirstClick(DEFAULT_DIFFICULTY, SEED, FIRST_CLICK);
    const minePositions = afterFirstClick
      .flat()
      .map((cell, index) => ({
        cell,
        row: Math.floor(index / DEFAULT_DIFFICULTY.cols),
        col: index % DEFAULT_DIFFICULTY.cols,
      }))
      .filter(({ cell }) => cell.hasMine);

    await page.goto(`/?seed=${SEED}`);
    await page.getByTestId(`cell-${FIRST_CLICK.row}-${FIRST_CLICK.col}`).click();

    const [target] = minePositions;
    await page.getByTestId(`cell-${target.row}-${target.col}`).click();

    await expect(page.getByTestId("game-status")).toHaveText("Perdiste. Inténtalo de nuevo.");

    for (const { row, col } of minePositions) {
      await expect(page.getByTestId(`cell-${row}-${col}`)).toHaveAttribute("data-state", "revealed");
    }
  });

  test("revealing every safe cell wins the game", async ({ page }) => {
    await page.goto(`/?seed=${SEED}`);
    await page.getByTestId(`cell-${FIRST_CLICK.row}-${FIRST_CLICK.col}`).click();

    const afterFirstClick = simulateFirstClick(DEFAULT_DIFFICULTY, SEED, FIRST_CLICK);
    const safePositions = afterFirstClick
      .flat()
      .map((cell, index) => ({
        cell,
        row: Math.floor(index / DEFAULT_DIFFICULTY.cols),
        col: index % DEFAULT_DIFFICULTY.cols,
      }))
      .filter(({ cell }) => !cell.hasMine);

    for (const { row, col } of safePositions) {
      const locator = page.getByTestId(`cell-${row}-${col}`);
      const state = await locator.getAttribute("data-state");
      if (state === "hidden") {
        await locator.click();
      }
    }

    await expect(page.getByTestId("game-status")).toHaveText("¡Ganaste! 🎉");
  });
});
