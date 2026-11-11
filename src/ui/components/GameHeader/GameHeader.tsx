import type { GameStatus } from "../../../domain/minesweeper";
import styles from "./GameHeader.module.css";

export interface GameHeaderProps {
  minesRemaining: number;
  elapsedSeconds: number;
  status: GameStatus;
  onReset: () => void;
}

const FACE_BY_STATUS: Record<GameStatus, string> = {
  ready: "🙂",
  playing: "🙂",
  won: "😎",
  lost: "😵",
};

export function GameHeader({ minesRemaining, elapsedSeconds, status, onReset }: GameHeaderProps) {
  return (
    <div className={styles.header}>
      <span className={styles.counter} data-testid="mines-remaining" aria-label="Minas restantes">
        {formatCounter(minesRemaining)}
      </span>

      <button
        type="button"
        className={styles.resetButton}
        onClick={onReset}
        aria-label="Reiniciar juego"
        data-testid="reset-button"
      >
        {FACE_BY_STATUS[status]}
      </button>

      <span className={styles.counter} data-testid="elapsed-seconds" aria-label="Tiempo transcurrido">
        {formatCounter(elapsedSeconds)}
      </span>
    </div>
  );
}

function formatCounter(value: number): string {
  const clamped = Math.max(0, Math.min(999, value));
  return clamped.toString().padStart(3, "0");
}
