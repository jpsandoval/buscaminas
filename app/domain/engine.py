from __future__ import annotations

import random as _random_module

from .board import create_empty_board, place_mines
from .gameplay import count_flags, has_won, reveal_all_mines, reveal_cell, toggle_flag
from .types import Difficulty, GameStatus, MinesweeperState, Position, RandomSource


class MinesweeperEngine:
    """Orchestrates a single Minesweeper game: owns the board, applies the
    first-click-is-safe rule, and tracks win/lose status. Framework-agnostic
    so it can be unit tested in isolation and reused by any UI layer."""

    def __init__(self, difficulty: Difficulty, random: RandomSource = _random_module.random):
        self._difficulty = difficulty
        self._random = random
        self._board = create_empty_board(difficulty.rows, difficulty.cols)
        self._status: GameStatus = "ready"
        self._mines_placed = False

    def get_state(self) -> MinesweeperState:
        flags_placed = count_flags(self._board)
        return MinesweeperState(
            board=self._board,
            status=self._status,
            difficulty=self._difficulty,
            flags_placed=flags_placed,
            mines_remaining=self._difficulty.mines - flags_placed,
        )

    def reveal(self, position: Position) -> MinesweeperState:
        if self._is_finished() or self._board[position.row][position.col].state == "flagged":
            return self.get_state()

        if not self._mines_placed:
            self._board = place_mines(self._board, self._difficulty.mines, position, self._random)
            self._mines_placed = True
            self._status = "playing"

        outcome = reveal_cell(self._board, position)
        self._board = outcome.board

        if outcome.hit_mine:
            self._board = reveal_all_mines(self._board)
            self._status = "lost"
        elif has_won(self._board):
            self._status = "won"

        return self.get_state()

    def toggle_flag(self, position: Position) -> MinesweeperState:
        if self._is_finished():
            return self.get_state()

        self._board = toggle_flag(self._board, position)
        return self.get_state()

    def _is_finished(self) -> bool:
        return self._status in ("won", "lost")
