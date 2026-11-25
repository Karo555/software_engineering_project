import js from "@eslint/js";
import prettier from "eslint-config-prettier/flat";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import { defineConfig, globalIgnores } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";

export default defineConfig([
  globalIgnores(["dist/", "coverage/"]),
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    extends: [js.configs.recommended],
  },
  {
    files: ["**/*.{ts,mts,cts,tsx}"],
    extends: [tseslint.configs.recommended],
  },
  {
    files: ["src/**/*.{js,jsx,ts,tsx}"],
    extends: [reactHooks.configs.flat.recommended, reactRefresh.configs.vite],
    languageOptions: { globals: globals.browser },
  },
  {
    // Tool configuration at the package root runs in Node, not in the browser.
    files: ["*.{js,mjs,cjs,ts,mts,cts}"],
    languageOptions: { globals: globals.node },
  },
  // Keep last: turns off the ESLint rules that would conflict with Prettier.
  prettier,
]);
