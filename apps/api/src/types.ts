import type { RedeemCodeScraper } from "./srapers/base.ts";

export type RedeemCodeServiceConstructor = {
  giScrapers?: RedeemCodeScraper[];
  zzzScrapers?: RedeemCodeScraper[];
};

export type GameQuery = "gi" | "zzz";
