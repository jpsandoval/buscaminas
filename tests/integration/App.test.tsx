import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";
import { App } from "../../src/ui/App/App";

function setUrl(search: string) {
  window.history.pushState({}, "", `/${search}`);
}

describe("App", () => {
  beforeEach(() => {
    setUrl("");
  });

  it("shows the initial prompt before the first click", () => {
    render(<App />);

    expect(screen.getByTestId("game-status")).toHaveTextContent(
      "Haz click en una casilla para empezar.",
    );
  });

  it("starts the game and keeps the first click safe", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByTestId("cell-4-4"));

    expect(screen.getByTestId("game-status")).toHaveTextContent(
      "Click izquierdo para revelar, click derecho para marcar.",
    );
    expect(screen.getByTestId("cell-4-4")).toHaveAttribute("data-state", "revealed");
  });

  it("flagging a cell updates the remaining mines counter", () => {
    render(<App />);

    expect(screen.getByTestId("mines-remaining")).toHaveTextContent("010");

    fireEvent.contextMenu(screen.getByTestId("cell-0-0"));

    expect(screen.getByTestId("mines-remaining")).toHaveTextContent("009");
    expect(screen.getByTestId("cell-0-0")).toHaveAttribute("data-state", "flagged");
  });

  it("switching difficulty rebuilds the board with the new size", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByTestId("difficulty-expert"));

    expect(screen.getByTestId("board").querySelectorAll("button")).toHaveLength(16 * 30);
  });

  it("the reset button restarts the game in ready status", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByTestId("cell-4-4"));
    expect(screen.getByTestId("game-status")).not.toHaveTextContent(
      "Haz click en una casilla para empezar.",
    );

    await user.click(screen.getByTestId("reset-button"));

    expect(screen.getByTestId("game-status")).toHaveTextContent(
      "Haz click en una casilla para empezar.",
    );
  });
});
