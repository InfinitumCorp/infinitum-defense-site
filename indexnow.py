"""Tell Bing, Yandex and other IndexNow engines that every page changed. Run after a production deploy:

    python indexnow.py

The key is public by design: it is served at https://infinitumdefense.com/9975a3c913356e0128d7e93b74ea1481.txt to prove ownership.
"""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import pages  # noqa: E402

KEY = "9975a3c913356e0128d7e93b74ea1481"


def main():
    data = json.loads((Path(__file__).resolve().parent / "services.json").read_text(encoding="utf-8"))
    body = json.dumps({
        "host": "infinitumdefense.com",
        "key": KEY,
        "keyLocation": f"{pages.SITE}/{KEY}.txt",
        "urlList": pages.all_urls(data),
    }).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow:", r.status, f"({len(pages.all_urls(data))} URLs)")


if __name__ == "__main__":
    main()
