import js from "@eslint/js";
import eslintPluginPrettier from "eslint-plugin-prettier/recommended";
import { defineConfig } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";

export default defineConfig([
  tseslint.configs.recommended,
  eslintPluginPrettier,
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts}"],
    plugins: { js },
    extends: ["js/recommended"],
    languageOptions: {
      globals: globals.node
    }
  },
  {
    ignores: ["dist", "node_modules"],
  }
]);
