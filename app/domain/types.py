from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Literal

if TYPE_CHECKING:
    from .board import Board

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

    @property
    def is_hidden(self) -> bool:
        return self.state == "hidden"

    @property
    def is_revealed(self) -> bool:
        return self.state == "revealed"

    @property
    def is_flagged(self) -> bool:
        return self.state == "flagged"

    def reveal(self) -> None:
        self.state = "revealed"

    def toggle_flag(self) -> None:
        if self.is_revealed:
            return
        self.state = "hidden" if self.is_flagged else "flagged"


@dataclass(frozen=True)
class Difficulty:
    id: str
    label: str
    rows: int
    cols: int
    mines: int

    @classmethod
    def all(cls) -> tuple[Difficulty, ...]:
        return _DIFFICULTIES

    @classmethod
    def default(cls) -> Difficulty:
        return _DIFFICULTIES[0]

    @classmethod
    def find_by_id(cls, difficulty_id: str) -> Difficulty | None:
        for difficulty in _DIFFICULTIES:
            if difficulty.id == difficulty_id:
                return difficulty
        return None


_DIFFICULTIES: tuple[Difficulty, ...] = (
    Difficulty(id="beginner", label="Principiante", rows=9, cols=9, mines=10),
    Difficulty(id="intermediate", label="Intermedio", rows=16, cols=16, mines=40),
    Difficulty(id="expert", label="Experto", rows=16, cols=30, mines=99),
)


@dataclass
class MinesweeperState:
    board: Board
    status: GameStatus
    difficulty: Difficulty
    flags_placed: int
    mines_remaining: int
