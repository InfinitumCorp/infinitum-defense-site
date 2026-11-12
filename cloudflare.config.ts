import { defineConfig } from "cf/config";

// infinitumdefense.com: the files build.py writes to dist/, served by this Worker on the custom domain.
export default defineConfig({
  worker: {
    name: "infinitum-defense-site",
    compatibilityDate: "2026-11-04",
    observability: { enabled: true },
    assets: { htmlHandling: "drop-trailing-slash", notFoundHandling: "404-page" },
    domains: ["infinitumdefense.com"],
  },
});
