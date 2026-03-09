import type { RedeemCode } from "@hooyootracker/core";
import express from "express";
import request from "supertest";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { codesRouter } from "../src/routes/codes.ts";

const { mockGetCodes } = vi.hoisted(() => ({
  mockGetCodes: vi.fn(),
}));

vi.mock("../src/service/factory.ts", () => ({
  redeemCodeService: {
    getCodes: mockGetCodes,
  },
}));

function makeCode(code: string): RedeemCode {
  return {
    code,
    description: `${code} description`,
    source: {
      name: "test-source",
      url: "https://example.com/source",
    },
  };
}

describe("GET /api/codes", () => {
  beforeEach(() => {
    mockGetCodes.mockReset();
  });

  it("returns 400 for missing game query", async () => {
    const app = express();
    app.use("/api", codesRouter);

    const response = await request(app).get("/api/codes");

    expect(response.status).toBe(400);
    expect(response.body).toEqual({
      error: "Invalid query parameter. Expected 'game=gi' or 'game=zzz'.",
    });
    expect(mockGetCodes).not.toHaveBeenCalled();
  });

  it("returns codes when query is valid", async () => {
    const expectedCodes = [makeCode("GI123")];
    mockGetCodes.mockResolvedValue(expectedCodes);

    const app = express();
    app.use("/api", codesRouter);

    const response = await request(app).get("/api/codes?game=gi");

    expect(response.status).toBe(200);
    expect(mockGetCodes).toHaveBeenCalledWith("gi");
    expect(response.body.codes).toEqual(expectedCodes);
    expect(typeof response.body.date).toBe("string");
  });

  it("returns 500 when service throws", async () => {
    mockGetCodes.mockRejectedValue(new Error("boom"));

    const app = express();
    app.use("/api", codesRouter);

    const response = await request(app).get("/api/codes?game=zzz");

    expect(response.status).toBe(500);
    expect(response.body.error).toContain("Failed to fetch codes");
  });
});
