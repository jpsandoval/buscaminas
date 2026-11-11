import { describe, expect, it } from "vitest";
import {
  calculateAdjacentMines,
  createEmptyBoard,
  getNeighborPositions,
  placeMines,
} from "../../../src/domain/minesweeper/board";

describe("createEmptyBoard", () => {
  it("creates a board with the given dimensions, all cells hidden and mine-free", () => {
    const board = createEmptyBoard(3, 4);

    expect(board).toHaveLength(3);
    expect(board[0]).toHaveLength(4);
    for (const row of board) {
      for (const cell of row) {
        expect(cell).toEqual({ hasMine: false, adjacentMines: 0, state: "hidden" });
      }
    }
  });
});

describe("getNeighborPositions", () => {
  it("returns all 8 neighbors for a cell in the middle of the board", () => {
    const neighbors = getNeighborPositions({ row: 1, col: 1 }, 3, 3);
    expect(neighbors).toHaveLength(8);
  });

  it("excludes out-of-bounds positions for a corner cell", () => {
    const neighbors = getNeighborPositions({ row: 0, col: 0 }, 3, 3);
    expect(neighbors).toHaveLength(3);
    expect(neighbors).toEqual(
      expect.arrayContaining([
        { row: 0, col: 1 },
        { row: 1, col: 0 },
        { row: 1, col: 1 },
      ]),
    );
  });
});

describe("placeMines", () => {
  it("places exactly the requested number of mines", () => {
    const board = createEmptyBoard(5, 5);
    const result = placeMines(board, 6, { row: 0, col: 0 });

    const mineCount = result.flat().filter((cell) => cell.hasMine).length;
    expect(mineCount).toBe(6);
  });

  it("never places a mine on the safe position or its neighbors", () => {
    const board = createEmptyBoard(5, 5);
    const safePosition = { row: 2, col: 2 };
    // Fill almost the whole board with mines to stress-test the safe zone.
    const result = placeMines(board, 16, safePosition);

    const safeZone = [safePosition, ...getNeighborPositions(safePosition, 5, 5)];
    for (const position of safeZone) {
      expect(result[position.row][position.col].hasMine).toBe(false);
    }
  });

  it("is deterministic given the same random source", () => {
    const board = createEmptyBoard(5, 5);
    const fixedRandom = sequence([0.1, 0.9, 0.3, 0.5, 0.7, 0.2]);
    const anotherFixedRandom = sequence([0.1, 0.9, 0.3, 0.5, 0.7, 0.2]);

    const first = placeMines(board, 5, { row: 0, col: 0 }, fixedRandom);
    const second = placeMines(board, 5, { row: 0, col: 0 }, anotherFixedRandom);

    expect(first).toEqual(second);
  });
});

describe("calculateAdjacentMines", () => {
  it("counts how many mines surround each non-mine cell", () => {
    const board = createEmptyBoard(3, 3);
    board[0][0].hasMine = true;
    board[2][2].hasMine = true;

    const result = calculateAdjacentMines(board);

    expect(result[0][1].adjacentMines).toBe(1);
    expect(result[1][0].adjacentMines).toBe(1);
    expect(result[1][1].adjacentMines).toBe(2);
    expect(result[1][2].adjacentMines).toBe(1);
    expect(result[2][1].adjacentMines).toBe(1);
    expect(result[0][2].adjacentMines).toBe(0);
  });
});

function sequence(values: number[]): () => number {
  let index = 0;
  return () => values[index++ % values.length];
}
