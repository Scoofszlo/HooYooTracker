import { Router, type Request, type Response } from "express";
import { createRedeemCodeService } from "../service/factory.ts";
import type { RedeemCodeService } from "../service/interface.ts";

type RedeemCodeServiceLike = Pick<RedeemCodeService, "getCodes">;

export function createCodesRouter(
  service: RedeemCodeServiceLike = createRedeemCodeService(),
) {
  const codesRouter = Router();

  codesRouter.get("/codes", (req: Request, res: Response) => {
    const query = req.query["game"];

    if (query !== "gi" && query !== "zzz") {
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

  return codesRouter;
}

export const codesRouter = createCodesRouter();
