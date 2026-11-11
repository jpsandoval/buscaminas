from __future__ import annotations

from .types import RandomSource

_MASK32 = 0xFFFFFFFF


def _imul(a: int, b: int) -> int:
    return (a * b) & _MASK32


def create_seeded_random_source(seed: int) -> RandomSource:
    """Deterministic PRNG (mulberry32) so a game can be reproduced from a numeric
    seed — used for shareable boards and for deterministic end-to-end tests."""
    state = seed & _MASK32

    def mulberry32() -> float:
        nonlocal state
        state = (state + 0x6D2B79F5) & _MASK32
        s = state
        result = _imul(s ^ (s >> 15), (1 | s) & _MASK32)
        combined = (result + _imul(result ^ (result >> 7), (61 | result) & _MASK32)) & _MASK32
        result = (combined ^ result) & _MASK32
        final = (result ^ (result >> 14)) & _MASK32
        return final / 4294967296

    return mulberry32
