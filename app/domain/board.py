from __future__ import annotations

import copy
import random as _random_module

from .types import Board, Cell, Position, RandomSource


def create_empty_board(rows: int, cols: int) -> Board:
    return [[_create_empty_cell() for _ in range(cols)] for _ in range(rows)]


def _create_empty_cell() -> Cell:
    return Cell(has_mine=False, adjacent_mines=0, state="hidden")


def clone_board(board: Board) -> Board:
    return copy.deepcopy(board)


def get_neighbor_positions(position: Position, rows: int, cols: int) -> list[Position]:
    neighbors: list[Position] = []

    for delta_row in (-1, 0, 1):
        for delta_col in (-1, 0, 1):
            if delta_row == 0 and delta_col == 0:
                continue

            row = position.row + delta_row
            col = position.col + delta_col

            if 0 <= row < rows and 0 <= col < cols:
                neighbors.append(Position(row, col))

    return neighbors


def place_mines(
    board: Board,
    mine_count: int,
    safe_position: Position,
    random: RandomSource = _random_module.random,
) -> Board:
    """Places mines on the board, keeping `safe_position` and its neighbors
    mine-free so the player's first click always opens a safe area."""
    rows = len(board)
    cols = len(board[0]) if rows else 0
    candidates = _find_mine_candidates(rows, cols, safe_position, mine_count)

    mine_positions = {
        _to_key(position)
        for position in _shuffle(candidates, random)[: min(mine_count, len(candidates))]
    }

    next_board = clone_board(board)
    for row in range(rows):
        for col in range(cols):
            next_board[row][col].has_mine = _to_key(Position(row, col)) in mine_positions

    return calculate_adjacent_mines(next_board)


def calculate_adjacent_mines(board: Board) -> Board:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    next_board = clone_board(board)

    for row in range(rows):
        for col in range(cols):
            if next_board[row][col].has_mine:
                continue

            neighbors = get_neighbor_positions(Position(row, col), rows, cols)
            next_board[row][col].adjacent_mines = sum(
                1 for neighbor in neighbors if next_board[neighbor.row][neighbor.col].has_mine
            )

    return next_board


def _find_mine_candidates(
    rows: int, cols: int, safe_position: Position, mine_count: int
) -> list[Position]:
    """Candidate cells for mines, excluding `safe_position` and its neighbors so
    the first click opens a safe area. Falls back to excluding only
    `safe_position` itself when the board is too small to spare the whole
    neighborhood and still fit every requested mine."""
    excluded_with_neighbors = {_to_key(safe_position)} | {
        _to_key(neighbor) for neighbor in get_neighbor_positions(safe_position, rows, cols)
    }
    with_neighbors_excluded = _positions_excluding(rows, cols, excluded_with_neighbors)

    if len(with_neighbors_excluded) >= mine_count:
        return with_neighbors_excluded

    return _positions_excluding(rows, cols, {_to_key(safe_position)})


def _positions_excluding(rows: int, cols: int, excluded: set[str]) -> list[Position]:
    positions: list[Position] = []
    for row in range(rows):
        for col in range(cols):
            position = Position(row, col)
            if _to_key(position) not in excluded:
                positions.append(position)
    return positions


def _to_key(position: Position) -> str:
    return f"{position.row}:{position.col}"


def _shuffle(items: list[Position], random: RandomSource) -> list[Position]:
    result = list(items)

    for i in range(len(result) - 1, 0, -1):
        j = int(random() * (i + 1))
        result[i], result[j] = result[j], result[i]

    return result
