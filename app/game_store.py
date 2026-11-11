from __future__ import annotations

import uuid

from .domain import Difficulty, MinesweeperEngine, RandomSource

_GAMES: dict[str, MinesweeperEngine] = {}


def create_game(difficulty: Difficulty, random: RandomSource | None = None) -> tuple[str, MinesweeperEngine]:
    game_id = uuid.uuid4().hex
    engine = MinesweeperEngine(difficulty, random) if random else MinesweeperEngine(difficulty)
    _GAMES[game_id] = engine
    return game_id, engine


def get_game(game_id: str | None) -> MinesweeperEngine | None:
    if game_id is None:
        return None
    return _GAMES.get(game_id)


def discard_game(game_id: str | None) -> None:
    if game_id is not None:
        _GAMES.pop(game_id, None)
