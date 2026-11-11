from app.domain.board import Board
from app.domain.types import Position


def test_reveal_reveals_a_single_cell_with_adjacent_mines_without_flooding():
    board = Board(3, 3)
    board[0][0].has_mine = True
    board[0][1].adjacent_mines = 1

    outcome = board.reveal(Position(0, 1))

    assert outcome.hit_mine is False
    assert outcome.board[0][1].state == "revealed"
    assert outcome.board[1][1].state == "hidden"


def test_reveal_floods_outward_through_connected_zero_cells():
    board = Board(3, 3)
    board[0][0].has_mine = True
    board[0][1].adjacent_mines = 1
    board[1][0].adjacent_mines = 1
    # every other cell has 0 adjacent mines and should be revealed by the flood

    outcome = board.reveal(Position(2, 2))

    assert outcome.hit_mine is False
    assert outcome.board[2][2].state == "revealed"
    assert outcome.board[1][1].state == "revealed"
    assert outcome.board[0][1].state == "revealed"
    assert outcome.board[1][0].state == "revealed"
    assert outcome.board[0][0].state == "hidden"


def test_reveal_reports_hit_mine_and_reveals_only_the_mine():
    board = Board(2, 2)
    board[1][1].has_mine = True

    outcome = board.reveal(Position(1, 1))

    assert outcome.hit_mine is True
    assert outcome.board[1][1].state == "revealed"
    assert outcome.board[0][0].state == "hidden"


def test_reveal_does_nothing_when_already_revealed_or_flagged():
    board = Board(2, 2)
    board[0][0].state = "revealed"
    board[0][1].state = "flagged"

    assert board.reveal(Position(0, 0)).board[0][0].state == "revealed"
    assert board.reveal(Position(0, 1)).board[0][1].state == "flagged"


def test_toggle_flag_flags_a_hidden_cell_and_unflags_it_back():
    board = Board(2, 2)

    flagged = board.toggle_flag(Position(0, 0))
    assert flagged[0][0].state == "flagged"

    unflagged = flagged.toggle_flag(Position(0, 0))
    assert unflagged[0][0].state == "hidden"


def test_toggle_flag_does_not_flag_an_already_revealed_cell():
    board = Board(2, 2)
    board[0][0].state = "revealed"

    result = board.toggle_flag(Position(0, 0))
    assert result[0][0].state == "revealed"


def test_reveal_all_mines_reveals_every_mine_leaving_other_cells_untouched():
    board = Board(2, 2)
    board[0][0].has_mine = True
    board[1][1].has_mine = True

    result = board.reveal_all_mines()

    assert result[0][0].state == "revealed"
    assert result[1][1].state == "revealed"
    assert result[0][1].state == "hidden"


def test_count_flags_counts_flagged_cells_only():
    board = Board(2, 2)
    board[0][0].state = "flagged"
    board[0][1].state = "flagged"
    board[1][0].state = "revealed"

    assert board.count_flags() == 2


def test_has_won_is_false_while_a_non_mine_cell_remains_hidden():
    board = Board(2, 2)
    board[0][0].has_mine = True
    board[0][1].state = "revealed"
    board[1][0].state = "revealed"
    # board[1][1] stays hidden

    assert board.has_won() is False


def test_has_won_is_true_once_every_non_mine_cell_is_revealed_mines_untouched():
    board = Board(2, 2)
    board[0][0].has_mine = True
    board[0][1].state = "revealed"
    board[1][0].state = "revealed"
    board[1][1].state = "revealed"

    assert board.has_won() is True
