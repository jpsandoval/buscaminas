from __future__ import annotations

import random as _random_module

from .board import Board
from .types import Difficulty, GameStatus, MinesweeperState, Position, RandomSource


class MinesweeperEngine:
    """Orchestrates a single Minesweeper game: owns the board, applies the
    first-click-is-safe rule, and tracks win/lose status. Framework-agnostic
    so it can be unit tested in isolation and reused by any UI layer."""

    def __init__(self, difficulty: Difficulty, random: RandomSource = _random_module.random):
        self._difficulty = difficulty
        self._random = random
        self._board = Board(difficulty.rows, difficulty.cols)
        self._status: GameStatus = "ready"
        self._mines_placed = False

    def get_state(self) -> MinesweeperState:
        flags_placed = self._board.count_flags()
        return MinesweeperState(
            board=self._board,
            status=self._status,
            difficulty=self._difficulty,
            flags_placed=flags_placed,
            mines_remaining=self._difficulty.mines - flags_placed,
        )

    def reveal(self, position: Position) -> MinesweeperState:
        if self._is_finished() or self._board[position.row][position.col].is_flagged:
            return self.get_state()

        if not self._mines_placed:
            self._board = self._board.place_mines(self._difficulty.mines, position, self._random)
            self._mines_placed = True
            self._status = "playing"

        outcome = self._board.reveal(position)
        self._board = outcome.board

        if outcome.hit_mine:
            self._board = self._board.reveal_all_mines()
            self._status = "lost"
        elif self._board.has_won():
            self._status = "won"

        return self.get_state()

    def toggle_flag(self, position: Position) -> MinesweeperState:
        if self._is_finished():
            return self.get_state()

        self._board = self._board.toggle_flag(position)
        return self.get_state()

    def _is_finished(self) -> bool:
        return self._status in ("won", "lost")
