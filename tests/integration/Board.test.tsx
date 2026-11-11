import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { Board } from "../../src/ui/components/Board/Board";
import { createEmptyBoard } from "../../src/domain/minesweeper";

describe("Board", () => {
  it("renders one cell button per board position", () => {
    const board = createEmptyBoard(2, 3);
    render(<Board board={board} disabled={false} onReveal={vi.fn()} onToggleFlag={vi.fn()} />);

    expect(screen.getAllByRole("button")).toHaveLength(6);
  });

  it("calls onReveal with the clicked position", async () => {
    const user = userEvent.setup();
    const board = createEmptyBoard(2, 2);
    const onReveal = vi.fn();

    render(<Board board={board} disabled={false} onReveal={onReveal} onToggleFlag={vi.fn()} />);

    await user.click(screen.getByTestId("cell-1-0"));

    expect(onReveal).toHaveBeenCalledWith({ row: 1, col: 0 });
  });

  it("calls onToggleFlag on right click instead of revealing", () => {
    const board = createEmptyBoard(2, 2);
    const onReveal = vi.fn();
    const onToggleFlag = vi.fn();

    render(<Board board={board} disabled={false} onReveal={onReveal} onToggleFlag={onToggleFlag} />);

    fireEvent.contextMenu(screen.getByTestId("cell-0-1"));

    expect(onToggleFlag).toHaveBeenCalledWith({ row: 0, col: 1 });
    expect(onReveal).not.toHaveBeenCalled();
  });

  it("displays the adjacent mine count on a revealed cell", () => {
    const board = createEmptyBoard(1, 1);
    board[0][0].state = "revealed";
    board[0][0].adjacentMines = 3;

    render(<Board board={board} disabled={false} onReveal={vi.fn()} onToggleFlag={vi.fn()} />);

    expect(screen.getByTestId("cell-0-0")).toHaveTextContent("3");
  });

  it("disables every cell when the board is disabled", async () => {
    const user = userEvent.setup();
    const board = createEmptyBoard(1, 1);
    const onReveal = vi.fn();

    render(<Board board={board} disabled={true} onReveal={onReveal} onToggleFlag={vi.fn()} />);

    await user.click(screen.getByTestId("cell-0-0"));

    expect(onReveal).not.toHaveBeenCalled();
  });
});
