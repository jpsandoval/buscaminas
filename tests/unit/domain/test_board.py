from app.domain.board import Board
from app.domain.types import Position


def test_create_empty_board_has_given_dimensions_all_hidden_mine_free():
    board = Board(3, 4)

    assert len(board) == 3
    assert len(board[0]) == 4
    for row in board:
        for cell in row:
            assert cell.has_mine is False
            assert cell.adjacent_mines == 0
            assert cell.state == "hidden"


def test_neighbors_returns_all_8_for_a_middle_cell():
    board = Board(3, 3)
    neighbors = board.neighbors(Position(1, 1))
    assert len(neighbors) == 8


def test_neighbors_excludes_out_of_bounds_for_a_corner_cell():
    board = Board(3, 3)
    neighbors = board.neighbors(Position(0, 0))
    assert len(neighbors) == 3
    assert set(neighbors) == {Position(0, 1), Position(1, 0), Position(1, 1)}


def test_place_mines_places_exactly_the_requested_number():
    board = Board(5, 5)
    result = board.place_mines(6, Position(0, 0))

    mine_count = sum(1 for row in result for cell in row if cell.has_mine)
    assert mine_count == 6


def test_place_mines_never_places_a_mine_on_the_safe_position_or_its_neighbors():
    board = Board(5, 5)
    safe_position = Position(2, 2)
    # Fill almost the whole board with mines to stress-test the safe zone.
    result = board.place_mines(16, safe_position)

    safe_zone = [safe_position, *board.neighbors(safe_position)]
    for position in safe_zone:
        assert result[position.row][position.col].has_mine is False


def test_place_mines_is_deterministic_given_the_same_random_source():
    board = Board(5, 5)
    fixed_values = [0.1, 0.9, 0.3, 0.5, 0.7, 0.2]

    def make_sequence():
        values = list(fixed_values)
        index = 0

        def sequence():
            nonlocal index
            value = values[index % len(values)]
            index += 1
            return value

        return sequence

    first = board.place_mines(5, Position(0, 0), make_sequence())
    second = board.place_mines(5, Position(0, 0), make_sequence())

    assert first == second


def test_calculate_adjacent_mines_counts_mines_around_each_non_mine_cell():
    board = Board(3, 3)
    board[0][0].has_mine = True
    board[2][2].has_mine = True

    result = board.calculate_adjacent_mines()

    assert result[0][1].adjacent_mines == 1
    assert result[1][0].adjacent_mines == 1
    assert result[1][1].adjacent_mines == 2
    assert result[1][2].adjacent_mines == 1
    assert result[2][1].adjacent_mines == 1
    assert result[0][2].adjacent_mines == 0
