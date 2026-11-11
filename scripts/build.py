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
        # French is also served at /<slug>/. Give both URLs a single canonical
        # and point all hreflang/structured-data/sitemap references at that URL.
        replacement = replacement.replace(f"{DOMAIN}/{slug}/fr/index.html", f"{DOMAIN}/{slug}/")
        replacement = replacement.replace(f"{DOMAIN}/{slug}/index.html", f"{DOMAIN}/{slug}/")
        if original != replacement:
            f.write_text(replacement, encoding="utf-8")


def unpack_zapiki_artwork(target):
    """Unpack exactly the expected ZAPIKI images for production and preview."""
    archive = target/"assets"/"zapiki-visuels-webp.zip"
    if not archive.is_file():
        raise FileNotFoundError(f"Missing ZAPIKI artwork archive: {archive}")
    expected = {f"{lang}/{i:02d}.webp" for lang in LANGS for i in range(1,8)}
    expected.update({"cinema.webp", "icone-source.webp"})
    output = target/"assets"/"promo"
    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())
        missing = sorted(expected - names)
        if missing:
            raise ValueError(f"ZAPIKI artwork ZIP missing {len(missing)} images: {missing[:10]}")
        for name in sorted(expected):
            item = output/name
            item.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(name) as input_file, item.open("wb") as output_file:
                shutil.copyfileobj(input_file, output_file)
    archive.unlink()
    print("OK: ZAPIKI 70 visuals plus 2 supplemental images")

def build_preview(sources, destination):
    """Publish an isolated noindex preview without changing the current public ZAPIKI site."""
    source = sources/"zapiki-preview"
    if not (source/"index.html").is_file():
        return
    target = destination/"apercu-zapiki"
    mirror(source, target, "Zapiki-Website", "apercu-zapiki")
    unpack_zapiki_artwork(target)
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
        if slug == "zapiki":
            unpack_zapiki_artwork(target)
            if not (target / "download" / "index.html").is_file():
                raise FileNotFoundError("ZAPIKI downloads landing page missing")
            links.append(f"{DOMAIN}/zapiki/download/")
        links.append(f"{DOMAIN}/{slug}/")
        if slug in {"stopododo", "clikospido"}:
            for lang in LANGS:
                if not (target/lang/"index.html").is_file():
                    raise ValueError(f"Missing {lang} translation in {slug}")
                links.append(f"{DOMAIN}/{slug}/{lang}/index.html")
        else:
            for lang in LANGS:
                if not (target/lang/"index.html").is_file():
                    raise ValueError(f"Missing ZAPIKI translation: {lang}")
                links.append(f"{DOMAIN}/{slug}/{lang}/index.html")
                guides_dir = target/lang/"guides"
                if not (guides_dir/"index.html").is_file():
                    raise ValueError(f"Missing ZAPIKI guides hub: {lang}")
                links.append(f"{DOMAIN}/{slug}/{lang}/guides/")
                guide_pages = sorted(g for g in guides_dir.iterdir() if g.is_dir() and (g/"index.html").is_file())
                if len(guide_pages) != 10:
                    raise ValueError(f"Expected 10 ZAPIKI guides for {lang}, found {len(guide_pages)}")
                for guide_dir in guide_pages:
                    links.append(f"{DOMAIN}/{slug}/{lang}/guides/{guide_dir.name}/")
            for page in ("confidentialite.html", "conditions.html", "suppression-compte.html"):
                if not (target/page).is_file():
                    raise ValueError(f"Missing legal page {page} in ZAPIKI")
                links.append(f"{DOMAIN}/{slug}/{page}")
        for page in (target/"index.html", target/"fr"/"index.html"):
            html = page.read_text(encoding="utf-8")
            expected = f'rel="canonical" href="{DOMAIN}/{slug}/"'
            if expected not in html:
                raise ValueError(f"Canonical URL mismatch: {page}")
        print(f"OK {slug}: all source files mirrored and root canonicals checked")
    build_preview(sources, destination)
    # The French localized landing pages duplicate the product roots.
    # Google has already chosen the shorter product roots for canonicalization.
    # Submit those canonical roots, not the duplicated /fr/index.html URLs.
    canonical_links = [url for url in links if url not in
                       {f"{DOMAIN}/{slug}/fr/index.html" for slug in SITES}]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.extend(f"  <url><loc>{escape(url)}</loc></url>" for url in canonical_links)
    xml.append("</urlset>")
    (destination/"sitemap-pages.xml").write_text("\n".join(xml)+"\n", encoding="utf-8")
    # The mirrored source sitemaps already provide multilingual guide
    # URLs and reciprocal hreflang annotations.
    sitemap_urls = [
        f"{DOMAIN}/sitemap-pages.xml",
        f"{DOMAIN}/stopododo/sitemap.xml",
        f"{DOMAIN}/clikospido/sitemap.xml",
        f"{DOMAIN}/stopododo/video-sitemap.xml",
        f"{DOMAIN}/clikospido/video-sitemap.xml",
    ]
    for slug, file in (("stopododo", "sitemap.xml"),
                       ("clikospido", "sitemap.xml"),
                       ("stopododo", "video-sitemap.xml"),
                       ("clikospido", "video-sitemap.xml")):
        if not (destination/slug/file).is_file():
            raise FileNotFoundError(f"Required SEO sitemap missing: {slug}/{file}")
    index = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    index.extend(f"  <sitemap><loc>{escape(url)}</loc></sitemap>" for url in sitemap_urls)
    index.append("</sitemapindex>")
    (destination/"sitemap.xml").write_text("\n".join(index)+"\n", encoding="utf-8")
    (destination/"robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://gogostudio.app/sitemap.xml\n",
        encoding="utf-8")
    print(f"Ready: {destination}, {len(canonical_links)} canonical core URLs + product and video sitemaps")

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--sources",type=Path,required=True)
    parser.add_argument("--destination",type=Path,required=True)
    args=parser.parse_args()
    build(args.sources,args.destination,Path(__file__).resolve().parent.parent)
