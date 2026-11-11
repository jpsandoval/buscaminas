from app.domain.random_source import SeededRandomSource


def test_produces_same_sequence_for_same_seed():
    first = SeededRandomSource(42)
    second = SeededRandomSource(42)

    first_values = [first() for _ in range(10)]
    second_values = [second() for _ in range(10)]

    assert first_values == second_values


def test_produces_different_sequences_for_different_seeds():
    first = SeededRandomSource(1)
    second = SeededRandomSource(2)

    first_values = [first() for _ in range(10)]
    second_values = [second() for _ in range(10)]

    assert first_values != second_values


def test_always_returns_values_within_unit_interval():
    random = SeededRandomSource(7)

    for _ in range(1000):
        value = random()
        assert 0 <= value < 1
