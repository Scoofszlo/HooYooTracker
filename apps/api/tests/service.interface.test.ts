import type { RedeemCode } from "@hooyootracker/core";
import type { RedeemCodeScraper } from "../src/scrapers/interface.ts";
import type { GameQuery } from "../src/types.ts";
import { RedeemCodeService } from "../src/service/interface.ts";
import { describe, expect, it, vi } from "vitest";

function makeCode(code: string, sourceName: string): RedeemCode {
  return {
    code,
    description: `${code} description`,
    source: {
      name: sourceName,
      url: `https://example.com/${sourceName}`,
    },
  };
}

describe("RedeemCodeService", () => {
  it("deduplicates codes returned by scrapers", async () => {
    const repeatedCode = makeCode("ABC123", "source1");
    const repeatedCode2 = makeCode("DEF456", "source2");

    const giScraperA: RedeemCodeScraper = {
      sourceName: "a",
      scrape: vi.fn().mockResolvedValue([makeCode("GI777", "a")]),
    };

    const giScraperB: RedeemCodeScraper = {
      sourceName: "b",
      scrape: vi.fn().mockResolvedValue([makeCode("GI888", "b")]),
    };

    const giScraperC: RedeemCodeScraper = {
      sourceName: "c",
      scrape: vi.fn().mockResolvedValue(repeatedCode),
    };

    const giScraperD: RedeemCodeScraper = {
      sourceName: "d",
      scrape: vi.fn().mockResolvedValue(repeatedCode),
    };

    const giScraperE: RedeemCodeScraper = {
      sourceName: "d",
      scrape: vi.fn().mockResolvedValue(repeatedCode2),
    };

    const giScraperF: RedeemCodeScraper = {
      sourceName: "d",
      scrape: vi.fn().mockResolvedValue(repeatedCode2),
    };

    const service = new RedeemCodeService({
      giScrapers: [
        giScraperA,
        giScraperB,
        giScraperC,
        giScraperD,
        giScraperE,
        giScraperF,
      ],
      zzzScrapers: [],
    });

    const result = await service.getCodes("gi");
    expect(result.map((code) => code.code)).toEqual([
      "GI777",
      "GI888",
      "ABC123",
      "DEF456",
    ]);
  });

  it("uses only scrapers for the requested game", async () => {
    const giScraper: RedeemCodeScraper = {
      sourceName: "gi",
      scrape: vi.fn().mockResolvedValue([makeCode("GI111", "gi")]),
    };

    const zzzScraper: RedeemCodeScraper = {
      sourceName: "zzz",
      scrape: vi.fn().mockResolvedValue([makeCode("ZZZ111", "zzz")]),
    };

    const service = new RedeemCodeService({
      giScrapers: [giScraper],
      zzzScrapers: [zzzScraper],
    });

    await service.getCodes("gi");

    expect(giScraper.scrape).toHaveBeenCalledTimes(1);
    expect(zzzScraper.scrape).not.toHaveBeenCalled();
  });

  it("throws when game query is unsupported", async () => {
    const service = new RedeemCodeService({ giScrapers: [], zzzScrapers: [] });

    await expect(service.getCodes("hsr" as GameQuery)).rejects.toThrow(
      "Unsupported game query",
    );
  });
});
