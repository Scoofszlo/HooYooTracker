import type { RedeemCode } from "@hooyootracker/core";
import axios from "axios";
import * as cheerio from "cheerio";
import { GI_SOURCES } from "../../constants.ts";
import type { RedeemCodeScraper } from "../../scrapers/base.ts";

export class GIGame8Scraper implements RedeemCodeScraper {
  sourceName: string = GI_SOURCES.GAME8.name;

  async scrape(): Promise<RedeemCode[]> {
    const data = await axios.get(GI_SOURCES.GAME8.url);
    const results: RedeemCode[] = [];
    const $ = cheerio.load(data.data);
    const rows = $("table.a-table:first tbody tr:gt(0)"); // Select all rows except the header row

    rows.each((_, element) => {
      const $row = $(element);
      const code = $row.find("input").val() as string;
      const description = () => {
        const td = $row.find("td:nth-child(2)");
        const divs = td.find("div");

        const rewards: string[] = [];
        divs.each((_, div) => {
          const text = $(div)
            .text()
            .replace(/\s{2,}/g, " ")
            .trim();
          rewards.push(text);
        });

        return rewards.join(", ");
      };

      results.push({
        source: {
          name: GI_SOURCES.GAME8.name,
          url: GI_SOURCES.GAME8.url,
        },
        code: code,
        description: description(),
      });
    });

    return results;
  }
}
