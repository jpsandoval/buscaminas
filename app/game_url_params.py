from __future__ import annotations

from dataclasses import dataclass

from .domain import Difficulty


@dataclass
class GameUrlParams:
    difficulty: Difficulty
    seed: int | None


def read_game_url_params(args) -> GameUrlParams:
    """Reads `difficulty=` and `seed=` query params so a game can be shared or
    reproduced deterministically (also used to drive deterministic e2e tests)."""
    difficulty_id = args.get("difficulty")
    difficulty = (difficulty_id and Difficulty.find_by_id(difficulty_id)) or Difficulty.default()

    seed_param = args.get("seed")
    seed: int | None
    try:
        seed = int(seed_param) if seed_param is not None else None
    except ValueError:
        seed = None

    return GameUrlParams(difficulty=difficulty, seed=seed)
