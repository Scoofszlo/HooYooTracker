import type { RedeemCode } from "@hooyootracker/core";

export interface RedeemCodeScraper {
  sourceName: string;
  scrape(): Promise<RedeemCode[]>;
}
