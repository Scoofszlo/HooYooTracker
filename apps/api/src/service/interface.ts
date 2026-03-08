import type { RedeemCode } from "@hooyootracker/core";
import type { RedeemCodeScraper } from "../scrapers/interface.ts";
import type { GameQuery, RedeemCodeServiceDeps } from "../types.ts";
import { getUniqueCodes } from "./helper.ts";

export class RedeemCodeService {
  private giScrapers: RedeemCodeScraper[];
  private zzzScrapers: RedeemCodeScraper[];

  constructor(scrapers: RedeemCodeServiceDeps) {
    this.giScrapers = scrapers.giScrapers || [];
    this.zzzScrapers = scrapers.zzzScrapers || [];
  }

  async getCodes(game: GameQuery): Promise<RedeemCode[]> {
    if (game != "gi" && game != "zzz") {
      throw new Error(`Unsupported game query: ${game}`);
    }

    const scrapers = game === "gi" ? this.giScrapers : this.zzzScrapers;
    const allResults = await Promise.all(
      scrapers.map((scraper) => scraper.scrape()),
    );
    const flattenedResults = allResults.flat();

    return getUniqueCodes(flattenedResults);
  }
}
