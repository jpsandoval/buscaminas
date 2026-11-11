from __future__ import annotations

import copy
import random as _random_module
from dataclasses import dataclass

from .types import Cell, Position, RandomSource


@dataclass
class RevealOutcome:
    board: Board
    hit_mine: bool


class Board:
    """The Minesweeper grid. Owns its cells and every operation that reads or
    mutates them, so callers never poke at cell state directly."""

    def __init__(self, rows: int, cols: int, grid: list[list[Cell]] | None = None):
        self._rows = rows
        self._cols = cols
        self._grid = grid if grid is not None else [[Cell() for _ in range(cols)] for _ in range(rows)]

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def __getitem__(self, row: int) -> list[Cell]:
        return self._grid[row]

    def __iter__(self):
        return iter(self._grid)

    def __len__(self) -> int:
        return self._rows

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Board) and self._grid == other._grid

    def clone(self) -> Board:
        return Board(self._rows, self._cols, copy.deepcopy(self._grid))

    def neighbors(self, position: Position) -> list[Position]:
        neighbors: list[Position] = []

        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                if delta_row == 0 and delta_col == 0:
                    continue

                row = position.row + delta_row
                col = position.col + delta_col

                if 0 <= row < self._rows and 0 <= col < self._cols:
                    neighbors.append(Position(row, col))

        return neighbors

    def place_mines(
        self,
        mine_count: int,
        safe_position: Position,
        random: RandomSource = _random_module.random,
    ) -> Board:
        """Places mines on a copy of this board, keeping `safe_position` and its
        neighbors mine-free so the player's first click always opens a safe area."""
        candidates = self._find_mine_candidates(safe_position, mine_count)

        mine_positions = {
            _to_key(position)
            for position in self._shuffle(candidates, random)[: min(mine_count, len(candidates))]
        }

        next_board = self.clone()
        for row in range(self._rows):
            for col in range(self._cols):
                next_board[row][col].has_mine = _to_key(Position(row, col)) in mine_positions

        return next_board.calculate_adjacent_mines()

    def calculate_adjacent_mines(self) -> Board:
        next_board = self.clone()

        for row in range(self._rows):
            for col in range(self._cols):
                cell = next_board[row][col]
                if cell.has_mine:
                    continue

                cell.adjacent_mines = sum(
                    1
                    for neighbor in next_board.neighbors(Position(row, col))
                    if next_board[neighbor.row][neighbor.col].has_mine
                )

        return next_board

    def reveal(self, position: Position) -> RevealOutcome:
        """Reveals a cell. If it has no adjacent mines, floods outward revealing
        every connected zero-cell and its bordering numbered cells."""
        cell = self[position.row][position.col]

        if not cell.is_hidden:
            return RevealOutcome(board=self, hit_mine=False)

        next_board = self.clone()
        target = next_board[position.row][position.col]

        if target.has_mine:
            target.reveal()
            return RevealOutcome(board=next_board, hit_mine=True)

        next_board._flood_reveal(position)
        return RevealOutcome(board=next_board, hit_mine=False)

    def toggle_flag(self, position: Position) -> Board:
        cell = self[position.row][position.col]
        if cell.is_revealed:
            return self

        next_board = self.clone()
        next_board[position.row][position.col].toggle_flag()
        return next_board

    def reveal_all_mines(self) -> Board:
        next_board = self.clone()
        for row in next_board:
            for cell in row:
                if cell.has_mine:
                    cell.reveal()
        return next_board

    def count_flags(self) -> int:
        return sum(1 for row in self for cell in row if cell.is_flagged)

    def has_won(self) -> bool:
        """The player wins once every non-mine cell has been revealed."""
        return all(cell.has_mine or cell.is_revealed for row in self for cell in row)

    def _flood_reveal(self, start: Position) -> None:
        pending: list[Position] = [start]

        while pending:
            position = pending.pop()

            cell = self[position.row][position.col]
            if not cell.is_hidden or cell.has_mine:
                continue

            cell.reveal()

            if cell.adjacent_mines == 0:
                pending.extend(self.neighbors(position))

    def _find_mine_candidates(self, safe_position: Position, mine_count: int) -> list[Position]:
        """Candidate cells for mines, excluding `safe_position` and its neighbors so
        the first click opens a safe area. Falls back to excluding only
        `safe_position` itself when the board is too small to spare the whole
        neighborhood and still fit every requested mine."""
        excluded_with_neighbors = {_to_key(safe_position)} | {
            _to_key(neighbor) for neighbor in self.neighbors(safe_position)
        }
        with_neighbors_excluded = self._positions_excluding(excluded_with_neighbors)

        if len(with_neighbors_excluded) >= mine_count:
            return with_neighbors_excluded

        return self._positions_excluding({_to_key(safe_position)})

    def _positions_excluding(self, excluded: set[str]) -> list[Position]:
        positions: list[Position] = []
        for row in range(self._rows):
            for col in range(self._cols):
                position = Position(row, col)
                if _to_key(position) not in excluded:
                    positions.append(position)
        return positions

    @staticmethod
    def _shuffle(items: list[Position], random: RandomSource) -> list[Position]:
        result = list(items)

        for i in range(len(result) - 1, 0, -1):
            j = int(random() * (i + 1))
            result[i], result[j] = result[j], result[i]

        return result


def _to_key(position: Position) -> str:
    return f"{position.row}:{position.col}"
