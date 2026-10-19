#!/usr/bin/env python3
"""Build static site into dist/. Cloudflare Pages: build command `python3 build.py`, output dir `dist`."""
import json, re, shutil, html, sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SRC = json.loads((ROOT / "sources.json").read_text())
S = {s["key"]: s for s in SRC}

NAV_FILES = None
NAV = [("index.html","Home"),("origins.html","Origins"),("evidence.html","How We Know"),("stories.html","Stories"),("names.html","Names & Identity"),
       ("colonial.html","Colonial Era"),("faith.html","Faith & Literacy"),("modern.html","Modern History"),
       ("culture.html","Culture"),("diaspora.html","Diaspora"),("sources.html","Sources")]
TAGS = {"oral":'<span class="tag oral">Oral tradition</span>',"doc":'<span class="tag doc">Documented</span>',
        "sch":'<span class="tag sch">Scholarly interpretation</span>',"contested":'<span class="tag contested">Contested</span>'}
missing = set()
import os, datetime
SITE_URL = os.environ.get("SITE_URL", "https://tangthu.kws.site").rstrip("/")
TODAY = datetime.date.today().isoformat()
SITE_NAME = "Zogam History"
DESC = {
 "index.html": ("Zomi History & Zo History | Chin, Kuki, Mizo Peoples — Zogam History", "Zomi history and Zo history in one free, fully sourced archive: origins, Chin Hills, Anglo-Kuki War, Pau Cin Hau, Panglong, diaspora — for Zomi, Chin, Kuki, Lai and Mizo readers."),
 "origins.html": ("Zomi & Zo Origins and Migration: Khul, Chhinlung, Kabaw Valley", "Where did the Zo, Zomi and Chin peoples come from? Khul and Chhinlung origin traditions, Khampat, Ciimnuai, and what historians can and cannot prove."),
 "evidence.html": ("How We Know Zo History: Sources and Evidence", "The evidence behind Zo and Zomi history: the Man Shu, Burmese inscriptions, Carey & Tuck (1896), clan genealogies, songs and memorial stones."),
 "stories.html": ("Zomi History Stories: Ciimnuai, Khai Kam, Pau Cin Hau, Mautam", "Stories from Zo history: the remembered city of Ciimnuai, the Khampat banyan, Khan Thuam, Khai Kam’s resistance, Pau Cin Hau, and the Mautam famine."),
 "names.html": ("Zo, Zomi, Chin, Kuki, Mizo, Lai: What the Names Mean", "Why the Zo peoples are called Zomi, Chin, Kuki, Lai, Mizo and Zou — the origin of each name and why naming is debated, presented fairly."),
 "colonial.html": ("Chin Hills Under British Rule & the Anglo-Kuki War (Zou Gal)", "British annexation of the Chin Hills, the Chin Hills Regulation 1896, and the 1917–1919 Anglo-Kuki War (Zou Gal), with sources."),
 "faith.html": ("Zo Faith & Literacy: Missionaries, the Tedim Bible, Pau Cin Hau Script", "Traditional Zo religion, the 1899 Baptist mission to Hakha, the Tedim Bible, and Pau Cin Hau’s Laipian movement and Unicode script."),
 "modern.html": ("Modern Zomi, Zo & Chin History: Panglong to Today", "Panglong 1947, Chin National Day, Zomi and Zo reunification movements, displacement after Myanmar’s 2021 coup, and the Manipur conflict — neutral and sourced."),
 "culture.html": ("Zomi & Chin Culture: Language, Clans, Khuado, Weaving", "Zo languages, clans and chieftainship, the Khuado harvest festival, traditional music and backstrap weaving (puan)."),
 "diaspora.html": ("Zomi & Chin Diaspora: Indianapolis, Malaysia, Australia, Europe", "Zo, Zomi and Chin communities abroad — Indianapolis, Malaysia, Australia, New Zealand and Europe — and why families left."),
 "sources.html": ("Sources & Bibliography — Zogam History", "Full bibliography and editorial standards for Zogam History: primary, scholarly, news and community sources, labelled by type."),
 "contribute.html": ("Contribute Photos & Oral Histories — Zogam History", "Share family photographs, elders’ oral histories, genealogies and corrections to help preserve Zo and Zomi history."),
 "404.html": ("Page not found — Zogam History", "Page not found."),
}
FAQ = [
 ("What is Zomi history?", "Zomi history is the history of the peoples who call themselves Zomi (“Zo people”) — including Tedim, Paite, Zou, Simte, Vaiphei and related communities — in Myanmar’s Chin State, India’s Manipur and Mizoram, and the diaspora. The name was proposed in 1950 and adopted by the Zomi Baptist Convention in 1953."),
 ("What is Zo history?", "Zo history covers the wider family of related peoples — Zomi, Chin, Kuki, Lai, Mizo and Zou — who share Kuki-Chin languages and origin traditions such as Khul and Chhinlung, across Myanmar, Northeast India and Bangladesh."),
 ("Where did the Zo and Zomi people come from?", "Oral tradition tells of emergence from a cave called Khul or Chhinlung. Historians trace movement through the Kabaw and Kale valleys of the Chindwin into the Chin Hills; Burmese inscriptions mention the Chin by the 12th century."),
 ("What is the difference between Zo, Zomi, Chin, Kuki and Mizo?", "They overlap. Zomi and Mizo both mean “Zo people.” Chin and Kuki came from outside languages but are now held with pride by many. In 1896 British officers recorded that the Northern Chins called themselves Yo, the Haka and southern tribes Lai, and Lower Burma Chins Shu."),
 ("What is Zogam?", "Zogam means “the land of the Zo”: the hill country of Chin State (Myanmar), Manipur and Mizoram (India) and the Chittagong Hill Tracts (Bangladesh)."),
]
def clean(f): return "/" if f=="index.html" else "/"+f[:-5]

ACCESSED = "19 October 2026"
TIER = {"Primary":"Primary source","Archive":"Archive","Scholarly":"Scholarly work","Technical / scholarly":"Technical standard","Reference":"Reference work","Journalism":"News report","Research brief":"Research report","Community":"Community source","Community organisation":"Community organisation","Community essay":"Community essay","Missions database":"Missions database"}
def tier(s):
    return TIER.get(s["type"].split(" (")[0], s["type"])
def is_print(s):
    u=s["url"]; return ("google.com/search" in u) or ("worldcat.org/search" in u) or u=="contribute.html"
_used=[]
def cite(m):
    k = m.group(1)
    if k not in S: missing.add(k); return f'<span class="cite">[{k}?]</span>'
    if k not in _used: _used.append(k)
    n=_used.index(k)+1
    return f'<sup class="fn"><a href="#ref-{k}" title="{html.escape(S[k]["cite"])}" aria-label="Source {n}: {html.escape(S[k]["short"])}">[{n}]</a></sup>'

def refs_block(title):
    if not _used: return ""
    items=[]
    for k in _used:
        s=S[k]
        link = (f'<a href="{s["url"]}" rel="noopener" target="_blank">{"Catalogue search" if is_print(s) else "Read the source"}</a>' if s["url"]!="contribute.html" else '<span>Unpublished; held by the project</span>')
        status = '<span class="badge warn">Print / not yet verified online</span>' if is_print(s) else f'<span class="badge">Accessed {ACCESSED}</span>'
        note = f'<div class="note">{html.escape(s["note"])}</div>' if s.get("note") else ""
        items.append(f'<li id="ref-{k}"><span class="badge type">{html.escape(tier(s))}</span> {html.escape(s["cite"])} {link} {status}{note}</li>')
    cite_box=f'<div class="citebox"><strong>Cite this page:</strong> Zogam History. “{html.escape(title)}.” Accessed {ACCESSED}. <span class="small">(Use the page address from your browser.)</span></div>'
    return f'<section class="refs" aria-labelledby="refs-h"><h2 id="refs-h">Sources for this page</h2><p class="small">Numbers in brackets in the text link here. Each source is labelled by type so you can judge its weight. Colonial, missionary and advocacy sources are included as evidence of a viewpoint, not as neutral authority.</p><ol>{"".join(items)}</ol>{cite_box}</section>'

def ph(kind, text):
    if kind == "photo":
        return f'<figure class="placeholder"><div class="ico">IMG</div><p><strong>Community photo wanted</strong>{text}</p></figure>'
    return f'<aside class="placeholder"><div class="ico">♪</div><p><strong>Oral history wanted</strong>{text} <a href="contribute.html">Contribute →</a></p></aside>'

def render(body):
    body = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', lambda m: f'href="{clean(m.group(1)+".html")}{m.group(2) or ""}"', body)
    body = re.sub(r"\[\[([\w-]+)\]\]", cite, body)
    body = re.sub(r"\{\{(photo|oralhistory):(.*?)\}\}", lambda m: ph(m.group(1), m.group(2)), body)
    for k,v in TAGS.items(): body = body.replace("{{"+k+"}}", v)
    return body

def page(fname, title, body, wide=False, home=False):
    nav = "".join(f'<a href="{clean(h)}"{" aria-current=\"page\"" if h==fname else ""}>{l}</a>' for h,l in NAV)
    leaflet = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
               '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>') if home else ""
    t, d = DESC.get(fname, (f"{title} — {SITE_NAME}", ""))
    url = SITE_URL + clean(fname)
    img = SITE_URL + "/assets/og.png"
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE_URL+"/"}]
    if not home: crumbs.append({"@type":"ListItem","position":2,"name":title,"item":url})
    graph = [
      {"@type":"WebSite","@id":SITE_URL+"/#site","url":SITE_URL+"/","name":SITE_NAME,"inLanguage":"en","description":DESC["index.html"][1]},
      {"@type":"WebPage" if home else "Article","@id":url+"#page","url":url,"name":t,"headline":title if not home else t,"description":d,"isPartOf":{"@id":SITE_URL+"/#site"},"inLanguage":"en","dateModified":TODAY,"image":img,
       "about":[{"@type":"Thing","name":n} for n in ["Zo people","Zomi","Chin people","Kuki people","Mizo people","Chin Hills"]]},
      {"@type":"BreadcrumbList","itemListElement":crumbs}]
    if home:
        graph.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    robots = '<meta name="robots" content="noindex">' if fname=="404.html" else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t)}</title>
<meta name="description" content="{html.escape(d)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'website' if home else 'article'}"><meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(t)}"><meta property="og:description" content="{html.escape(d)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(t)}"><meta name="twitter:description" content="{html.escape(d)}"><meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#9a4a2a">
<script type="application/ld+json">{ld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=Noto+Sans+Pau+Cin+Hau&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">{leaflet}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="bar"><a class="brand" href="/">Zo<span>gam</span> History</a>
<button class="navtoggle" aria-expanded="false" aria-label="Menu">Menu</button><nav class="main" aria-label="Main">{nav}</nav></div></header>
<main id="main"{' class="wide"' if wide else ""}>{body}</main>
<footer class="site"><p>An educational, non-partisan community resource. Oral tradition and documented history are labelled separately.<br>
Found an error? <a href="/contribute">Send a correction with a source.</a> · <a href="/sources">Sources &amp; standards</a> · <a href="/sitemap">Site map</a></p></footer>
<script src="/assets/sources.js"></script><script src="/assets/data.js"></script><script defer src="/assets/site.js"></script>
</body></html>'''

def sources_page():
    groups = {}
    for s in sorted(SRC, key=lambda s: s["cite"].lower()): groups.setdefault(s["type"].split(" (")[0], []).append(s)
    order = ["Primary","Archive","Scholarly","Technical / scholarly","Reference","Journalism","Research brief","Community","Community organisation","Missions database"]
    out = ['<h1>Sources &amp; Further Reading</h1>',
           '''<section class="standards"><h2>Editorial standards</h2>
<ul>
<li><strong>Every factual sentence is cited.</strong> Numbered notes on each page link to the full reference at the bottom of that page and to this bibliography.</li>
<li><strong>Three evidence labels.</strong> <em>Oral tradition</em> (songs, genealogies, memory), <em>Documented</em> (contemporary records, official data), and <em>Scholarly interpretation</em> (arguments by historians). They are never mixed silently.</li>
<li><strong>Source types are shown.</strong> Primary, scholarly, reference, news and community sources are labelled. Colonial, missionary and advocacy writing is used as evidence of a viewpoint, not as neutral authority.</li>
<li><strong>Contested topics.</strong> On names, borders and the Manipur conflict we report what each community says and what official figures show, and attribute every claim. We do not take sides.</li>
<li><strong>Unverified sources are flagged.</strong> Print works we have not yet examined are marked “Print / not yet verified online” and never stand alone for a contested claim.</li>
<li><strong>Corrections.</strong> Send a correction with a source through the <a href="contribute.html">Contribute</a> page. Corrections are made promptly and the review date below is updated.</li>
</ul>
<p class="small">Last full source review: 19 October 2026.</p></section>''',
           '<h2>Full bibliography</h2><p class="lede">Every claim on this site links here. Colonial and missionary sources are included because they are primary evidence — but they reflect their authors’ perspectives, and are flagged where that matters.</p>',
           '<div class="caution"><strong>About reference sources.</strong> Wikipedia and similar summaries are used for verifiable facts and as entry points. Where possible, follow them to the scholarly works listed under “Scholarly”.</div>']
    keys = sorted(groups, key=lambda g: order.index(g) if g in order else 99)
    for g in keys:
        out.append(f'<section class="src-group"><h2>{html.escape(g)}</h2>')
        for s in groups[g]:
            note = f'<div class="note">{html.escape(s["note"])}</div>' if s.get("note") else ""
            lk = '' if s["url"]=="contribute.html" else f' <a href="{s["url"]}" rel="noopener" target="_blank">{"Catalogue search" if is_print(s) else "Link"}</a>'
            out.append(f'<div class="src" id="{s["key"]}"><div class="k">{html.escape(s["short"])} · {html.escape(tier(s))}{" · print / not yet verified online" if is_print(s) else ""}</div>{html.escape(s["cite"])}{lk}{note}</div>')
        out.append("</section>")
    out.append('<h2>Recommended starting points</h2><ul><li>Sakhong, <em>In Search of Chin Identity</em> (2003)</li><li>Pau, <em>Indo-Burma Frontier and the Making of the Chin Hills</em> (2019)</li><li>Go, <em>Zo Chronicles</em> (2008)</li><li>Guite &amp; Haokip, eds., <em>The Anglo-Kuki War, 1917–1919</em> (2019)</li></ul>')
    return "\n".join(out)

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    global NAV
    NAV = [(clean(f) if False else f, l) for f,l in NAV]
    DIST.mkdir()
    shutil.copytree(ROOT/"assets", DIST/"assets")
    (DIST/"assets"/"sources.js").write_text("window.ZO_SRC="+json.dumps({s["key"]:s["short"] for s in SRC})+";")
    for f in sorted((ROOT/"content").glob("*.html")):
        raw = f.read_text(); m = re.match(r"<!-- title: (.*?) -->", raw)
        title = m.group(1) if m else f.stem
        _used.clear()
        body = render(raw)
        if f.name != "contribute.html": body += refs_block(title)
        (DIST/f.name).write_text(page(f.name, title, body, wide=f.name=="index.html", home=f.name=="index.html"))
    (DIST/"sources.html").write_text(page("sources.html","Sources",sources_page()))
    (DIST/"404.html").write_text(page("404.html","Not found",'<h1>Page not found</h1><p><a href="index.html">Return home</a></p>'))
    pages = [f.name for f in sorted((ROOT/"content").glob("*.html"))] + ["sources.html","sitemap.html"]
    pri = {"index.html":"1.0","origins.html":"0.9","names.html":"0.9","stories.html":"0.9","evidence.html":"0.8","colonial.html":"0.8","faith.html":"0.8","modern.html":"0.8","culture.html":"0.8","diaspora.html":"0.8","sources.html":"0.6","contribute.html":"0.4","sitemap.html":"0.3"}
    urls = "".join(f"<url><loc>{SITE_URL}{clean(p)}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{pri.get(p,'0.5')}</priority></url>" for p in pages)
    (DIST/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (DIST/"robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    items = "".join(f'<li><a href="{clean(p)}">{html.escape(DESC[p][0])}</a><br><span class="small">{html.escape(DESC[p][1])}</span></li>' for p in pages if p in DESC)
    (DIST/"sitemap.html").write_text(page("sitemap.html","Site map",f'<h1>Site map</h1><ul class="sitemap">{items}</ul>'))
    (DIST/"_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/assets/*\n  Cache-Control: public, max-age=86400\n")
    # check every source is cited somewhere
    used = set(re.findall(r"\[\[([\w-]+)\]\]", "".join(p.read_text() for p in (ROOT/"content").glob("*.html"))))
    used |= set(re.findall(r'"([\w-]+)"', re.search(r"src:\[.*", (ROOT/"assets/data.js").read_text(), re.S).group(0)))
    if missing: print("MISSING SOURCE KEYS:", missing); sys.exit(1)
    unused = set(S) - used
    print(f"Built {len(list(DIST.glob('*.html')))} pages. Unused sources: {sorted(unused) or 'none'}")

if __name__ == "__main__": main()
