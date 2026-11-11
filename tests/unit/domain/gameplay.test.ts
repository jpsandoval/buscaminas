import { describe, expect, it } from "vitest";
import { createEmptyBoard } from "../../../src/domain/minesweeper/board";
import {
  countFlags,
  hasWon,
  revealAllMines,
  revealCell,
  toggleFlag,
} from "../../../src/domain/minesweeper/gameplay";

describe("revealCell", () => {
  it("reveals a single cell with adjacent mines without flooding", () => {
    const board = createEmptyBoard(3, 3);
    board[0][0].hasMine = true;
    board[0][1].adjacentMines = 1;

    const { board: result, hitMine } = revealCell(board, { row: 0, col: 1 });

    expect(hitMine).toBe(false);
    expect(result[0][1].state).toBe("revealed");
    expect(result[1][1].state).toBe("hidden");
  });

  it("floods outward through connected zero cells", () => {
    const board = createEmptyBoard(3, 3);
    board[0][0].hasMine = true;
    board[0][1].adjacentMines = 1;
    board[1][0].adjacentMines = 1;
    // every other cell has 0 adjacent mines and should be revealed by the flood

    const { board: result, hitMine } = revealCell(board, { row: 2, col: 2 });

    expect(hitMine).toBe(false);
    expect(result[2][2].state).toBe("revealed");
    expect(result[1][1].state).toBe("revealed");
    expect(result[0][1].state).toBe("revealed");
    expect(result[1][0].state).toBe("revealed");
    expect(result[0][0].state).toBe("hidden");
  });

  it("reports hitMine and reveals only the mine when a mine is clicked", () => {
    const board = createEmptyBoard(2, 2);
    board[1][1].hasMine = true;

    const { board: result, hitMine } = revealCell(board, { row: 1, col: 1 });

    expect(hitMine).toBe(true);
    expect(result[1][1].state).toBe("revealed");
    expect(result[0][0].state).toBe("hidden");
  });

  it("does nothing when the cell is already revealed or flagged", () => {
    const board = createEmptyBoard(2, 2);
    board[0][0].state = "revealed";
    board[0][1].state = "flagged";

    expect(revealCell(board, { row: 0, col: 0 }).board[0][0].state).toBe("revealed");
    expect(revealCell(board, { row: 0, col: 1 }).board[0][1].state).toBe("flagged");
  });
});

describe("toggleFlag", () => {
  it("flags a hidden cell and unflags it back", () => {
    const board = createEmptyBoard(2, 2);

    const flagged = toggleFlag(board, { row: 0, col: 0 });
    expect(flagged[0][0].state).toBe("flagged");

    const unflagged = toggleFlag(flagged, { row: 0, col: 0 });
    expect(unflagged[0][0].state).toBe("hidden");
  });

  it("does not flag an already revealed cell", () => {
    const board = createEmptyBoard(2, 2);
    board[0][0].state = "revealed";

    const result = toggleFlag(board, { row: 0, col: 0 });
    expect(result[0][0].state).toBe("revealed");
  });
});

describe("revealAllMines", () => {
  it("reveals every mine, leaving other cells untouched", () => {
    const board = createEmptyBoard(2, 2);
    board[0][0].hasMine = true;
    board[1][1].hasMine = true;

    const result = revealAllMines(board);

    expect(result[0][0].state).toBe("revealed");
    expect(result[1][1].state).toBe("revealed");
    expect(result[0][1].state).toBe("hidden");
  });
});

describe("countFlags", () => {
  it("counts flagged cells only", () => {
    const board = createEmptyBoard(2, 2);
    board[0][0].state = "flagged";
    board[0][1].state = "flagged";
    board[1][0].state = "revealed";

    expect(countFlags(board)).toBe(2);
  });
});

describe("hasWon", () => {
  it("is false while a non-mine cell remains hidden", () => {
    const board = createEmptyBoard(2, 2);
    board[0][0].hasMine = true;
    board[0][1].state = "revealed";
    board[1][0].state = "revealed";
    // board[1][1] stays hidden

    expect(hasWon(board)).toBe(false);
  });

  it("is true once every non-mine cell is revealed, mines untouched", () => {
    const board = createEmptyBoard(2, 2);
    board[0][0].hasMine = true;
    board[0][1].state = "revealed";
    board[1][0].state = "revealed";
    board[1][1].state = "revealed";

    expect(hasWon(board)).toBe(true);
  });
});
