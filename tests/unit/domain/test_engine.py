from app.domain.engine import MinesweeperEngine
from app.domain.types import Difficulty, MinesweeperState, Position

TINY_DIFFICULTY = Difficulty(id="tiny", label="Tiny", rows=3, cols=3, mines=1)


def always_return(value):
    return lambda: value


def find_mine_position(state: MinesweeperState) -> Position:
    for row in range(len(state.board)):
        for col in range(len(state.board[row])):
            if state.board[row][col].has_mine:
                return Position(row, col)
    raise AssertionError("No mine found on board")


def all_positions(state: MinesweeperState) -> list[Position]:
    return [
        Position(row, col) for row in range(len(state.board)) for col in range(len(state.board[row]))
    ]


def test_starts_ready_with_no_mines_placed_on_an_untouched_board():
    engine = MinesweeperEngine(TINY_DIFFICULTY)
    state = engine.get_state()

    assert state.status == "ready"
    assert state.mines_remaining == 1
    assert all(not cell.has_mine for row in state.board for cell in row)


def test_places_mines_only_after_the_first_reveal_keeping_that_cell_safe():
    engine = MinesweeperEngine(TINY_DIFFICULTY, always_return(0))

    state = engine.reveal(Position(1, 1))

    assert state.status == "playing"
    assert state.board[1][1].has_mine is False
    assert sum(1 for row in state.board for cell in row if cell.has_mine) == 1


def test_transitions_to_lost_and_reveals_every_mine_when_a_mine_is_clicked():
    engine = MinesweeperEngine(TINY_DIFFICULTY, always_return(0))

    after_first_click = engine.reveal(Position(0, 0))
    mine_position = find_mine_position(after_first_click)

    state = engine.reveal(mine_position)

    assert state.status == "lost"
    assert state.board[mine_position.row][mine_position.col].state == "revealed"


def test_transitions_to_won_once_all_non_mine_cells_are_revealed():
    engine = MinesweeperEngine(TINY_DIFFICULTY, always_return(0))

    after_first_click = engine.reveal(Position(0, 0))
    mine_position = find_mine_position(after_first_click)
    remaining_positions = [
        position
        for position in all_positions(after_first_click)
        if not (position.row == mine_position.row and position.col == mine_position.col)
    ]

    state = after_first_click
    for position in remaining_positions:
        if state.board[position.row][position.col].state == "hidden":
            state = engine.reveal(position)

    assert state.status == "won"


def test_ignores_reveals_and_flag_toggles_once_the_game_has_ended():
    engine = MinesweeperEngine(TINY_DIFFICULTY, always_return(0))

    after_first_click = engine.reveal(Position(0, 0))
    mine_position = find_mine_position(after_first_click)
    lost_state = engine.reveal(mine_position)
    assert lost_state.status == "lost"

    after_extra_reveal = engine.reveal(Position(0, 0))
    after_extra_flag = engine.toggle_flag(Position(0, 0))

    assert after_extra_reveal == lost_state
    assert after_extra_flag == lost_state


def test_tracks_flags_placed_and_mines_remaining():
    engine = MinesweeperEngine(TINY_DIFFICULTY, always_return(0))

    state = engine.toggle_flag(Position(0, 0))

    assert state.flags_placed == 1
    assert state.mines_remaining == 0


def test_does_not_reveal_a_flagged_cell():
    engine = MinesweeperEngine(TINY_DIFFICULTY, always_return(0))

    engine.toggle_flag(Position(1, 1))
    state = engine.reveal(Position(1, 1))

    assert state.board[1][1].state == "flagged"
    assert state.status == "ready"
