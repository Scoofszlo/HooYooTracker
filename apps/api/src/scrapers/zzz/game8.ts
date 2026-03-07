import type { RedeemCode } from "@hooyootracker/core";
import axios from "axios";
import * as cheerio from "cheerio";
import { ZZZ_SOURCES } from "../../constants.ts";
import type { RedeemCodeScraper } from "../base.ts";

export class ZZZGame8Scraper implements RedeemCodeScraper {
  sourceName: string = ZZZ_SOURCES.GAME8.name;

  async scrape(): Promise<RedeemCode[]> {
    const data = await axios.get(ZZZ_SOURCES.GAME8.url);
    const results: RedeemCode[] = [];
    const $ = cheerio.load(data.data);
    const rows = $("table.a-table:first tbody tr:gt(0)"); // Select all rows except the header row

    rows.each((_, element) => {
      const $row = $(element);
      const code = $row.find("input").val() as string; // Get the value of the input element
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
      }; // Get the text of the second td element

      results.push({
        source: this.sourceName,
        code: code,
        description: description(),
      });
    });

    return results;
  }
}
