import type { Express } from "express";
import { codesRouter } from "./codes.ts";

export function registerRoutes(app: Express): void {
  app.use("/api", codesRouter);
}
