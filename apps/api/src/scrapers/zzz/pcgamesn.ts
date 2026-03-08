import type { RedeemCode } from "@hooyootracker/core";
import axios from "axios";
import * as cheerio from "cheerio";
import { ZZZ_SOURCES } from "../../constants.ts";
import type { RedeemCodeScraper } from "../base.ts";

export class ZZZPCGamesNScraper implements RedeemCodeScraper {
  sourceName: string = ZZZ_SOURCES.PCGAMESN.name;

  async scrape(): Promise<RedeemCode[]> {
    const data = await axios.get(ZZZ_SOURCES.PCGAMESN.url);
    const results: RedeemCode[] = [];
    const $ = cheerio.load(data.data);
    const rows = $("div.entry-content ul:eq(0) li");

    rows.each((_, element) => {
      const $li = $(element);
      const code = $li.find("strong:eq(0)").text().trim();
      const description = $li
        .text()
        .replace(/\w+\s+-\s+/g, "")
        .trim();

      results.push({
        source: {
          name: ZZZ_SOURCES.PCGAMESN.name,
          url: ZZZ_SOURCES.PCGAMESN.url,
        },
        code: code,
        description: description,
      });
    });

    return results;
  }
}
