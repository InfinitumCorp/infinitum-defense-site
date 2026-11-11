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

```bash
vercel deploy --prod
```

Pushes to `main` deploy to production automatically through Vercel's GitHub integration.
`.vercelignore` keeps the sources (`src/`, `build.py`, `i18n.json`, `services.json`) out of the deployment.

After a production deploy, tell Bing, Yandex and other IndexNow engines about the changed pages:

```bash
python indexnow.py
```
