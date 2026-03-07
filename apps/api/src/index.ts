import cors from "cors";
import express, { type Request, type Response } from "express";
import { GIGame8Scraper } from "./scrapers/gi/game8.ts";
import { GIRockPaperShotgunScraper } from "./scrapers/gi/rockpapershotgun.ts";
import { GIVG247Scraper } from "./scrapers/gi/vg247.ts";
import { ZZZGame8Scraper } from "./scrapers/zzz/game8.ts";
import { ZZZPCGamesNScraper } from "./scrapers/zzz/pcgamesn.ts";
import { ZZZVG247Scraper } from "./scrapers/zzz/vg247.ts";
import { RedeemCodeService } from "./service/index.ts";
import type { GameQuery } from "./types.ts";

const app = express();
app.use(cors());
const port = process.env["PORT"] || 3000;

const service = new RedeemCodeService({
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

app.get("/api/codes", async (req: Request, res: Response) => {
  const query = req.query["game"] as GameQuery;

  if (!query || (query !== "gi" && query !== "zzz")) {
    return res.status(400).json({
      error: "Invalid query parameter. Expected 'game=gi' or 'game=zzz'.",
    });
  }

  return service
    .getCodes(query)
    .then((codes) => {
      res.json({
        codes,
        date: new Date().toISOString(),
      });
    })
    .catch((error) => {
      console.error("Error fetching codes:", error);
      res.status(500).json({ error: `Failed to fetch codes: ${error}` });
    });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
