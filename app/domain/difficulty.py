from __future__ import annotations

from .types import Difficulty

DIFFICULTIES: tuple[Difficulty, ...] = (
    Difficulty(id="beginner", label="Principiante", rows=9, cols=9, mines=10),
    Difficulty(id="intermediate", label="Intermedio", rows=16, cols=16, mines=40),
    Difficulty(id="expert", label="Experto", rows=16, cols=30, mines=99),
)

DEFAULT_DIFFICULTY: Difficulty = DIFFICULTIES[0]


def find_difficulty_by_id(difficulty_id: str) -> Difficulty | None:
    for difficulty in DIFFICULTIES:
        if difficulty.id == difficulty_id:
            return difficulty
    return None
