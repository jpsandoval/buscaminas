import type { Difficulty } from "./types";

export const DIFFICULTIES: readonly Difficulty[] = [
  { id: "beginner", label: "Principiante", rows: 9, cols: 9, mines: 10 },
  { id: "intermediate", label: "Intermedio", rows: 16, cols: 16, mines: 40 },
  { id: "expert", label: "Experto", rows: 16, cols: 30, mines: 99 },
];

export const DEFAULT_DIFFICULTY: Difficulty = DIFFICULTIES[0];

export function findDifficultyById(id: string): Difficulty | undefined {
  return DIFFICULTIES.find((difficulty) => difficulty.id === id);
}
