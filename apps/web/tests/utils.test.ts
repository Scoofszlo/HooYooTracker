import { describe, expect, it } from "vitest";
import { formatElapsed } from "../src/utils/index";

describe("formatElapsed", () => {
  it("formats seconds", () => {
    expect(formatElapsed(15_000)).toBe("15s");
  });

  it("formats minutes and seconds", () => {
    expect(formatElapsed(125_000)).toBe("2m 5s");
  });

  it("formats days, hours, minutes, seconds", () => {
    expect(formatElapsed(90_061_000)).toBe("1d 1h 1m 1s");
  });
});
