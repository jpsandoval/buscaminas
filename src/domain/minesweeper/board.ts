import type { Board, Cell, Position, RandomSource } from "./types";

export function createEmptyBoard(rows: number, cols: number): Board {
  return Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => createEmptyCell()),
  );
}

function createEmptyCell(): Cell {
  return { hasMine: false, adjacentMines: 0, state: "hidden" };
}

export function cloneBoard(board: Board): Board {
  return board.map((row) => row.map((cell) => ({ ...cell })));
}

export function getNeighborPositions(
  position: Position,
  rows: number,
  cols: number,
): Position[] {
  const neighbors: Position[] = [];

  for (let deltaRow = -1; deltaRow <= 1; deltaRow++) {
    for (let deltaCol = -1; deltaCol <= 1; deltaCol++) {
      if (deltaRow === 0 && deltaCol === 0) continue;

      const row = position.row + deltaRow;
      const col = position.col + deltaCol;

      if (row >= 0 && row < rows && col >= 0 && col < cols) {
        neighbors.push({ row, col });
      }
    }
  }

  return neighbors;
}

/**
 * Places mines on the board, keeping `safePosition` and its neighbors mine-free
 * so the player's first click always opens a safe area.
 */
export function placeMines(
  board: Board,
  mineCount: number,
  safePosition: Position,
  random: RandomSource = Math.random,
): Board {
  const rows = board.length;
  const cols = board[0]?.length ?? 0;
  const candidates = findMineCandidates(rows, cols, safePosition, mineCount);

  const minePositions = new Set(
    shuffle(candidates, random)
      .slice(0, Math.min(mineCount, candidates.length))
      .map(toKey),
  );

  const nextBoard = cloneBoard(board);
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      nextBoard[row][col].hasMine = minePositions.has(toKey({ row, col }));
    }
  }

  return calculateAdjacentMines(nextBoard);
}

export function calculateAdjacentMines(board: Board): Board {
  const rows = board.length;
  const cols = board[0]?.length ?? 0;
  const nextBoard = cloneBoard(board);

  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      if (nextBoard[row][col].hasMine) continue;

      const neighbors = getNeighborPositions({ row, col }, rows, cols);
      nextBoard[row][col].adjacentMines = neighbors.filter(
        (neighbor) => nextBoard[neighbor.row][neighbor.col].hasMine,
      ).length;
    }
  }

  return nextBoard;
}

/**
 * Candidate cells for mines, excluding `safePosition` and its neighbors so
 * the first click opens a safe area. Falls back to excluding only
 * `safePosition` itself when the board is too small to spare the whole
 * neighborhood and still fit every requested mine.
 */
function findMineCandidates(
  rows: number,
  cols: number,
  safePosition: Position,
  mineCount: number,
): Position[] {
  const withNeighborsExcluded = positionsExcluding(
    rows,
    cols,
    new Set([safePosition, ...getNeighborPositions(safePosition, rows, cols)].map(toKey)),
  );

  if (withNeighborsExcluded.length >= mineCount) {
    return withNeighborsExcluded;
  }

  return positionsExcluding(rows, cols, new Set([toKey(safePosition)]));
}

function positionsExcluding(rows: number, cols: number, excluded: Set<string>): Position[] {
  const positions: Position[] = [];
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      if (!excluded.has(toKey({ row, col }))) {
        positions.push({ row, col });
      }
    }
  }
  return positions;
}

function toKey(position: Position): string {
  return `${position.row}:${position.col}`;
}

function shuffle<T>(items: T[], random: RandomSource): T[] {
  const result = [...items];

  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }

  return result;
}
