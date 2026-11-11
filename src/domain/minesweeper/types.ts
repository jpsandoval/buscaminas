export interface Position {
  row: number;
  col: number;
}

export type CellState = "hidden" | "revealed" | "flagged";

export interface Cell {
  hasMine: boolean;
  adjacentMines: number;
  state: CellState;
}

export type Board = Cell[][];

export type GameStatus = "ready" | "playing" | "won" | "lost";

export interface Difficulty {
  id: string;
  label: string;
  rows: number;
  cols: number;
  mines: number;
}

export interface MinesweeperState {
  board: Board;
  status: GameStatus;
  difficulty: Difficulty;
  flagsPlaced: number;
  minesRemaining: number;
}

export type RandomSource = () => number;
