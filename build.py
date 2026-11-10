"""Build the static EN and RU pages from src/index.template.html + i18n.json.

    python build.py

Writes index.html (English, served at /) and ru/index.html (Russian, served at /ru).
Both pages carry the whole dictionary inline so the EN/RU switch can swap text live.
"""
import json
import re
from pathlib import Path

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

    used = set(re.findall(r"\{\{([\w.]+)\}\}", tpl)) - {"lang", "__i18n__"}
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
        def sub(m):
            key = m.group(1)
            if key == "lang":
                return lang
            if key == "__i18n__":
                return payload
            if key.startswith("meta."):
                return d["meta"][key[5:]][lang]
            src = d["attr"] if key in d["attr"] else d["text"]
            return src[key][lang]

        html = re.sub(r"\{\{([\w.]+)\}\}", sub, tpl)
        assert "{{" not in html, f"unfilled placeholder in {lang}"
        OUT[lang].parent.mkdir(parents=True, exist_ok=True)
        OUT[lang].write_text(html, encoding="utf-8", newline="\n")
        print(f"wrote {OUT[lang].relative_to(ROOT)} ({len(html.encode()) // 1024} KB)")


if __name__ == "__main__":
    main()
