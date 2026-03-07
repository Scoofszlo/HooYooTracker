import type { RedeemCodeScraper } from "./scrapers/base.ts";

export type RedeemCodeServiceConstructor = {
  giScrapers?: RedeemCodeScraper[];
  zzzScrapers?: RedeemCodeScraper[];
};

export type GameQuery = "gi" | "zzz";
