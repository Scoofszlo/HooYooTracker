import type { RedeemCodeScraper } from "./scrapers/interface.ts";

export type RedeemCodeServiceDeps = {
  giScrapers?: RedeemCodeScraper[];
  zzzScrapers?: RedeemCodeScraper[];
};

export type GameQuery = "gi" | "zzz";
