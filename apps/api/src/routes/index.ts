import type { Express } from "express";
import type { RedeemCodeService } from "../service/interface.ts";
import { codesRouter, createCodesRouter } from "./codes.ts";

export function registerRoutes(
  app: Express,
  service?: Pick<RedeemCodeService, "getCodes">,
): void {
  app.use("/api", service ? createCodesRouter(service) : codesRouter);
}
