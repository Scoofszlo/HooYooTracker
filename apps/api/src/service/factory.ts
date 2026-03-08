import { GIGame8Scraper } from "../scrapers/gi/game8.ts";
import { GIRockPaperShotgunScraper } from "../scrapers/gi/rockpapershotgun.ts";
import { GIVG247Scraper } from "../scrapers/gi/vg247.ts";
import { ZZZGame8Scraper } from "../scrapers/zzz/game8.ts";
import { ZZZPCGamesNScraper } from "../scrapers/zzz/pcgamesn.ts";
import { ZZZVG247Scraper } from "../scrapers/zzz/vg247.ts";
import { RedeemCodeService } from "./interface.ts";

export function createRedeemCodeService(): RedeemCodeService {
  return new RedeemCodeService({
    giScrapers: [
      new GIGame8Scraper(),
      new GIRockPaperShotgunScraper(),
      new GIVG247Scraper(),
    ],
    zzzScrapers: [
      new ZZZGame8Scraper(),
      new ZZZPCGamesNScraper(),
      new ZZZVG247Scraper(),
    ],
  });
}
