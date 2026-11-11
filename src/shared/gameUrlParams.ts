import { DEFAULT_DIFFICULTY, findDifficultyById } from "../domain/minesweeper";
import type { Difficulty } from "../domain/minesweeper";

export interface GameUrlParams {
  difficulty: Difficulty;
  seed: number | null;
}

/**
 * Reads `?difficulty=` and `?seed=` from the URL so a game can be shared or
 * reproduced deterministically (also used to drive deterministic e2e tests).
 */
export function readGameUrlParams(search: string): GameUrlParams {
  const params = new URLSearchParams(search);

  const difficultyId = params.get("difficulty");
  const difficulty = (difficultyId && findDifficultyById(difficultyId)) || DEFAULT_DIFFICULTY;

  const seedParam = params.get("seed");
  const parsedSeed = seedParam === null ? NaN : Number(seedParam);
  const seed = Number.isFinite(parsedSeed) ? parsedSeed : null;

  return { difficulty, seed };
}
