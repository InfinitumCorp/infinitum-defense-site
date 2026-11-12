import { defineWranglerConfig } from "wrangler/experimental-config";

// Cloudflare serves the static files that build.py assembles in dist/.
export default defineWranglerConfig({
  "assetsDirectory": "./dist"
});
