import type { MouseEvent } from "react";
import type { Cell as CellModel, Position } from "../../../domain/minesweeper";
import styles from "./Cell.module.css";

export interface CellProps {
  cell: CellModel;
  position: Position;
  disabled: boolean;
  onReveal: (position: Position) => void;
  onToggleFlag: (position: Position) => void;
}

const COUNT_STYLES: Record<number, string> = {
  1: styles.count1,
  2: styles.count2,
  3: styles.count3,
  4: styles.count4,
  5: styles.count5,
  6: styles.count6,
  7: styles.count7,
  8: styles.count8,
};

export function Cell({ cell, position, disabled, onReveal, onToggleFlag }: CellProps) {
  const label = describeCell(cell, position);

  function handleClick() {
    if (disabled) return;
    onReveal(position);
  }

  function handleContextMenu(event: MouseEvent) {
    event.preventDefault();
    if (disabled) return;
    onToggleFlag(position);
  }

  return (
    <button
      type="button"
      className={[styles.cell, styles[cell.state], cell.state === "revealed" && cell.hasMine ? styles.mine : ""]
        .filter(Boolean)
        .join(" ")}
      onClick={handleClick}
      onContextMenu={handleContextMenu}
      disabled={disabled || cell.state === "revealed"}
      aria-label={label}
      data-testid={`cell-${position.row}-${position.col}`}
      data-state={cell.state}
      data-has-mine={cell.hasMine}
    >
      <CellContent cell={cell} />
    </button>
  );
}

function CellContent({ cell }: { cell: CellModel }) {
  if (cell.state === "flagged") return <span aria-hidden="true">🚩</span>;
  if (cell.state !== "revealed") return null;
  if (cell.hasMine) return <span aria-hidden="true">💣</span>;
  if (cell.adjacentMines === 0) return null;

  return (
    <span aria-hidden="true" className={COUNT_STYLES[cell.adjacentMines]}>
      {cell.adjacentMines}
    </span>
  );
}

function describeCell(cell: CellModel, position: Position): string {
  const where = `fila ${position.row + 1}, columna ${position.col + 1}`;

  if (cell.state === "flagged") return `Casilla marcada, ${where}`;
  if (cell.state === "hidden") return `Casilla oculta, ${where}`;
  if (cell.hasMine) return `Mina, ${where}`;
  if (cell.adjacentMines === 0) return `Casilla vacía, ${where}`;
  return `${cell.adjacentMines} minas adyacentes, ${where}`;
}
