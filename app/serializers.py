from __future__ import annotations

from .domain import MinesweeperState


def serialize_state(state: MinesweeperState) -> dict:
    return {
        "status": state.status,
        "difficulty": {
            "id": state.difficulty.id,
            "label": state.difficulty.label,
            "rows": state.difficulty.rows,
            "cols": state.difficulty.cols,
            "mines": state.difficulty.mines,
        },
        "flagsPlaced": state.flags_placed,
        "minesRemaining": state.mines_remaining,
        "board": [
            [
                {
                    "hasMine": cell.has_mine,
                    "adjacentMines": cell.adjacent_mines,
                    "state": cell.state,
                }
                for cell in row
            ]
            for row in state.board
        ],
    }
