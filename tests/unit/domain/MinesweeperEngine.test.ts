import { describe, expect, it } from "vitest";
import { MinesweeperEngine } from "../../../src/domain/minesweeper/MinesweeperEngine";
import type { Difficulty, MinesweeperState, Position } from "../../../src/domain/minesweeper/types";

const TINY_DIFFICULTY: Difficulty = { id: "tiny", label: "Tiny", rows: 3, cols: 3, mines: 1 };

function alwaysReturn(value: number): () => number {
  return () => value;
}

function findMinePosition(state: MinesweeperState): Position {
  for (let row = 0; row < state.board.length; row++) {
    for (let col = 0; col < state.board[row].length; col++) {
      if (state.board[row][col].hasMine) return { row, col };
    }
  }
  throw new Error("No mine found on board");
}

function allPositions(state: MinesweeperState): Position[] {
  const positions: Position[] = [];
  for (let row = 0; row < state.board.length; row++) {
    for (let col = 0; col < state.board[row].length; col++) {
      positions.push({ row, col });
    }
  }
  return positions;
}

describe("MinesweeperEngine", () => {
  it("starts in ready status with no mines placed on an untouched board", () => {
    const engine = new MinesweeperEngine(TINY_DIFFICULTY);
    const state = engine.getState();

    expect(state.status).toBe("ready");
    expect(state.minesRemaining).toBe(1);
    expect(state.board.flat().every((cell) => !cell.hasMine)).toBe(true);
  });

  it("places mines only after the first reveal, keeping that cell safe", () => {
    const engine = new MinesweeperEngine(TINY_DIFFICULTY, alwaysReturn(0));

    const state = engine.reveal({ row: 1, col: 1 });

    expect(state.status).toBe("playing");
    expect(state.board[1][1].hasMine).toBe(false);
    expect(state.board.flat().filter((cell) => cell.hasMine)).toHaveLength(1);
  });

  it("transitions to lost and reveals every mine when a mine is clicked", () => {
    const engine = new MinesweeperEngine(TINY_DIFFICULTY, alwaysReturn(0));

    const afterFirstClick = engine.reveal({ row: 0, col: 0 });
    const minePosition = findMinePosition(afterFirstClick);

    const state = engine.reveal(minePosition);

    expect(state.status).toBe("lost");
    expect(state.board[minePosition.row][minePosition.col].state).toBe("revealed");
  });

  it("transitions to won once all non-mine cells are revealed", () => {
    const engine = new MinesweeperEngine(TINY_DIFFICULTY, alwaysReturn(0));

    const afterFirstClick = engine.reveal({ row: 0, col: 0 });
    const minePosition = findMinePosition(afterFirstClick);
    const remainingPositions = allPositions(afterFirstClick).filter(
      (position) => !(position.row === minePosition.row && position.col === minePosition.col),
    );

    let state = afterFirstClick;
    for (const position of remainingPositions) {
      if (state.board[position.row][position.col].state === "hidden") {
        state = engine.reveal(position);
      }
    }

    expect(state.status).toBe("won");
  });

  it("ignores reveals and flag toggles once the game has ended", () => {
    const engine = new MinesweeperEngine(TINY_DIFFICULTY, alwaysReturn(0));

    const afterFirstClick = engine.reveal({ row: 0, col: 0 });
    const minePosition = findMinePosition(afterFirstClick);
    const lostState = engine.reveal(minePosition);
    expect(lostState.status).toBe("lost");

    const afterExtraReveal = engine.reveal({ row: 0, col: 0 });
    const afterExtraFlag = engine.toggleFlag({ row: 0, col: 0 });

    expect(afterExtraReveal).toEqual(lostState);
    expect(afterExtraFlag).toEqual(lostState);
  });

  it("tracks flags placed and mines remaining", () => {
    const engine = new MinesweeperEngine(TINY_DIFFICULTY, alwaysReturn(0));

    const state = engine.toggleFlag({ row: 0, col: 0 });

    expect(state.flagsPlaced).toBe(1);
    expect(state.minesRemaining).toBe(0);
  });

  it("does not reveal a flagged cell", () => {
    const engine = new MinesweeperEngine(TINY_DIFFICULTY, alwaysReturn(0));

    engine.toggleFlag({ row: 1, col: 1 });
    const state = engine.reveal({ row: 1, col: 1 });

    expect(state.board[1][1].state).toBe("flagged");
    expect(state.status).toBe("ready");
  });
});
