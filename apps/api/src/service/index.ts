import type { RedeemCode } from "@hooyootracker/core";
import type { RedeemCodeScraper } from "../srapers/base.ts";
import type { GameQuery, RedeemCodeServiceConstructor } from "../types.ts";

export class RedeemCodeService {
  private giScrapers: RedeemCodeScraper[];
  private zzzScrapers: RedeemCodeScraper[];

  constructor(scrapers: RedeemCodeServiceConstructor) {
    this.giScrapers = scrapers.giScrapers || [];
    this.zzzScrapers = scrapers.zzzScrapers || [];
  }

  async getCodes(game: GameQuery): Promise<RedeemCode[]> {
    if (game === "gi") {
      const allResults = await Promise.all(
        this.giScrapers.map((scraper) => scraper.scrape()),
      );
      return allResults.flat();
    } else if (game === "zzz") {
      const allResults = await Promise.all(
        this.zzzScrapers.map((scraper) => scraper.scrape()),
      );
      return allResults.flat();
    }
    throw new Error(`Unsupported game query: ${game}`);
  }
}
