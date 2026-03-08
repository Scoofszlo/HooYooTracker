import express from "express";
import request from "supertest";
import type { RedeemCode } from "@hooyootracker/core";
import { createCodesRouter } from "../src/routes/codes.ts";
import { describe, expect, it, vi } from "vitest";

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
  it("returns 400 for missing game query", async () => {
    const mockService = {
      getCodes: vi.fn(),
    };

    const app = express();
    app.use("/api", createCodesRouter(mockService));

    const response = await request(app).get("/api/codes");

    expect(response.status).toBe(400);
    expect(response.body).toEqual({
      error: "Invalid query parameter. Expected 'game=gi' or 'game=zzz'.",
    });
    expect(mockService.getCodes).not.toHaveBeenCalled();
  });

  it("returns codes when query is valid", async () => {
    const expectedCodes = [makeCode("GI123")];
    const mockService = {
      getCodes: vi.fn().mockResolvedValue(expectedCodes),
    };

    const app = express();
    app.use("/api", createCodesRouter(mockService));

    const response = await request(app).get("/api/codes?game=gi");

    expect(response.status).toBe(200);
    expect(mockService.getCodes).toHaveBeenCalledWith("gi");
    expect(response.body.codes).toEqual(expectedCodes);
    expect(typeof response.body.date).toBe("string");
  });

  it("returns 500 when service throws", async () => {
    const mockService = {
      getCodes: vi.fn().mockRejectedValue(new Error("boom")),
    };

    const app = express();
    app.use("/api", createCodesRouter(mockService));

    const response = await request(app).get("/api/codes?game=zzz");

    expect(response.status).toBe(500);
    expect(response.body.error).toContain("Failed to fetch codes");
  });
});
