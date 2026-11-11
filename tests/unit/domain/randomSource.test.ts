import { describe, expect, it } from "vitest";
import { createSeededRandomSource } from "../../../src/domain/minesweeper/randomSource";

describe("createSeededRandomSource", () => {
  it("produces the same sequence of numbers for the same seed", () => {
    const first = createSeededRandomSource(42);
    const second = createSeededRandomSource(42);

    const firstValues = Array.from({ length: 10 }, () => first());
    const secondValues = Array.from({ length: 10 }, () => second());

    expect(firstValues).toEqual(secondValues);
  });

  it("produces different sequences for different seeds", () => {
    const first = createSeededRandomSource(1);
    const second = createSeededRandomSource(2);

    const firstValues = Array.from({ length: 10 }, () => first());
    const secondValues = Array.from({ length: 10 }, () => second());

    expect(firstValues).not.toEqual(secondValues);
  });

  it("always returns values within [0, 1)", () => {
    const random = createSeededRandomSource(7);

    for (let i = 0; i < 1000; i++) {
      const value = random();
      expect(value).toBeGreaterThanOrEqual(0);
      expect(value).toBeLessThan(1);
    }
  });
});
