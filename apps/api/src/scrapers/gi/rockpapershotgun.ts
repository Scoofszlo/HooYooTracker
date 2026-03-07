import type { RedeemCode } from "@hooyootracker/core";
import axios from "axios";
import * as cheerio from "cheerio";
import { GI_SOURCES } from "../../constants.ts";
import type { RedeemCodeScraper } from "../base.ts";

export class GIRockPaperShotgunScraper implements RedeemCodeScraper {
  sourceName: string = GI_SOURCES.ROCK_PAPER_SHOTGUN.name;

  async scrape(): Promise<RedeemCode[]> {
    const data = await axios.get(GI_SOURCES.ROCK_PAPER_SHOTGUN.url);
    const results: RedeemCode[] = [];
    const $ = cheerio.load(data.data);
    // Select the first ul element inside the article body content and get its li children
    const li = $("div.article_body_content > ul:eq(0) li");

    li.each((_, element) => {
      const $li = $(element);
      const code = $li.find("strong").text().trim();
      const description = $li
        .text()
        .replace(/\w+:\s+/g, "")
        .trim();
      results.push({
        source: this.sourceName,
        code: code,
        description: description,
      });
    });

    return results;
  }
}
