import { createEmptyBoard, placeMines } from "./board";
import {
  countFlags,
  hasWon,
  revealAllMines,
  revealCell,
  toggleFlag,
} from "./gameplay";
import type {
  Difficulty,
  GameStatus,
  MinesweeperState,
  Position,
  RandomSource,
} from "./types";

/**
 * Orchestrates a single Minesweeper game: owns the board, applies the
 * first-click-is-safe rule, and tracks win/lose status. Framework-agnostic
 * so it can be unit tested in isolation and reused by any UI layer.
 */
export class MinesweeperEngine {
  private readonly difficulty: Difficulty;
  private readonly random: RandomSource;
  private board = createEmptyBoard(0, 0);
  private status: GameStatus = "ready";
  private minesPlaced = false;

  constructor(difficulty: Difficulty, random: RandomSource = Math.random) {
    this.difficulty = difficulty;
    this.random = random;
    this.board = createEmptyBoard(difficulty.rows, difficulty.cols);
  }

  getState(): MinesweeperState {
    const flagsPlaced = countFlags(this.board);
    return {
      board: this.board,
      status: this.status,
      difficulty: this.difficulty,
      flagsPlaced,
      minesRemaining: this.difficulty.mines - flagsPlaced,
    };
  }

  reveal(position: Position): MinesweeperState {
    if (this.isFinished() || this.board[position.row][position.col].state === "flagged") {
      return this.getState();
    }

    if (!this.minesPlaced) {
      this.board = placeMines(this.board, this.difficulty.mines, position, this.random);
      this.minesPlaced = true;
      this.status = "playing";
    }

    const { board, hitMine } = revealCell(this.board, position);
    this.board = board;

    if (hitMine) {
      this.board = revealAllMines(this.board);
      this.status = "lost";
    } else if (hasWon(this.board)) {
      this.status = "won";
    }

    return this.getState();
  }

  toggleFlag(position: Position): MinesweeperState {
    if (this.isFinished()) return this.getState();

    this.board = toggleFlag(this.board, position);
    return this.getState();
  }

  private isFinished(): boolean {
    return this.status === "won" || this.status === "lost";
  }
}
