"""Build the static EN and RU pages from src/index.template.html + i18n.json.

    python build.py

Writes index.html (English, served at /) and ru/index.html (Russian, served at /ru).
Both pages carry the whole dictionary inline so the EN/RU switch can swap text live.

Also renders, from services.json: /services and /ru/services (hub), one page per service in each
language, 404.html, sitemap.xml and llms.txt.

Finally it copies the public files into dist/, which the Cloudflare Worker serves (`cf deploy`).
"""
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import pages  # noqa: E402

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "ru")
OUT = {"en": ROOT / "index.html", "ru": ROOT / "ru" / "index.html"}


def main():
    d = json.loads((ROOT / "i18n.json").read_text(encoding="utf-8"))
    tpl = (ROOT / "src" / "index.template.html").read_text(encoding="utf-8")

    for group in ("meta", "attr", "text", "js"):
        for k, v in d[group].items():
            missing = [l for l in LANGS if l not in v]
            assert not missing, f"{group}.{k} has no {missing}"

    used = set(re.findall(r"\{\{([\w.]+)\}\}", tpl)) - {"lang", "__i18n__", "__faq_ld__"}
    known = {f"meta.{k}" for k in d["meta"]} | set(d["attr"]) | set(d["text"])
    unknown = used - known
    assert not unknown, f"template uses unknown keys: {sorted(unknown)}"

    # What the browser needs to switch languages live.
    client = {
        "text": d["text"],
        "attr": d["attr"],
        "js": d["js"],
        "title": d["meta"]["title"],
        "url": {l: ("/" if l == "en" else f"/{l}") for l in LANGS},
    }
    payload = json.dumps(client, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    for lang in LANGS:
        faq_ld = pages.ld({
            "@context": "https://schema.org", "@type": "FAQPage",
            "@id": f"{pages.SITE}{pages.home(lang)}#faq", "inLanguage": pages.UI[lang]["inlang"],
            "mainEntity": [
                {"@type": "Question", "name": pages.plain(d["text"][f"fq{i}"][lang]),
                 "acceptedAnswer": {"@type": "Answer", "text": pages.plain(d["text"][f"fa{i}"][lang])}}
                for i in range(1, 100) if f"fq{i}" in d["text"]
            ],
        })

        def sub(m):
            key = m.group(1)
            if key == "lang":
                return lang
            if key == "__i18n__":
                return payload
            if key == "__faq_ld__":
                return faq_ld
            if key.startswith("meta."):
                return d["meta"][key[5:]][lang]
            src = d["attr"] if key in d["attr"] else d["text"]
            return src[key][lang]

        html = re.sub(r"\{\{([\w.]+)\}\}", sub, tpl)
        assert "{{" not in html, f"unfilled placeholder in {lang}"
        OUT[lang].parent.mkdir(parents=True, exist_ok=True)
        OUT[lang].write_text(html, encoding="utf-8", newline="\n")
        print(f"wrote {OUT[lang].relative_to(ROOT)} ({len(html.encode()) // 1024} KB)")

    build_pages(d)


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    assert "{{" not in text, f"unfilled placeholder in {rel}"
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def build_pages(d):
    data = json.loads((ROOT / "services.json").read_text(encoding="utf-8"))
    groups = d["text"]
    for slug in data["order"]:
        s = data["services"][slug]
        assert s["group"] in groups, f"{slug}: unknown group {s['group']}"
        for r in s["related"]:
            assert r in data["services"] and r != slug, f"{slug}: bad related {r}"
        for lang in LANGS:
            c = s[lang]
            for k in ("name", "title", "desc", "h1", "lede", "includes", "for", "faq"):
                assert c.get(k), f"{slug}.{lang}.{k} is empty"
            assert len(pages.plain(c["desc"])) <= 170, f"{slug}.{lang}.desc is {len(c['desc'])} chars"

    n = 0
    for lang in LANGS:
        base = "" if lang == "en" else "ru/"
        write(f"{base}services/index.html", pages.hub_page(lang, data, groups)); n += 1
        for slug in data["order"]:
            write(f"{base}services/{slug}/index.html", pages.service_page(lang, slug, data, groups)); n += 1
    write("404.html", pages.not_found_page(data))
    write("sitemap.xml", pages.sitemap(data, datetime.date.today().isoformat()))
    write("llms.txt", llms(d, data))
    print(f"wrote {n} service pages, 404.html, sitemap.xml ({len(pages.all_urls(data))} URLs), llms.txt")
    assemble_dist()


# Only these go live. An allowlist keeps sources, configs and any .env file out of the upload.
PUBLIC_FILES = ["index.html", "404.html", "sitemap.xml", "robots.txt", "llms.txt", "site.webmanifest", "favicon.ico"]
PUBLIC_GLOBS = ["*.png", "[0-9a-f]" * 32 + ".txt"]  # images, IndexNow key
PUBLIC_DIRS = ["ru", "services"]


def assemble_dist():
    dist = ROOT / "dist"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    files = [ROOT / f for f in PUBLIC_FILES] + [f for g in PUBLIC_GLOBS for f in ROOT.glob(g)]
    for f in files:
        shutil.copy2(f, dist / f.name)
    for d in PUBLIC_DIRS:
        shutil.copytree(ROOT / d, dist / d)
    shutil.copy2(ROOT / "src" / "_headers", dist / "_headers")
    count = sum(1 for f in dist.rglob("*") if f.is_file())
    print(f"assembled dist/ ({count} files)")


def llms(d, data):
    """Plain-language summary for AI assistants and answer engines (llmstxt.org)."""
    t = d["text"]
    lines = [
        "# Infinitum Defense",
        "",
        "> " + pages.plain(d["meta"]["description"]["en"]),
        "",
        "Infinitum Defense (Infinitum Defense Contracting Inc.) is the defensive arm of Infinitum Corporation, "
        "headquartered in Washington, D.C. The operations desk is open 24 hours a day, 7 days a week. "
        "Contracts run from a single day to indefinitely and start with a free consultation. "
        "The site is available in English and Russian.",
        "",
        "Phone (24/7): +1 202-831-4443",
        "",
        "## Services",
        "",
    ]
    for slug in data["order"]:
        c = data["services"][slug]["en"]
        lines.append(f"- [{pages.plain(c['name'])}]({pages.SITE}/services/{slug}): {pages.plain(c['desc'])}")
    lines += ["", "## Frequently asked questions", ""]
    i = 1
    while f"fq{i}" in t:
        lines.append(f"- {pages.plain(t[f'fq{i}']['en'])} {pages.plain(t[f'fa{i}']['en'])}")
        i += 1
    lines += [
        "",
        "## Pages",
        "",
        f"- [Home]({pages.SITE}/): overview, services, approach and contact form",
        f"- [Services]({pages.SITE}/services): all eight services",
        f"- [Russian version]({pages.SITE}/ru): the whole site in Russian",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
