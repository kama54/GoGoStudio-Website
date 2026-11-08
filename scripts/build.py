#!/usr/bin/env python3
"""Assemble GoGoStudio without modifying the three original repositories."""
import argparse
import shutil
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

DOMAIN = "https://gogostudio.app"
SITES = {"stopododo": "Stopododo-Website", "clikospido": "ClikoSpido-Website", "zapiki": "Zapiki-Website"}
LANGS = ["fr", "en", "es", "it", "de", "nl", "pt", "ar", "ja", "ko"]
TEXT_EXT = {".html", ".htm", ".css", ".js", ".xml", ".json", ".txt", ".webmanifest"}

def ignore(_dir, names):
    return [x for x in names if x in {".git", ".github", "node_modules", "__pycache__", "dist", "CNAME", ".DS_Store"}]

def mirror(source, target, repo, slug):
    if not (source/"index.html").exists():
        raise ValueError(f"Missing index for {slug}: {source}")
    shutil.copytree(source, target, ignore=ignore)
    old = f"https://kama54.github.io/{repo}/"
    new = f"{DOMAIN}/{slug}/"
    for f in target.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in TEXT_EXT:
            continue
        try:
            original = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        replacement = original.replace(old, new).replace(f"/{repo}/", f"/{slug}/")
        if original != replacement:
            f.write_text(replacement, encoding="utf-8")


def unpack_zapiki_preview(target):
    """Unpack exactly the trusted, expected image paths for the temporary preview."""
    archive = target/"assets"/"zapiki-visuels-webp.zip"
    if not archive.is_file():
        raise FileNotFoundError(f"Missing preview artwork archive: {archive}")
    expected = {f"{lang}/{i:02d}.webp" for lang in LANGS for i in range(1,8)}
    expected.update({"cinema.webp", "icone-source.webp"})
    output = target/"assets"/"promo"
    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())
        missing = sorted(expected - names)
        if missing:
            raise ValueError(f"ZAPIKI preview ZIP missing {len(missing)} images: {missing[:10]}")
        for name in sorted(expected):
            item = output/name
            item.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(name) as input_file, item.open("wb") as output_file:
                shutil.copyfileobj(input_file, output_file)
    archive.unlink()
    print("OK: ZAPIKI preview 70 visuals plus 2 supplemental images")

def build_preview(sources, destination):
    """Publish an isolated noindex preview without changing the current public ZAPIKI site."""
    source = sources/"zapiki-preview"
    if not (source/"index.html").is_file():
        return
    target = destination/"apercu-zapiki"
    mirror(source, target, "Zapiki-Website", "apercu-zapiki")
    unpack_zapiki_preview(target)
    count = 0
    for html_file in target.rglob("*.html"):
        page = html_file.read_text(encoding="utf-8")
        new_page, changed = re.subn(r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>',
                                    '<meta name="robots" content="noindex,nofollow">',
                                    page, count=1)
        if not changed:
            new_page = page.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">', 1)
        html_file.write_text(new_page, encoding="utf-8")
        count += 1
    for lang in LANGS:
        assert (target/lang/"index.html").is_file(), f"Missing preview locale {lang}"
        assert all((target/"assets"/"promo"/lang/f"{i:02d}.webp").is_file() for i in range(1,8)), f"Missing {lang} images"
    assert count >= 11, "Expected 10 locales and preview homepage"
    print(f"Preview built: {target}, {count} noindex HTML pages")

def build(sources, destination, root):
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for name in ("index.html", "styles.css", "app.js", "favicon.svg"):
        shutil.copy2(root/name, destination/name)
    if (root/"assets").is_dir():
        shutil.copytree(root/"assets", destination/"assets")
    (destination/".nojekyll").write_text("", encoding="utf-8")
    links = [DOMAIN+"/"]
    for slug, repo in SITES.items():
        target = destination/slug
        mirror(sources/slug, target, repo, slug)
        links.append(f"{DOMAIN}/{slug}/")
        if slug in {"stopododo", "clikospido"}:
            for lang in LANGS:
                if not (target/lang/"index.html").is_file():
                    raise ValueError(f"Missing {lang} translation in {slug}")
                links.append(f"{DOMAIN}/{slug}/{lang}/index.html")
        else:
            for page in ("confidentialite.html", "conditions.html", "suppression-compte.html"):
                if not (target/page).is_file():
                    raise ValueError(f"Missing legal page {page} in ZAPIKI")
                links.append(f"{DOMAIN}/{slug}/{page}")
        print(f"OK {slug}: all source files mirrored")
    build_preview(sources, destination)
    xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.extend(f"  <url><loc>{escape(link)}</loc></url>" for link in links)
    xml.append("</urlset>")
    (destination/"sitemap.xml").write_text("\n".join(xml)+"\n",encoding="utf-8")
    (destination/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://gogostudio.app/sitemap.xml\n",encoding="utf-8")
    print(f"Ready: {destination}, {len(links)} sitemap URLs")

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--sources",type=Path,required=True)
    parser.add_argument("--destination",type=Path,required=True)
    args=parser.parse_args()
    build(args.sources,args.destination,Path(__file__).resolve().parent.parent)
