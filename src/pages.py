"""Service pages, the services hub, the 404 page and the sitemap, rendered from services.json.

Imported by build.py. Each page is plain static HTML in the home page's black-and-white style,
with its own title, description, canonical, hreflang pair and JSON-LD.
"""
import json
from html import escape, unescape

SITE = "https://infinitumdefense.com"
LANGS = ("en", "ru")

UI = {
    "en": {
        "home": "Home", "services": "Services", "cta": "Let's talk", "book": "Book a free consultation",
        "all": "All services", "includes": "What's included", "for": "Who it's for", "faq": "Questions",
        "related": "Related services", "more": "Learn more", "open": "Open 24/7", "hq": "Washington, D.C.",
        "close_h": "Tell us what you need protected.",
        "close_p": "A short consultation is free. We reply with a written plan, staffing and timeline.",
        "foot": "The defensive arm of Infinitum Corporation. Headquartered in Washington, D.C.",
        "company": "Company", "contact": "Contact", "lang": "Language", "crumbs": "Breadcrumb",
        "nf_title": "Page not found | Infinitum Defense", "nf_h": "This page doesn't exist.",
        "nf_p": "The link may be old or mistyped. Everything we do is listed on the services page.",
        "locale": "en_US", "inlang": "en-US", "og_alt": "Infinitum Defense: We protect what matters most.",
    },
    "ru": {
        "home": "Главная", "services": "Услуги", "cta": "Связаться", "book": "Бесплатная консультация",
        "all": "Все услуги", "includes": "Что входит", "for": "Для кого", "faq": "Вопросы",
        "related": "Похожие услуги", "more": "Подробнее", "open": "Работаем 24/7", "hq": "Вашингтон, округ Колумбия",
        "close_h": "Расскажите, что нужно защитить.",
        "close_p": "Короткая консультация бесплатна. В ответ вы получите письменный план, состав и сроки.",
        "foot": "Оборонное подразделение Infinitum Corporation. Штаб-квартира в Вашингтоне.",
        "company": "Компания", "contact": "Контакты", "lang": "Язык", "crumbs": "Навигационная цепочка",
        "nf_title": "Страница не найдена | Infinitum Defense", "nf_h": "Такой страницы нет.",
        "nf_p": "Возможно, ссылка устарела или в ней опечатка. Все наши услуги перечислены на странице услуг.",
        "locale": "ru_RU", "inlang": "ru-RU", "og_alt": "Infinitum Defense: Мы защищаем то, что важнее всего.",
    },
}

CSS = """
:root{--ink:#000;--panel:#111;--line:#262626;--line-strong:#4d4d4d;--fg:#f5f5f5;--muted:#a3a3a3;--dim:#6b6b6b;
--sans:"Helvetica Neue",Helvetica,Arial,sans-serif;--mono:"Geist Mono",ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;
--ease:cubic-bezier(.2,.8,.2,1);--gutter:16px;--max:1320px;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--ink);color:var(--fg);font:16px/1.55 var(--sans);-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--fg);outline-offset:3px}
.wrap{max-width:var(--max);margin:0 auto;padding-left:max(var(--gutter),env(safe-area-inset-left,0px));padding-right:max(var(--gutter),env(safe-area-inset-right,0px))}
@media(min-width:760px){:root{--gutter:40px}}
.label{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
.logo{display:inline-block;aspect-ratio:640/411;background:currentColor;-webkit-mask:url(/favicon.png) center/contain no-repeat;mask:url(/favicon.png) center/contain no-repeat}
.lockup{display:grid;justify-items:center;text-align:center;line-height:1;gap:4px}
.lockup b{font-weight:600;font-size:14px;letter-spacing:.2em;padding-left:.2em}
.lockup small{font-size:8px;letter-spacing:.5em;padding-left:.5em}
header.nav{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--ink) 92%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:32px;height:64px}
.mark{display:flex;align-items:center;gap:12px}.mark .logo{width:36px;flex:none}
.nav nav{display:flex;gap:28px;margin-left:auto}
.nav nav a{font-size:13px;color:var(--muted);padding-block:6px;border-bottom:1px solid transparent}
.nav nav a:hover,.nav nav a[aria-current=page]{color:var(--fg);border-bottom-color:var(--fg)}
@media(max-width:860px){.nav nav{display:none}.nav .btn{margin-left:auto}.nav .wrap{gap:16px}}
.btn{display:inline-flex;align-items:center;gap:10px;position:relative;overflow:hidden;isolation:isolate;font:500 14px/1 var(--sans);padding:15px 20px;border:1px solid var(--fg);background:var(--fg);color:var(--ink);transition:color .35s var(--ease)}
.btn::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--ink);transform:translateY(101%);transition:transform .45s var(--ease)}
.btn:hover::before{transform:none}.btn:hover{color:var(--fg)}
.btn.ghost{background:transparent;color:var(--fg);border-color:var(--line-strong)}.btn.ghost::before{background:var(--fg)}.btn.ghost:hover{color:var(--ink);border-color:var(--fg)}
.nav .btn{padding:10px 16px;font-size:13px;background:transparent;color:var(--fg)}.nav .btn::before{background:var(--fg)}.nav .btn:hover{color:var(--ink)}
.lang{display:flex;align-items:center;gap:6px;flex:none;font:500 12px/1 var(--mono);letter-spacing:.08em}
.lang a{color:var(--dim);padding:8px 2px;border-bottom:1px solid transparent}.lang a:hover{color:var(--fg)}
.lang a[aria-current=true]{color:var(--fg);border-bottom-color:var(--fg)}.lang i{font-style:normal;color:var(--line-strong)}
.crumbs{font-size:13px;color:var(--dim);padding-top:28px}
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.crumbs li+li::before{content:"/";margin-right:8px;color:var(--line-strong)}
.crumbs a{color:var(--muted)}.crumbs a:hover{color:var(--fg)}
.hero{border-bottom:1px solid var(--line)}
.hero .in{padding-block:clamp(48px,7vw,96px) clamp(64px,8vw,112px);max-width:900px}
h1{font-weight:400;font-size:clamp(40px,6.4vw,92px);line-height:.98;letter-spacing:-.055em;margin:18px 0 0;text-wrap:balance}
.lede{font-size:clamp(17px,1.5vw,20px);color:var(--muted);max-width:56ch;margin:28px 0 0}
.ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}
.facts{display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:40px;font-size:13px;color:var(--muted)}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--fg);margin-right:8px;vertical-align:1px}
section.band{border-bottom:1px solid var(--line)}section.band>.wrap{padding-block:clamp(64px,8vw,112px)}
.head{display:grid;grid-template-columns:1fr 2fr;gap:40px;margin-bottom:48px}
h2{font-weight:400;margin:0;font-size:clamp(30px,4vw,52px);line-height:1.04;letter-spacing:-.05em}
.grid3{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);border-top:2px solid var(--fg)}
.grid3>li{padding:24px 24px 0 0;min-width:0}.grid3>li+li{padding-left:24px;border-left:1px solid var(--line)}
.grid3 h3{font-weight:400;font-size:22px;letter-spacing:-.03em;margin:14px 0 10px}
.grid3 p{margin:0;color:var(--muted);font-size:15px}
.for{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)}
.for li{padding:18px 18px 18px 0;border-bottom:1px solid var(--line);font-size:17px}
.for li::before{content:"\\2014";color:var(--dim);margin-right:12px}
.faq details{border-top:1px solid var(--line)}.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;padding:22px 40px 22px 0;font-size:19px;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:4px;top:18px;font:400 24px/1 var(--mono);color:var(--muted);transition:transform .3s var(--ease)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq p{margin:0 0 24px;color:var(--muted);max-width:68ch}
.cards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.cards a{display:flex;flex-direction:column;gap:12px;height:100%;padding:24px;background:var(--ink);transition:background .3s}
.cards a:hover{background:var(--panel)}
.cards b{font-weight:400;font-size:22px;letter-spacing:-.03em;line-height:1.1}
.cards p{margin:0;color:var(--muted);font-size:14px}
.cards .go{margin-top:auto;font-size:13px;color:var(--fg)}
.close{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:32px}
.close p{color:var(--muted);margin:14px 0 0;max-width:52ch}
footer .wrap{padding-block:64px 40px}
.foot-top{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:32px}
.foot-top h4{font-size:12px;font-weight:400;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 16px}
.foot-top ul{list-style:none;margin:0;padding:0;display:grid;gap:10px;font-size:14px}
.foot-top a:hover{color:var(--muted)}
.foot-bot{margin-top:64px;border-top:1px solid var(--line);padding-top:22px}
@media(max-width:760px){.head{grid-template-columns:1fr;gap:12px;margin-bottom:32px}.grid3{grid-template-columns:1fr}
.grid3>li+li{padding-left:0;border-left:0;border-top:1px solid var(--line);margin-top:24px}.for{grid-template-columns:1fr}
.foot-top{grid-template-columns:1fr 1fr}.foot-top>div:first-child{grid-column:1/-1}}
"""

# Saves the reader's choice so the home page's auto-detection respects it.
LANG_JS = ('<script>document.querySelectorAll(".lang a").forEach(a=>a.addEventListener("click",()=>'
           '{try{localStorage.setItem("lang",a.dataset.lang)}catch(e){}}))</script>')


def home(lang):
    return "/" if lang == "en" else "/ru"


def prefix(lang):
    return "" if lang == "en" else "/ru"


def svc_path(lang, slug=None):
    return f"{prefix(lang)}/services" + (f"/{slug}" if slug else "")


def plain(s):
    """Text for JSON-LD and attributes: copy in services.json may hold HTML entities."""
    return unescape(s)


def ld(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1).replace("</", "<\\/")


def head(lang, title, desc, paths, og_image, ld_obj, robots="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"):
    u = UI[lang]
    other = "ru" if lang == "en" else "en"
    url = SITE + paths[lang] if paths else None
    alt = ""
    if paths:
        alt = (f'<link rel="canonical" href="{url}">\n'
               f'<link rel="alternate" hreflang="en" href="{SITE}{paths["en"]}">\n'
               f'<link rel="alternate" hreflang="ru" href="{SITE}{paths["ru"]}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{SITE}{paths["en"]}">\n')
    og = ""
    if paths:
        og = f"""<meta property="og:type" content="website">
<meta property="og:site_name" content="Infinitum Defense">
<meta property="og:locale" content="{u['locale']}">
<meta property="og:locale:alternate" content="{UI[other]['locale']}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{escape(plain(title))}">
<meta property="og:description" content="{escape(plain(desc))}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/png">
<meta property="og:image:alt" content="{escape(u['og_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(plain(title))}">
<meta name="twitter:description" content="{escape(plain(desc))}">
<meta name="twitter:image" content="{SITE}/{og_image}">
<meta name="twitter:image:alt" content="{escape(u['og_alt'])}">
"""
    ld_tag = f'<script type="application/ld+json">\n{ld(ld_obj)}\n</script>\n' if ld_obj else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{escape(plain(desc))}">
{alt}<meta name="robots" content="{robots}">
<meta name="theme-color" content="#000000">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="US-DC">
<meta name="geo.placename" content="Washington, D.C.">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{og}{ld_tag}<style>{CSS}</style>
</head>
<body>
"""


def header(lang, paths, current=None):
    u = UI[lang]
    lang_links = ""
    if paths:
        on = ' aria-current="true"'
        en_cur, ru_cur = (on, "") if lang == "en" else ("", on)
        lang_links = (f'<div class="lang" role="group" aria-label="{u["lang"]}">'
                      f'<a href="{paths["en"]}" hreflang="en" lang="en" data-lang="en"{en_cur}>EN</a>'
                      f'<i aria-hidden="true">/</i>'
                      f'<a href="{paths["ru"]}" hreflang="ru" lang="ru" data-lang="ru"{ru_cur}>RU</a></div>')
    cur = ' aria-current="page"' if current == "services" else ""
    return f"""<header class="nav">
  <div class="wrap">
    <a class="mark" href="{home(lang)}" aria-label="Infinitum Defense — {u['home']}"><i class="logo" aria-hidden="true"></i><span class="lockup"><b>INFINITUM</b><small>DEFENSE</small></span></a>
    <nav aria-label="{u['services']}">
      <a href="{home(lang)}">{u['home']}</a>
      <a href="{svc_path(lang)}"{cur}>{u['services']}</a>
      <a href="{home(lang)}#about">{UI[lang]['company']}</a>
    </nav>
    <a class="btn" href="{home(lang)}#contact">{u['cta']}</a>
    {lang_links}
  </div>
</header>
"""


def footer(lang, data):
    u = UI[lang]
    svcs = data["services"]
    order = data["order"]
    col = lambda slugs: "".join(f'<li><a href="{svc_path(lang, s)}">{svcs[s][lang]["name"]}</a></li>' for s in slugs)
    return f"""<footer>
  <div class="wrap">
    <div class="foot-top">
      <div>
        <a class="mark" href="{home(lang)}"><i class="logo" aria-hidden="true"></i><span class="lockup"><b>INFINITUM</b><small>DEFENSE</small></span></a>
        <p style="color:var(--muted);max-width:34ch;margin:18px 0 0;font-size:14px">{u['foot']}</p>
      </div>
      <div><h4>{u['services']}</h4><ul>{col(order[:4])}</ul></div>
      <div><h4>&nbsp;</h4><ul>{col(order[4:])}</ul></div>
      <div><h4>{u['company']}</h4><ul><li><a href="{home(lang)}">{u['home']}</a></li><li><a href="{svc_path(lang)}">{u['all']}</a></li><li><a href="{home(lang)}#about">{u['company']}</a></li><li><a href="{home(lang)}#contact">{u['contact']}</a></li></ul></div>
    </div>
    <div class="foot-bot label">© 2026 Infinitum Defense Contracting Inc.</div>
  </div>
</footer>
{LANG_JS}
</body>
</html>
"""


def crumbs(lang, trail):
    u = UI[lang]
    items = "".join(
        f'<li><a href="{href}">{name}</a></li>' if href else f'<li aria-current="page">{name}</li>'
        for name, href in trail)
    return f'<nav class="crumbs wrap" aria-label="{u["crumbs"]}"><ol>{items}</ol></nav>'


def crumbs_ld(trail, page_url):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": plain(name), "item": SITE + href if href else page_url}
            for i, (name, href) in enumerate(trail)
        ],
    }


def close_band(lang):
    u = UI[lang]
    return f"""<section class="band"><div class="wrap close">
  <div><h2>{u['close_h']}</h2><p>{u['close_p']}</p></div>
  <a class="btn" href="{home(lang)}#contact">{u['book']} <span aria-hidden="true">→</span></a>
</div></section>
"""


def service_page(lang, slug, data, groups):
    s = data["services"][slug]
    c = s[lang]
    u = UI[lang]
    paths = {l: svc_path(l, slug) for l in LANGS}
    url = SITE + paths[lang]
    og_image = "og-image.png" if lang == "en" else "og-image-ru.png"
    trail = [(u["home"], home(lang)), (u["services"], svc_path(lang)), (c["name"], None)]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage", "@id": url + "#webpage", "url": url, "name": plain(c["title"]),
                "description": plain(c["desc"]), "inLanguage": u["inlang"],
                "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": url + "#service"},
                "breadcrumb": {"@id": url + "#breadcrumb"},
            },
            {
                "@type": "Service", "@id": url + "#service", "name": plain(c["name"]),
                "serviceType": plain(c["name"]), "description": plain(c["lede"]), "url": url,
                "provider": {"@id": f"{SITE}/#org"},
                "areaServed": [{"@type": "City", "name": "Washington, D.C."}, {"@type": "Country", "name": "United States"}],
                "hasOfferCatalog": {
                    "@type": "OfferCatalog", "name": plain(c["name"]),
                    "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": plain(h), "description": plain(p)}} for h, p in c["includes"]],
                },
            },
            {**crumbs_ld(trail, url), "@id": url + "#breadcrumb"},
            {
                "@type": "FAQPage", "@id": url + "#faq", "inLanguage": u["inlang"],
                "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in c["faq"]],
            },
        ],
    }
    num = data["order"].index(slug) + 1
    includes = "".join(f'<li><span class="mono label">{i + 1:02d}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(c["includes"]))
    fors = "".join(f"<li>{x}</li>" for x in c["for"])
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faq"])
    rel = "".join(
        f'<li><a href="{svc_path(lang, r)}"><span class="label">{groups[data["services"][r]["group"]][lang]}</span>'
        f'<b>{data["services"][r][lang]["name"]}</b><p>{data["services"][r][lang]["lede"].split(". ")[0].rstrip(".")}.</p>'
        f'<span class="go">{u["more"]} →</span></a></li>'
        for r in s["related"])
    body = f"""{header(lang, paths, "services")}{crumbs(lang, trail)}
<main>
<section class="hero"><div class="wrap"><div class="in">
  <div class="label"><span class="mono">{num:02d}</span> · {groups[s['group']][lang]}</div>
  <h1>{c['h1']}</h1>
  <p class="lede">{c['lede']}</p>
  <div class="ctas"><a class="btn" href="{home(lang)}#contact">{u['book']} <span aria-hidden="true">→</span></a><a class="btn ghost" href="{svc_path(lang)}">{u['all']}</a></div>
  <div class="facts"><span><i class="dot"></i>{u['open']}</span><span>{u['hq']}</span></div>
</div></div></section>
<section class="band"><div class="wrap">
  <div class="head"><div class="label">{u['includes']}</div><h2>{c['name']}</h2></div>
  <ul class="grid3">{includes}</ul>
</div></section>
<section class="band"><div class="wrap">
  <div class="head"><div class="label">{u['for']}</div><ul class="for">{fors}</ul></div>
</div></section>
<section class="band faq"><div class="wrap">
  <div class="head"><div class="label">{u['faq']}</div><div>{faqs}</div></div>
</div></section>
<section class="band"><div class="wrap">
  <div class="head"><div class="label">{u['related']}</div><div></div></div>
  <ul class="cards">{rel}</ul>
</div></section>
{close_band(lang)}</main>
"""
    return head(lang, c["title"], c["desc"], paths, og_image, graph) + body + footer(lang, data)


def hub_page(lang, data, groups):
    h = data["hub"][lang]
    u = UI[lang]
    paths = {l: svc_path(l) for l in LANGS}
    url = SITE + paths[lang]
    og_image = "og-image.png" if lang == "en" else "og-image-ru.png"
    trail = [(u["home"], home(lang)), (u["services"], None)]
    order = data["order"]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": plain(h["title"]),
                "description": plain(h["desc"]), "inLanguage": u["inlang"], "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/#org"}, "breadcrumb": {"@id": url + "#breadcrumb"},
                "mainEntity": {"@id": url + "#list"},
            },
            {
                "@type": "ItemList", "@id": url + "#list",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "url": SITE + svc_path(lang, s), "name": plain(data["services"][s][lang]["name"])}
                    for i, s in enumerate(order)
                ],
            },
            {**crumbs_ld(trail, url), "@id": url + "#breadcrumb"},
        ],
    }
    cards = "".join(
        f'<li><a href="{svc_path(lang, s)}"><span class="label"><span class="mono">{i + 1:02d}</span> · {groups[data["services"][s]["group"]][lang]}</span>'
        f'<b>{data["services"][s][lang]["name"]}</b><p>{data["services"][s][lang]["desc"]}</p>'
        f'<span class="go">{u["more"]} →</span></a></li>'
        for i, s in enumerate(order))
    body = f"""{header(lang, paths, "services")}{crumbs(lang, trail)}
<main>
<section class="hero"><div class="wrap"><div class="in">
  <div class="label">Infinitum Defense</div>
  <h1>{h['h1']}</h1>
  <p class="lede">{h['lede']}</p>
  <div class="ctas"><a class="btn" href="{home(lang)}#contact">{u['book']} <span aria-hidden="true">→</span></a></div>
  <div class="facts"><span><i class="dot"></i>{u['open']}</span><span>{u['hq']}</span></div>
</div></div></section>
<section class="band"><div class="wrap"><ul class="cards">{cards}</ul></div></section>
{close_band(lang)}</main>
"""
    return head(lang, h["title"], h["desc"], paths, og_image, graph) + body + footer(lang, data)


def not_found_page(data):
    """One bilingual 404. Served for any missing path, so it is noindex and has no canonical."""
    en, ru = UI["en"], UI["ru"]
    body = f"""{header("en", None)}
<main>
<section class="hero"><div class="wrap"><div class="in">
  <div class="label mono">404</div>
  <h1>{en['nf_h']}</h1>
  <p class="lede">{en['nf_p']}</p>
  <p class="lede" lang="ru">{ru['nf_h']} {ru['nf_p']}</p>
  <div class="ctas"><a class="btn" href="/services">{en['all']} <span aria-hidden="true">→</span></a><a class="btn ghost" href="/">{en['home']}</a><a class="btn ghost" href="/ru/services" lang="ru">{ru['all']}</a></div>
</div></div></section>
</main>
"""
    return head("en", en["nf_title"], en["nf_p"], None, None, None, robots="noindex, follow") + body + footer("en", data)


def sitemap(data, lastmod):
    """Every indexable page, each with its EN/RU alternates."""
    pairs = [({"en": "/", "ru": "/ru"}, ("og-image.png", "og-image-ru.png"))]
    pairs.append(({l: svc_path(l) for l in LANGS}, None))
    for s in data["order"]:
        pairs.append(({l: svc_path(l, s) for l in LANGS}, None))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for paths, images in pairs:
        for i, lang in enumerate(LANGS):
            out.append("  <url>")
            out.append(f"    <loc>{SITE}{paths[lang]}</loc>")
            out.append(f"    <lastmod>{lastmod}</lastmod>")
            for l in LANGS:
                out.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{paths[l]}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{paths["en"]}"/>')
            if images:
                out.append(f"    <image:image><image:loc>{SITE}/{images[i]}</image:loc></image:image>")
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def all_urls(data):
    urls = [SITE + "/", SITE + "/ru"]
    for l in LANGS:
        urls.append(SITE + svc_path(l))
        urls += [SITE + svc_path(l, s) for s in data["order"]]
    return urls
