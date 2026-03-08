import type { RedeemCode } from "@hooyootracker/core";
import type { RedeemCodeScraper } from "../scrapers/interface.ts";
import type { GameQuery, RedeemCodeServiceDeps } from "../types.ts";

export class RedeemCodeService {
  private giScrapers: RedeemCodeScraper[];
  private zzzScrapers: RedeemCodeScraper[];

  constructor(scrapers: RedeemCodeServiceDeps) {
    this.giScrapers = scrapers.giScrapers || [];
    this.zzzScrapers = scrapers.zzzScrapers || [];
  }

  async getCodes(game: GameQuery): Promise<RedeemCode[]> {
    if (game === "gi") {
      return this.getUniqueCodesFromScrapers(this.giScrapers);
    }

    if (game === "zzz") {
      return this.getUniqueCodesFromScrapers(this.zzzScrapers);
    }

    throw new Error(`Unsupported game query: ${game}`);
  }

  private async getUniqueCodesFromScrapers(
    scrapers: RedeemCodeScraper[],
  ): Promise<RedeemCode[]> {
    const allResults = await Promise.all(
      scrapers.map((scraper) => scraper.scrape()),
    );
    const flattenedResults = allResults.flat();
    const uniqueMap = new Map<string, RedeemCode>();

    flattenedResults.forEach((code) => {
      if (!uniqueMap.has(code.code)) {
        uniqueMap.set(code.code, code);
      }
    });

    return Array.from(uniqueMap.values());
  }
}
