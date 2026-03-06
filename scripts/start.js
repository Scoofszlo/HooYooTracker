import { execSync } from "child_process";
import { existsSync, readFileSync, writeFileSync } from "fs";
import { dirname, resolve } from "path";
import { fileURLToPath } from "url";

// Get the directory of the current script
const __dirname = dirname(fileURLToPath(import.meta.url));

// Get the current version of the project
const rootPkg = JSON.parse(readFileSync(resolve(__dirname, "../package.json"), "utf-8"));
const currentVersion = rootPkg.version;

const builtVersionPath = resolve(__dirname, "../.hooyootracker-version");
const builtVersion = existsSync(builtVersionPath)
  ? readFileSync(builtVersionPath, "utf-8").trim()
  : null;

const isNewVersion = builtVersion !== currentVersion;

if (isNewVersion && builtVersion) {
  console.log(`🆕 New version detected: ${builtVersion} → ${currentVersion}. Rebuilding...`);
}

const nodeModules = resolve(__dirname, "../node_modules");

if (!existsSync(nodeModules)) {
  console.log("📦 Installing dependencies...");
  execSync("npm install", { stdio: "inherit", cwd: resolve(__dirname, "..") });
  console.log("✅ Dependencies installed.");
} else if (isNewVersion) {
  console.log("📦 Reinstalling dependencies for new version...");
  execSync("npm install", { stdio: "inherit", cwd: resolve(__dirname, "..") });
} else {
  console.log("✅ Dependencies already installed, skipping...");
}

const webDist = resolve(__dirname, "../apps/web/dist");
const apiDist = resolve(__dirname, "../apps/api/dist");

const isWebBuilt = existsSync(webDist) && !isNewVersion;
const isApiBuilt = existsSync(apiDist) && !isNewVersion;

if (!isWebBuilt) {
  process.stdout.write("🔨 Building front-end...");
  execSync("npm run build -w apps/web", { stdio: "ignore" });
  process.stdout.write("\r✅ Front-end built successfully.\n");
} else {
  console.log("✅ Web app already built, skipping...");
}

if (!isApiBuilt) {
  process.stdout.write("🔨 Building backend API...");
  execSync("npm run build -w apps/api", { stdio: "ignore" });
  process.stdout.write("\r✅ Backend API built successfully.\n");
} else {
  console.log("✅ API already built, skipping...");
}

// Save current version as the last built version
writeFileSync(builtVersionPath, currentVersion);

console.log("🚀 Starting HooYooTracker...\n");
execSync(
  "concurrently --kill-others --names \"API,WEB\" --prefix-colors \"blue,green\" \"npm run start -w apps/api\" \"npm run start -w apps/web\"",
  { stdio: "inherit" }
);
