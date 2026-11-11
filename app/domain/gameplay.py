from __future__ import annotations

from dataclasses import dataclass

from .board import clone_board, get_neighbor_positions
from .types import Board, Position


@dataclass
class RevealOutcome:
    board: Board
    hit_mine: bool


def reveal_cell(board: Board, position: Position) -> RevealOutcome:
    """Reveals a cell. If it has no adjacent mines, floods outward revealing
    every connected zero-cell and its bordering numbered cells."""
    cell = board[position.row][position.col]

    if cell.state != "hidden":
        return RevealOutcome(board=board, hit_mine=False)

    next_board = clone_board(board)

    if cell.has_mine:
        next_board[position.row][position.col].state = "revealed"
        return RevealOutcome(board=next_board, hit_mine=True)

    _flood_reveal(next_board, position)
    return RevealOutcome(board=next_board, hit_mine=False)


def _flood_reveal(board: Board, start: Position) -> None:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    pending: list[Position] = [start]

    while pending:
        position = pending.pop()

        cell = board[position.row][position.col]
        if cell.state != "hidden" or cell.has_mine:
            continue

        cell.state = "revealed"

        if cell.adjacent_mines == 0:
            pending.extend(get_neighbor_positions(position, rows, cols))


def toggle_flag(board: Board, position: Position) -> Board:
    cell = board[position.row][position.col]
    if cell.state == "revealed":
        return board

    next_board = clone_board(board)
    next_board[position.row][position.col].state = "hidden" if cell.state == "flagged" else "flagged"
    return next_board


def reveal_all_mines(board: Board) -> Board:
    next_board = clone_board(board)
    for row in next_board:
        for cell in row:
            if cell.has_mine:
                cell.state = "revealed"
    return next_board


def count_flags(board: Board) -> int:
    return sum(1 for row in board for cell in row if cell.state == "flagged")


def has_won(board: Board) -> bool:
    """The player wins once every non-mine cell has been revealed."""
    return all(cell.has_mine or cell.state == "revealed" for row in board for cell in row)
