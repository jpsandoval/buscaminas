import type { Board as BoardModel, Position } from "../../../domain/minesweeper";
import { Cell } from "../Cell/Cell";
import styles from "./Board.module.css";

export interface BoardProps {
  board: BoardModel;
  disabled: boolean;
  onReveal: (position: Position) => void;
  onToggleFlag: (position: Position) => void;
}

export function Board({ board, disabled, onReveal, onToggleFlag }: BoardProps) {
  const cols = board[0]?.length ?? 0;

  return (
    <div
      className={styles.board}
      style={{ gridTemplateColumns: `repeat(${cols}, 2rem)` }}
      role="grid"
      data-testid="board"
    >
      {board.map((row, rowIndex) => (
        <div className={styles.row} role="row" key={rowIndex}>
          {row.map((cell, colIndex) => (
            <Cell
              key={colIndex}
              cell={cell}
              position={{ row: rowIndex, col: colIndex }}
              disabled={disabled}
              onReveal={onReveal}
              onToggleFlag={onToggleFlag}
            />
          ))}
        </div>
      ))}
    </div>
  );
}
