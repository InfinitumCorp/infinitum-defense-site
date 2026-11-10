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

This writes `index.html` (English) and `ru/index.html` (Russian). Don't edit those two files by hand; the
build overwrites them. Both pages carry the whole dictionary, so the EN/RU switch in the header swaps the
text in place without a reload.

## Deploy

```bash
vercel deploy --prod
```

Pushes to `main` deploy to production automatically through Vercel's GitHub integration.
`.vercelignore` keeps `src/`, `build.py` and `i18n.json` out of the deployment.
