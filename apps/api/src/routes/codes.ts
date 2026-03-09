import { Router, type Request, type Response } from "express";
import { redeemCodeService } from "../service/factory.ts";

export const codesRouter = Router();

codesRouter.get("/codes", (req: Request, res: Response) => {
  const query = req.query["game"];

  if (query !== "gi" && query !== "zzz") {
    return res.status(400).json({
      error: "Invalid query parameter. Expected 'game=gi' or 'game=zzz'.",
    });
  }

  return redeemCodeService
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
