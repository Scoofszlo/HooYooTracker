import type { RedeemCode } from "@hooyootracker/core";
import axios from "axios";
import * as cheerio from "cheerio";
import { GI_SOURCES } from "../../constants.ts";
import type { RedeemCodeScraper } from "../interface.ts";

export class GIVG247Scraper implements RedeemCodeScraper {
  sourceName: string = GI_SOURCES.VG247.name;

  async scrape(): Promise<RedeemCode[]> {
    const data = await axios.get(GI_SOURCES.VG247.url);
    const results: RedeemCode[] = [];
    const $ = cheerio.load(data.data);
    const li = $("div.article_body_content > ul:eq(1) li");

    li.each((_, element) => {
      const $li = $(element);
      const code = $li.find("strong").text().trim();
      const description = $li
        .text()
        .replace(/\w+:\s+/g, "")
        .trim();

      results.push({
        source: {
          name: GI_SOURCES.VG247.name,
          url: GI_SOURCES.VG247.url,
        },
        code: code,
        description: description,
      });
    });

    return results;
  }
}
