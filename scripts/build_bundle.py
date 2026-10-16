#!/usr/bin/env python3
"""Build the FreeMium JayRain node bundle.

Downloads the latest Lavalink v4 server jar plus the youtube-plugin and
LavaSrc plugin jars from GitHub releases, then assembles freemium-node.zip:

    freemium-node.zip
    ├── Lavalink.jar
    ├── plugins/
    │   ├── youtube-plugin-<ver>.jar
    │   └── lavasrc-plugin-<ver>.jar
    ├── application.yml      (tuned template, __NODE_PASSWORD__ placeholder)
    ├── start-node.bat
    ├── start-node.sh
    └── README.txt

Writes versions.json with the resolved upstream versions.

Usage:
    python3 scripts/build_bundle.py [--out dist/]

Honors HTTPS_PROXY/HTTP_PROXY env vars (needed on restricted networks).
"""
import json
import os
import re
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT / "bundle"
GITHUB_API = "https://api.github.com"

SOURCES = [
    {
        "key": "lavalink",
        "repo": "lavalink-devs/Lavalink",
        "tag_prefix": "4",
        "asset": lambda n: n == "Lavalink.jar",
        "dest": "Lavalink.jar",
    },
    {
        "key": "youtube-plugin",
        "repo": "lavalink-devs/youtube-source",
        "tag_prefix": None,
        "asset": lambda n: (n.startswith("youtube-plugin-") and n.endswith(".jar")
                            and "sources" not in n and "javadoc" not in n),
        "dest": "plugins/",
    },
    {
        "key": "lavasrc",
        "repo": "topi314/LavaSrc",
        "tag_prefix": None,
        "asset": lambda n: (n.startswith("lavasrc-plugin-") and n.endswith(".jar")
                            and "sources" not in n and "javadoc" not in n),
        "dest": "plugins/",
    },
]


def _opener():
    # Honor proxy env vars (urllib does not always pick them up by itself).
    proxies = {}
    for var in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        if os.environ.get(var):
            scheme = "https" if var.lower().startswith("https") else "http"
            proxies[scheme] = os.environ[var]
    handlers = [urllib.request.ProxyHandler(proxies)] if proxies else []
    opener = urllib.request.build_opener(*handlers)
    opener.addheaders = [
        ("User-Agent", "freemium-jayrain-node-builder"),
        ("Accept", "application/vnd.github+json"),
    ]
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        opener.addheaders.append(("Authorization", f"Bearer {token}"))
    return opener


def gh_json(url, opener):
    with opener.open(url, timeout=60) as resp:
        return json.load(resp)


def pick_release(repo, tag_prefix, opener):
    data = gh_json(f"{GITHUB_API}/repos/{repo}/releases?per_page=15", opener)
    for rel in data:
        if rel.get("draft"):
            continue
        tag = rel.get("tag_name", "")
        norm = tag[1:] if tag.startswith("v") else tag
        if tag_prefix and not norm.startswith(tag_prefix):
            continue
        return rel
    raise RuntimeError(f"No suitable release found for {repo} (prefix={tag_prefix})")


def pick_asset(release, matcher):
    for asset in release.get("assets", []):
        name = asset.get("name", "")
        if matcher(name):
            return asset
    names = [a.get("name") for a in release.get("assets", [])]
    raise RuntimeError(
        f"No matching asset in {release.get('tag_name')}; available: {names}")


def download(url, dest, opener):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    # Don't send the JSON accept header for binary downloads.
    with opener.open(req, timeout=300) as resp, open(dest, "wb") as fh:
        shutil.copyfileobj(resp, fh, length=1024 * 256)
    size_mb = dest.stat().st_size / 1024 / 1024
    print(f"  downloaded {dest.name} ({size_mb:.1f} MB)")
    return dest


def main():
    out_dir = Path(sys.argv[sys.argv.index("--out") + 1]) \
        if "--out" in sys.argv else ROOT / "dist"
    work = out_dir / "work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    opener = _opener()
    versions = {}
    staged = []

    for src in SOURCES:
        print(f"Resolving {src['repo']}...")
        rel = pick_release(src["repo"], src["tag_prefix"], opener)
        tag = rel["tag_name"]
        asset = pick_asset(rel, src["asset"])
        print(f"  {tag} -> {asset['name']}")
        dest = work / src["dest"]
        if str(src["dest"]).endswith("/"):
            dest = dest / asset["name"]
        download(asset["browser_download_url"], dest, opener)
        staged.append((dest, asset["name"] if str(src["dest"]).endswith("/") else src["dest"]))
        versions[src["key"]] = {"repo": src["repo"], "tag": tag,
                                "asset": asset["name"]}

    # Static bundle files.
    for name in ("application.yml", "start-node.bat", "start-node.sh", "README.txt"):
        src = BUNDLE_DIR / name
        if not src.is_file():
            raise RuntimeError(f"Missing bundle file: {src}")
        shutil.copy2(src, work / name)

    # Make the .sh executable inside the zip (ZipInfo external_attr).
    zip_path = out_dir / "freemium-node.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(work.rglob("*")):
            if not path.is_file():
                continue
            arc = path.relative_to(work).as_posix()
            zi = zipfile.ZipInfo(arc)
            zi.external_attr = (0o755 if path.suffix == ".sh" else 0o644) << 16
            with open(path, "rb") as fh:
                zf.writestr(zi, fh.read())
    size_mb = zip_path.stat().st_size / 1024 / 1024
    print(f"Built {zip_path} ({size_mb:.1f} MB)")

    versions_path = out_dir / "versions.json"
    versions_path.write_text(json.dumps(versions, indent=2) + "\n")
    print(f"Wrote {versions_path}")
    for key, info in versions.items():
        print(f"  {key}: {info['tag']}")


if __name__ == "__main__":
    main()
