import {
  createEmptyBoard,
  createSeededRandomSource,
  placeMines,
  revealCell,
  type Board,
  type Difficulty,
  type Position,
} from "../../src/domain/minesweeper";

/**
 * Mirrors exactly what MinesweeperEngine does on the first reveal, using the
 * same seeded random source the app will use for a given `?seed=` URL param.
 * This lets e2e tests know the mine layout in advance without any test-only
 * hooks in the production code.
 */
export function simulateFirstClick(
  difficulty: Difficulty,
  seed: number,
  firstClick: Position,
): Board {
  const random = createSeededRandomSource(seed);
  const emptyBoard = createEmptyBoard(difficulty.rows, difficulty.cols);
  const minedBoard = placeMines(emptyBoard, difficulty.mines, firstClick, random);
  return revealCell(minedBoard, firstClick).board;
}

export function findMinePosition(board: Board): Position {
  for (let row = 0; row < board.length; row++) {
    for (let col = 0; col < board[row].length; col++) {
      if (board[row][col].hasMine) return { row, col };
    }
  }
  throw new Error("No mine found on board");
}

export function findHiddenNonMinePositions(board: Board): Position[] {
  const positions: Position[] = [];
  for (let row = 0; row < board.length; row++) {
    for (let col = 0; col < board[row].length; col++) {
      if (!board[row][col].hasMine && board[row][col].state === "hidden") {
        positions.push({ row, col });
      }
    }
  }
  return positions;
}
