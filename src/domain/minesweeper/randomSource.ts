import type { RandomSource } from "./types";

/**
 * Deterministic PRNG (mulberry32) so a game can be reproduced from a numeric
 * seed — used for shareable boards and for deterministic end-to-end tests.
 */
export function createSeededRandomSource(seed: number): RandomSource {
  let state = seed >>> 0;

  return function mulberry32() {
    state = (state + 0x6d2b79f5) | 0;
    let result = Math.imul(state ^ (state >>> 15), 1 | state);
    result = (result + Math.imul(result ^ (result >>> 7), 61 | result)) ^ result;
    return ((result ^ (result >>> 14)) >>> 0) / 4294967296;
  };
}
