import Router from "express";
import { createRedeemCodeService } from "../service/factory.ts";
import type { GameQuery } from "../types.ts";

const codesRouter = Router();
const service = createRedeemCodeService();

codesRouter.get("/codes", (req, res) => {
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

export { codesRouter };
