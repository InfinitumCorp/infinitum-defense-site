# Infinitum Defense

Website for Infinitum Defense, the defensive arm of Infinitum Corporation, headquartered in Washington, D.C.

- Live: https://infinitumdefense.com (English at `/`, Russian at `/ru`)
- Static site with a small Python build step for the two languages.

## Edit the copy

All page text lives in `i18n.json`, with an `en` and `ru` value for every string. Layout and code live in
`src/index.template.html`. After changing either, rebuild:

```bash
python build.py
```

This writes `index.html` (English) and `ru/index.html` (Russian), plus everything generated from
`services.json`: the services hub (`/services`, `/ru/services`), one page per service in each language,
`404.html`, `sitemap.xml` and `llms.txt`. Don't edit generated files by hand; the build overwrites them. Both pages carry the whole dictionary, so the EN/RU switch in the header swaps the
text in place without a reload.

## Deploy

infinitumdefense.com is served by the Cloudflare Worker `infinitum-defense-site` (DNS for the domain is on
Cloudflare). `python build.py` also copies the public files into `dist/`, and the Worker serves that folder.

```bash
npm install
npm run deploy
```

`npm run deploy` rebuilds, then runs `cf deploy`, which uploads `dist/` and keeps the custom domain attached.
Settings live in `cloudflare.config.ts` (Worker name, domain, 404 handling) and `wrangler.config.ts` (assets
folder). Response headers come from `src/_headers`. Only an allowlist of files in `build.py` goes into
`dist/`, so sources and `.env` files are never uploaded.

Cloudflare caches pages, so after a deploy purge the changed URLs (or everything) in the Cloudflare dashboard
under Caching > Configuration, or with `cf cache purge`.

The Vercel project (`vercel deploy --prod`) is a mirror at infinitumdefense.vercel.app, which redirects to
the domain. `.vercelignore` keeps the sources and the Cloudflare files out of it.

After a production deploy, tell Bing, Yandex and other IndexNow engines about the changed pages:

```bash
python indexnow.py
```
