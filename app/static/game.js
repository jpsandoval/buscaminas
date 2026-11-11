(() => {
  const FACE_BY_STATUS = { ready: "🙂", playing: "🙂", won: "😎", lost: "😵" };

  const STATUS_MESSAGES = {
    ready: "Haz click en una casilla para empezar.",
    playing: "Click izquierdo para revelar, click derecho para marcar.",
    won: "¡Ganaste! 🎉",
    lost: "Perdiste. Inténtalo de nuevo.",
  };

  const boardEl = document.querySelector('[data-testid="board"]');
  const statusEl = document.querySelector('[data-testid="game-status"]');
  const minesRemainingEl = document.querySelector('[data-testid="mines-remaining"]');
  const elapsedSecondsEl = document.querySelector('[data-testid="elapsed-seconds"]');
  const resetButtonEl = document.querySelector('[data-testid="reset-button"]');
  const difficultyButtons = Array.from(document.querySelectorAll("[data-difficulty-id]"));

  let state = JSON.parse(document.getElementById("initial-state").textContent);
  let elapsedSeconds = 0;
  let timerId = null;

  function formatCounter(value) {
    const clamped = Math.max(0, Math.min(999, value));
    return String(clamped).padStart(3, "0");
  }

  function describeCell(cell, row, col) {
    const where = `fila ${row + 1}, columna ${col + 1}`;
    if (cell.state === "flagged") return `Casilla marcada, ${where}`;
    if (cell.state === "hidden") return `Casilla oculta, ${where}`;
    if (cell.hasMine) return `Mina, ${where}`;
    if (cell.adjacentMines === 0) return `Casilla vacía, ${where}`;
    return `${cell.adjacentMines} minas adyacentes, ${where}`;
  }

  function cellContent(cell) {
    if (cell.state === "flagged") return '<span aria-hidden="true">🚩</span>';
    if (cell.state !== "revealed") return "";
    if (cell.hasMine) return '<span aria-hidden="true">💣</span>';
    if (cell.adjacentMines === 0) return "";
    return `<span aria-hidden="true" class="count-${cell.adjacentMines}">${cell.adjacentMines}</span>`;
  }

  function isFinished() {
    return state.status === "won" || state.status === "lost";
  }

  function render() {
    const disabled = isFinished();
    const cols = state.board[0]?.length ?? 0;
    boardEl.style.gridTemplateColumns = `repeat(${cols}, 2rem)`;

    boardEl.innerHTML = state.board
      .map((rowCells, row) => {
        const cellsHtml = rowCells
          .map((cell, col) => {
            const classes = ["cell", cell.state];
            if (cell.state === "revealed" && cell.hasMine) classes.push("mine");
            const isDisabled = disabled || cell.state === "revealed";
            return `<button type="button" class="${classes.join(" ")}" ${isDisabled ? "disabled" : ""}
              aria-label="${describeCell(cell, row, col)}"
              data-testid="cell-${row}-${col}" data-state="${cell.state}" data-has-mine="${cell.hasMine}"
              data-row="${row}" data-col="${col}">${cellContent(cell)}</button>`;
          })
          .join("");
        return `<div class="row" role="row">${cellsHtml}</div>`;
      })
      .join("");

    minesRemainingEl.textContent = formatCounter(state.minesRemaining);
    elapsedSecondsEl.textContent = formatCounter(elapsedSeconds);
    resetButtonEl.textContent = FACE_BY_STATUS[state.status];

    statusEl.textContent = STATUS_MESSAGES[state.status];
    statusEl.classList.toggle("won", state.status === "won");
    statusEl.classList.toggle("lost", state.status === "lost");

    for (const button of difficultyButtons) {
      button.classList.toggle("selected", button.dataset.difficultyId === state.difficulty.id);
      button.setAttribute(
        "aria-checked",
        String(button.dataset.difficultyId === state.difficulty.id),
      );
    }

    syncTimer();
  }

  function syncTimer() {
    if (state.status === "playing" && timerId === null) {
      timerId = window.setInterval(() => {
        elapsedSeconds += 1;
        elapsedSecondsEl.textContent = formatCounter(elapsedSeconds);
      }, 1000);
    } else if (state.status !== "playing" && timerId !== null) {
      window.clearInterval(timerId);
      timerId = null;
    }
  }

  async function postJson(url, body) {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return response.json();
  }

  boardEl.addEventListener("click", async (event) => {
    const cellButton = event.target.closest("button[data-testid^='cell-']");
    if (!cellButton || isFinished()) return;

    const row = Number(cellButton.dataset.row);
    const col = Number(cellButton.dataset.col);
    state = await postJson("/api/reveal", { row, col });
    render();
  });

  boardEl.addEventListener("contextmenu", async (event) => {
    event.preventDefault();
    const cellButton = event.target.closest("button[data-testid^='cell-']");
    if (!cellButton || isFinished()) return;

    const row = Number(cellButton.dataset.row);
    const col = Number(cellButton.dataset.col);
    state = await postJson("/api/flag", { row, col });
    render();
  });

  resetButtonEl.addEventListener("click", async () => {
    elapsedSeconds = 0;
    state = await postJson("/api/reset", {});
    render();
  });

  for (const button of difficultyButtons) {
    button.addEventListener("click", async () => {
      elapsedSeconds = 0;
      state = await postJson("/api/reset", { difficultyId: button.dataset.difficultyId });
      render();
    });
  }

  render();
})();
