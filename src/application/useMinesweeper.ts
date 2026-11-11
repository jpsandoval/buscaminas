import { useCallback, useEffect, useState } from "react";
import {
  MinesweeperEngine,
  type Difficulty,
  type MinesweeperState,
  type Position,
  type RandomSource,
} from "../domain/minesweeper";

export interface UseMinesweeperOptions {
  randomSource?: RandomSource;
}

export interface UseMinesweeperResult {
  state: MinesweeperState;
  elapsedSeconds: number;
  reveal: (position: Position) => void;
  toggleFlag: (position: Position) => void;
  reset: (difficulty?: Difficulty) => void;
}

function createEngine(
  difficulty: Difficulty,
  randomSource?: RandomSource,
): MinesweeperEngine {
  return randomSource
    ? new MinesweeperEngine(difficulty, randomSource)
    : new MinesweeperEngine(difficulty);
}

/** Bridges the framework-agnostic MinesweeperEngine with React state. */
export function useMinesweeper(
  initialDifficulty: Difficulty,
  options: UseMinesweeperOptions = {},
): UseMinesweeperResult {
  const { randomSource } = options;
  const [engine, setEngine] = useState<MinesweeperEngine>(() =>
    createEngine(initialDifficulty, randomSource),
  );
  const [state, setState] = useState<MinesweeperState>(() => engine.getState());
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  useEffect(() => {
    if (state.status !== "playing") return undefined;

    const intervalId = window.setInterval(() => {
      setElapsedSeconds((seconds) => seconds + 1);
    }, 1000);

    return () => window.clearInterval(intervalId);
  }, [state.status]);

  const reveal = useCallback(
    (position: Position) => {
      setState(engine.reveal(position));
    },
    [engine],
  );

  const toggleFlag = useCallback(
    (position: Position) => {
      setState(engine.toggleFlag(position));
    },
    [engine],
  );

  const reset = useCallback(
    (difficulty: Difficulty = state.difficulty) => {
      const nextEngine = createEngine(difficulty, randomSource);
      setEngine(nextEngine);
      setElapsedSeconds(0);
      setState(nextEngine.getState());
    },
    [state.difficulty, randomSource],
  );

  return { state, elapsedSeconds, reveal, toggleFlag, reset };
}
