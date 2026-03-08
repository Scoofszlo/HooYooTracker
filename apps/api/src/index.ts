import cors from "cors";
import express from "express";
import { registerRoutes } from "./routes/index.ts";

const port = process.env["PORT"] || 3000;
const app = express();

app.use(cors());
registerRoutes(app);

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
