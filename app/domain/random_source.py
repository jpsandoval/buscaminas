from __future__ import annotations

_MASK32 = 0xFFFFFFFF


class SeededRandomSource:
    """Deterministic PRNG (mulberry32) so a game can be reproduced from a numeric
    seed — used for shareable boards and for deterministic end-to-end tests."""

    def __init__(self, seed: int):
        self._state = seed & _MASK32

    def __call__(self) -> float:
        self._state = (self._state + 0x6D2B79F5) & _MASK32
        s = self._state
        result = self._imul(s ^ (s >> 15), (1 | s) & _MASK32)
        combined = (result + self._imul(result ^ (result >> 7), (61 | result) & _MASK32)) & _MASK32
        result = (combined ^ result) & _MASK32
        final = (result ^ (result >> 14)) & _MASK32
        return final / 4294967296

    @staticmethod
    def _imul(a: int, b: int) -> int:
        return (a * b) & _MASK32
