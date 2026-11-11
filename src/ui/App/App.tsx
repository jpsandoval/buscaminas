import { useMemo } from "react";
import { useMinesweeper } from "../../application/useMinesweeper";
import { createSeededRandomSource, type GameStatus } from "../../domain/minesweeper";
import { readGameUrlParams } from "../../shared/gameUrlParams";
import { Board } from "../components/Board/Board";
import { DifficultySelector } from "../components/DifficultySelector/DifficultySelector";
import { GameHeader } from "../components/GameHeader/GameHeader";
import styles from "./App.module.css";

export function App() {
  const { difficulty: initialDifficulty, seed } = useMemo(
    () => readGameUrlParams(window.location.search),
    [],
  );
  const randomSource = useMemo(
    () => (seed === null ? undefined : createSeededRandomSource(seed)),
    [seed],
  );

  const { state, elapsedSeconds, reveal, toggleFlag, reset } = useMinesweeper(
    initialDifficulty,
    { randomSource },
  );

  const isFinished = state.status === "won" || state.status === "lost";

  return (
    <main className={styles.page}>
      <h1 className={styles.title}>Buscaminas</h1>

      <DifficultySelector selected={state.difficulty} onSelect={(difficulty) => reset(difficulty)} />

      <GameHeader
        minesRemaining={state.minesRemaining}
        elapsedSeconds={elapsedSeconds}
        status={state.status}
        onReset={() => reset()}
      />

      <p
        className={[styles.status, state.status === "won" ? styles.won : "", state.status === "lost" ? styles.lost : ""]
          .filter(Boolean)
          .join(" ")}
        data-testid="game-status"
        role="status"
      >
        {describeStatus(state.status)}
      </p>

      <Board board={state.board} disabled={isFinished} onReveal={reveal} onToggleFlag={toggleFlag} />
    </main>
  );
}

function describeStatus(status: GameStatus): string {
  switch (status) {
    case "won":
      return "¡Ganaste! 🎉";
    case "lost":
      return "Perdiste. Inténtalo de nuevo.";
    case "playing":
      return "Click izquierdo para revelar, click derecho para marcar.";
    default:
      return "Haz click en una casilla para empezar.";
  }
}
