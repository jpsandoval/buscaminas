import { DIFFICULTIES, type Difficulty } from "../../../domain/minesweeper";
import styles from "./DifficultySelector.module.css";

export interface DifficultySelectorProps {
  selected: Difficulty;
  onSelect: (difficulty: Difficulty) => void;
}

export function DifficultySelector({ selected, onSelect }: DifficultySelectorProps) {
  return (
    <div className={styles.selector} role="radiogroup" aria-label="Dificultad">
      {DIFFICULTIES.map((difficulty) => (
        <button
          key={difficulty.id}
          type="button"
          role="radio"
          aria-checked={difficulty.id === selected.id}
          className={[styles.option, difficulty.id === selected.id ? styles.selected : ""]
            .filter(Boolean)
            .join(" ")}
          onClick={() => onSelect(difficulty)}
          data-testid={`difficulty-${difficulty.id}`}
        >
          {difficulty.label}
        </button>
      ))}
    </div>
  );
}
