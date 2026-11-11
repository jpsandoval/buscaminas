from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

CellState = Literal["hidden", "revealed", "flagged"]
GameStatus = Literal["ready", "playing", "won", "lost"]

RandomSource = Callable[[], float]


@dataclass(frozen=True)
class Position:
    row: int
    col: int


@dataclass
class Cell:
    has_mine: bool = False
    adjacent_mines: int = 0
    state: CellState = "hidden"


Board = list[list[Cell]]


@dataclass(frozen=True)
class Difficulty:
    id: str
    label: str
    rows: int
    cols: int
    mines: int


@dataclass
class MinesweeperState:
    board: Board
    status: GameStatus
    difficulty: Difficulty
    flags_placed: int
    mines_remaining: int
