import { cloneBoard, getNeighborPositions } from "./board";
import type { Board, Position } from "./types";

export interface RevealOutcome {
  board: Board;
  hitMine: boolean;
}

/**
 * Reveals a cell. If it has no adjacent mines, floods outward revealing
 * every connected zero-cell and its bordering numbered cells.
 */
export function revealCell(board: Board, position: Position): RevealOutcome {
  const cell = board[position.row][position.col];

  if (cell.state !== "hidden") {
    return { board, hitMine: false };
  }

  const nextBoard = cloneBoard(board);

  if (cell.hasMine) {
    nextBoard[position.row][position.col].state = "revealed";
    return { board: nextBoard, hitMine: true };
  }

  floodReveal(nextBoard, position);
  return { board: nextBoard, hitMine: false };
}

function floodReveal(board: Board, start: Position): void {
  const rows = board.length;
  const cols = board[0]?.length ?? 0;
  const pending: Position[] = [start];

  while (pending.length > 0) {
    const position = pending.pop();
    if (!position) continue;

    const cell = board[position.row][position.col];
    if (cell.state !== "hidden" || cell.hasMine) continue;

    cell.state = "revealed";

    if (cell.adjacentMines === 0) {
      pending.push(...getNeighborPositions(position, rows, cols));
    }
  }
}

export function toggleFlag(board: Board, position: Position): Board {
  const cell = board[position.row][position.col];
  if (cell.state === "revealed") return board;

  const nextBoard = cloneBoard(board);
  nextBoard[position.row][position.col].state =
    cell.state === "flagged" ? "hidden" : "flagged";
  return nextBoard;
}

export function revealAllMines(board: Board): Board {
  const nextBoard = cloneBoard(board);
  for (const row of nextBoard) {
    for (const cell of row) {
      if (cell.hasMine) cell.state = "revealed";
    }
  }
  return nextBoard;
}

export function countFlags(board: Board): number {
  return board.flat().filter((cell) => cell.state === "flagged").length;
}

/** The player wins once every non-mine cell has been revealed. */
export function hasWon(board: Board): boolean {
  return board.flat().every((cell) => cell.hasMine || cell.state === "revealed");
}
