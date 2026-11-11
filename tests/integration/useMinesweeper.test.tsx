import { act, renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { useMinesweeper } from "../../src/application/useMinesweeper";
import type { Difficulty } from "../../src/domain/minesweeper";

const TINY_DIFFICULTY: Difficulty = { id: "tiny", label: "Tiny", rows: 3, cols: 3, mines: 1 };

function alwaysReturn(value: number): () => number {
  return () => value;
}

describe("useMinesweeper", () => {
  it("starts ready and moves to playing after revealing a cell", () => {
    const { result } = renderHook(() =>
      useMinesweeper(TINY_DIFFICULTY, { randomSource: alwaysReturn(0) }),
    );

    expect(result.current.state.status).toBe("ready");

    act(() => {
      result.current.reveal({ row: 0, col: 0 });
    });

    expect(result.current.state.status).toBe("playing");
  });

  it("toggles a flag and updates minesRemaining", () => {
    const { result } = renderHook(() =>
      useMinesweeper(TINY_DIFFICULTY, { randomSource: alwaysReturn(0) }),
    );

    act(() => {
      result.current.toggleFlag({ row: 0, col: 0 });
    });

    expect(result.current.state.board[0][0].state).toBe("flagged");
    expect(result.current.state.minesRemaining).toBe(0);

    act(() => {
      result.current.toggleFlag({ row: 0, col: 0 });
    });

    expect(result.current.state.board[0][0].state).toBe("hidden");
    expect(result.current.state.minesRemaining).toBe(1);
  });

  it("resets the game to a fresh ready state", () => {
    const { result } = renderHook(() =>
      useMinesweeper(TINY_DIFFICULTY, { randomSource: alwaysReturn(0) }),
    );

    act(() => {
      result.current.reveal({ row: 0, col: 0 });
    });
    expect(result.current.state.status).toBe("playing");

    act(() => {
      result.current.reset();
    });

    expect(result.current.state.status).toBe("ready");
    expect(result.current.elapsedSeconds).toBe(0);
    expect(result.current.state.board.flat().every((cell) => cell.state === "hidden")).toBe(true);
  });

  it("switches difficulty on reset and rebuilds the board accordingly", () => {
    const { result } = renderHook(() =>
      useMinesweeper(TINY_DIFFICULTY, { randomSource: alwaysReturn(0) }),
    );

    const biggerDifficulty: Difficulty = { id: "bigger", label: "Bigger", rows: 5, cols: 5, mines: 3 };

    act(() => {
      result.current.reset(biggerDifficulty);
    });

    expect(result.current.state.difficulty).toEqual(biggerDifficulty);
    expect(result.current.state.board).toHaveLength(5);
    expect(result.current.state.board[0]).toHaveLength(5);
  });
});
