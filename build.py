#!/usr/bin/env python3
"""Build static site into dist/: python3 build.py"""
import json, re, shutil, html, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SRC = json.loads((ROOT / "sources.json").read_text())
S = {s["key"]: s for s in SRC}
PHOTOS = json.loads((ROOT / "photos.json").read_text()) if (ROOT / "photos.json").exists() else {}
PHOTO_RE = re.compile(r"\{\{photo:(.*?)\}\}")
PHOTO_REQUIRED = ("alt", "caption", "source", "width", "height")  # plus "file" or "url"
IMAGE_BASE = "https://assets.khual.net/tangthu/img"  # every {{img:key}} is served from here
IMAGE_REQUIRED = ("file", "caption", "alt", "author", "source", "licence", "licence_url", "date_taken", "changes", "context", "verified")
OFFLINE = "--offline" in sys.argv  # skip the reachability check (no network). Uploads are manual: scripts/upload_images.py
IMG_RE = re.compile(r"\{\{img:([\w-]+)\}\}")
def load_images():
    return json.loads((ROOT / "images.json").read_text()) if (ROOT / "images.json").exists() else {}
IMAGES = load_images()

NAV_FILES = None
NAV = [("origins.html","Origins"),("evidence.html","Evidence"),("stories.html","Stories"),("names.html","Names"),("colonial.html","Colonial"),("faith.html","Faith"),("modern.html","Modern"),("culture.html","Culture"),("diaspora.html","Diaspora"),("glossary.html","Glossary"),("sources.html","Sources"),("search.html","Search")]
TAGS = {"oral":'<span class="tag oral">Oral tradition</span>',"doc":'<span class="tag doc">Documented</span>',
        "sch":'<span class="tag sch">Scholarly interpretation</span>',"contested":'<span class="tag contested">Contested</span>'}
missing = set()
import os, datetime
SITE_URL = os.environ.get("SITE_URL", "https://tangthu.kws.site").rstrip("/")
CDN_BASE = os.environ.get("TANGTHU_CDN", "https://assets.khual.net/tangthu/img").rstrip("/")
CDN_ORIGIN = "/".join(CDN_BASE.split("/")[:3])  # for <link rel="preconnect">
FAVICON_DIR = ROOT / "zogam-favicons"
FAVICON_HEAD = (FAVICON_DIR / "head-snippet.html").read_text().strip()  # icon links + theme-color
TODAY = datetime.date.today().isoformat()
SITE_NAME = "Zogam History"
DESC = {
 "index.html": ("Zomi & Zo History | Chin, Kuki, Lai and Mizo Peoples", "Zomi and Zo history in nine short, sourced chapters: origins, the Chin Hills, Pau Cin Hau, Panglong, the diaspora. For Zomi, Chin, Kuki, Lai and Mizo readers."),
 "origins.html": ("Zomi Origins: Khul, Chhinlung and the Kabaw Valley", "Where did the Zo, Zomi and Chin peoples come from? Khul and Chhinlung origin traditions, Khampat, Ciimnuai, and what historians can and cannot prove."),
 "evidence.html": ("How We Know Zomi History: Sources and Evidence", "The evidence behind Zo and Zomi history: the Man Shu, Burmese inscriptions, Carey & Tuck (1896), clan genealogies, songs and memorial stones."),
 "stories.html": ("Zomi History Stories: Ciimnuai, Khai Kam, Mautam", "Stories from Zo history: the remembered city of Ciimnuai, the Khampat banyan, Khan Thuam, Khai Kam’s resistance, Pau Cin Hau, and the Mautam famine."),
 "names.html": ("Zomi, Zo, Chin, Kuki, Mizo, Lai: What the Names Mean", "Why the Zo peoples are called Zomi, Chin, Kuki, Lai, Mizo and Zou — the origin of each name and why naming is debated, presented fairly."),
 "colonial.html": ("Chin Hills History: British Rule, the Chin Rising and Falam (1888–1948)", "British annexation of the Chin Hills, the Chin Hills Regulation 1896, and the 1917–1919 Anglo-Kuki War (Zou Gal), with sources."),
 "faith.html": ("Zomi Faith: Tedim Bible and Pau Cin Hau Script", "Traditional Zo religion, the 1899 Baptist mission to Hakha, the Tedim Bible, and Pau Cin Hau’s Laipian movement and Unicode script."),
 "modern.html": ("Modern Zomi & Chin History: Panglong to Today", "Panglong 1947, Chin National Day, Zomi and Zo reunification movements, displacement after Myanmar’s 2021 coup, and the Manipur conflict — neutral and sourced."),
 "culture.html": ("Zomi & Chin Culture: Language, Clans, Khuado, Weaving", "Zo languages, clans and chieftainship, the Khuado harvest festival, traditional music and backstrap weaving (puan)."),
 "diaspora.html": ("Zomi & Chin Diaspora: Indianapolis, Malaysia, Australia", "Zo, Zomi and Chin communities abroad — Indianapolis, Malaysia, Australia, New Zealand and Europe — and why families left."),
 "timeline.html": ("Zomi History Timeline: From Khul to Today", "An interactive timeline of Zomi and Zo history: origin traditions, the Chin Hills under British rule, Pau Cin Hau, Panglong, Chin National Day and the diaspora."),
 "glossary.html": ("Zomi History Glossary: Puan, Khuado, Zogam & More", "Simple definitions of words in Zomi and Zo history: Zogam, puan, Khuado, Ciimnuai, Pau Cin Hau, Zou Gal, ZORO and more."),
 "sources.html": ("Sources & Bibliography — Zogam History", "Full bibliography and editorial standards for Zogam History: primary, scholarly, news and community sources, labelled by type."),
 "contribute.html": ("Contribute to Zomi History: Stories, Photos and Licence", "Email tangthu@khual.net to share family photographs, elders’ oral histories, genealogies and corrections to help preserve Zo and Zomi history."),
 "404.html": ("Page not found — Zogam History", "This page doesn’t exist. Start from the Zogam History home page or the chapter list."),
 "search.html": ("Search — Zogam History", "Search every page of Zogam History: chapters, stories, proverbs, glossary terms, timeline events and sources."),
 "sitemap.html": ("Site map — Zogam History", "Every page on Zogam History, the free, sourced history of the Zomi and Zo peoples, grouped by chapter."),
}
PAGE_TYPE = {"search.html": "SearchResultsPage", "sources.html": "CollectionPage", "contribute.html": "WebPage", "sitemap.html": "WebPage", "404.html": "WebPage"}  # chapters and stories are Article
FAQ = [
 ("What is Zomi history?", "Zomi history is the history of the peoples who call themselves Zomi (“Zo people”) — including Tedim, Paite, Zou, Simte, Vaiphei and related communities — in Myanmar’s Chin State, India’s Manipur and Mizoram, and the diaspora. The name was proposed in 1950 and adopted by the Zomi Baptist Convention in 1953."),
 ("What is Zo history?", "Zo history covers the wider family of related peoples — Zomi, Chin, Kuki, Lai, Mizo and Zou — who share Kuki-Chin languages and origin traditions such as Khul and Chhinlung, across Myanmar, Northeast India and Bangladesh."),
 ("Where did the Zo and Zomi people come from?", "Oral tradition tells of emergence from a cave called Khul or Chhinlung. Historians trace movement through the Kabaw and Kale valleys of the Chindwin into the Chin Hills; Burmese inscriptions mention the Chin by the 12th century."),
 ("What is the difference between Zo, Zomi, Chin, Kuki and Mizo?", "They overlap. Zomi and Mizo both mean “Zo people.” Chin and Kuki came from outside languages but are now held with pride by many. In 1896 British officers recorded that the Northern Chins called themselves Yo, the Haka and southern tribes Lai, and Lower Burma Chins Shu."),
 ("What is Zogam?", "Zogam means “the land of the Zo”: the hill country of Chin State (Myanmar), Manipur and Mizoram (India) and the Chittagong Hill Tracts (Bangladesh)."),
]
CHAPTERS = ["origins.html","evidence.html","stories.html","names.html","colonial.html","faith.html","modern.html","culture.html","diaspora.html"]
CH_LABEL = {"origins.html":"Origins & Migration","evidence.html":"How We Know","stories.html":"Stories","names.html":"Names & Identity","colonial.html":"Colonial Era","faith.html":"Faith & Literacy","modern.html":"Modern History","culture.html":"Culture","diaspora.html":"Diaspora"}
def chapter_head(f):
    if f not in CHAPTERS: return ""
    n=CHAPTERS.index(f)+1
    pub, upd = pdates(f)
    return (f'<p class="chapter-eyebrow">Chapter {n} of {len(CHAPTERS)}</p>'
            f'<p class="pagedates small">Published <time datetime="{pub}">{long_date(pub)}</time> · Last updated <time datetime="{upd}">{long_date(upd)}</time></p>')
def chapter_nav(f):
    if f not in CHAPTERS: return ""
    i=CHAPTERS.index(f); out='<nav class="chapter-nav" aria-label="Chapters">'
    if i>0: p=CHAPTERS[i-1]; out+=f'<a class="prev" href="{clean(p)}"><span>Previous chapter</span>{html.escape(CH_LABEL[p])}</a>'
    else: out+='<span></span>'
    if i<len(CHAPTERS)-1: nx=CHAPTERS[i+1]; out+=f'<a class="next" href="{clean(nx)}"><span>Next chapter</span>{html.escape(CH_LABEL[nx])}</a>'
    return out+'</nav>'
def onpage(body, fname):
    if fname not in CHAPTERS: return body
    out=[]; last=0; items=[]
    for m in re.finditer(r'<h2(?: id="([^"]*)")?>(.*?)</h2>', body, re.S):
        pre=body[:m.start()]
        if pre.rfind('<article')>pre.rfind('</article>'): continue
        label=re.sub(r'<span class="tag[^>]*>.*?</span>','',m.group(2)); label=re.sub('<[^>]+>','',label).strip()
        sid=m.group(1) or re.sub(r'[^a-z0-9]+','-',label.lower()).strip('-')[:40]
        out.append(body[last:m.start()]+f'<h2 id="{sid}">{m.group(2)}</h2>'); last=m.end(); items.append((sid,label))
    out.append(body[last:]); body="".join(out)
    if len(items)<2: return body
    nav='<nav class="onpage" aria-label="On this page"><span class="onpage-label">On this page</span><ul>'+"".join(f'<li><a href="#{i}">{html.escape(l)}</a></li>' for i,l in items)+'</ul></nav>'
    first=body.find(f'<h2 id="{items[0][0]}">')
    return body[:first]+nav+body[first:]
ABOUT = [("Zo people","https://en.wikipedia.org/wiki/Zo_people"),("Zomi people","https://en.wikipedia.org/wiki/Zomi_people"),("Chin people","https://en.wikipedia.org/wiki/Chin_people"),("Kuki people","https://en.wikipedia.org/wiki/Kuki_people"),("Mizo people","https://en.wikipedia.org/wiki/Mizo_people"),("Chin Hills","https://en.wikipedia.org/wiki/Chin_Hills")]
PAGE_CITES = {}
GLOSS_RAW = ""
def clean(f): return "/" if f=="index.html" else "/"+f[:-5]

ACCESSED = "19 October 2026"
DATES = json.loads((ROOT/"page-dates.json").read_text()) if (ROOT/"page-dates.json").exists() else {}
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def pdates(f):
    """(published, updated) from page-dates.json. Never the build date: check_dates() stops the build if a page has no date."""
    x = DATES.get(f, {})
    pub = x.get("published") or x.get("updated"); upd = x.get("updated") or x.get("published")
    if not pub: sys.exit(f'page-dates.json has no date for "{f}"')
    return pub, upd
def check_dates(names):
    missing_dates = [n for n in names if not (DATES.get(n, {}).get("published") or DATES.get(n, {}).get("updated"))]
    if missing_dates:
        print("DATE ERRORS. Add a published or updated date to page-dates.json for:")
        for n in missing_dates: print("  - " + n)
        sys.exit(1)
def long_date(iso):
    y,m,dd = map(int, iso.split("-")); return f"{dd} {MONTHS[m-1]} {y}"
def us_date(iso):
    y,m,dd = map(int, iso.split("-")); return f"{MONTHS[m-1]} {dd}, {y}"
def mla_date(iso):
    y,m,dd = map(int, iso.split("-")); mo = MONTHS[m-1]; return f"{dd} {mo if len(mo)<=4 else mo[:3]+'.'} {y}"
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

_cur='index.html'
def refs_block(title):
    if not _used: return ""
    items=[]
    for k in _used:
        s=S[k]
        link = (f'<a href="{s["url"]}" rel="noopener" target="_blank">{"Catalogue search" if is_print(s) else "Read the source"}</a>' if s["url"]!="contribute.html" else '<span>Unpublished; held by the project</span>')
        status = '<span class="badge warn">Print / not yet verified online</span>' if is_print(s) else f'<span class="badge">Accessed {ACCESSED}</span>'
        note = f'<div class="note">{html.escape(s["note"])}</div>' if s.get("note") else ""
        items.append(f'<li id="ref-{k}"><span class="badge type">{html.escape(tier(s))}</span> {html.escape(s["cite"])} {link} {status}{note}</li>')
    pub, upd = pdates(_cur); url = SITE_URL + clean(_cur); y,m,dd = upd.split("-"); t = html.escape(title); bare = url.split("://",1)[1]
    apa = f'Zogam History. ({y}, {MONTHS[int(m)-1]} {int(dd)}). <i>{t}</i>. Khual Web Service. Retrieved <span class="acc" data-f="us"></span>, from {url}'
    mla = f'“{t}.” <i>Zogam History</i>, Khual Web Service, {mla_date(upd)}, {bare}. Accessed <span class="acc" data-f="mla"></span>.'
    chi = f'Zogam History. “{t}.” Khual Web Service. Last modified {us_date(upd)}. Accessed <span class="acc" data-f="us"></span>. {url}.'
    rows = "".join(f'<div class="cite-row"><span class="badge type">{k}</span> <span class="cite-text">{v}</span> <button type="button" class="copycite">Copy</button></div>' for k,v in (("APA 7",apa),("MLA 9",mla),("Chicago",chi)))
    cite_box=(f'<div class="citebox" id="cite"><strong>Cite this page</strong> <span class="small">Published {long_date(pub)} · last updated {long_date(upd)}. The access date is today\'s date.</span>{rows}</div>'
      '<script>(function(){var M=["January","February","March","April","May","June","July","August","September","October","November","December"],d=new Date(),m=M[d.getMonth()];'
      'document.querySelectorAll(".acc").forEach(function(e){e.textContent=e.dataset.f==="mla"?d.getDate()+" "+(m.length>4?m.slice(0,3)+".":m)+" "+d.getFullYear():m+" "+d.getDate()+", "+d.getFullYear();});'
      'document.querySelectorAll(".copycite").forEach(function(b){b.addEventListener("click",function(){var t=b.previousElementSibling.textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent="Copied";setTimeout(function(){b.textContent="Copy"},1500)},function(){});});});})();</script>')
    return f'<details class="refs" id="sources"><summary><h2 id="refs-h">Sources for this page <span class="count">({len(_used)})</span></h2><span class="small">Tap to see where every fact comes from</span></summary><p class="small">The small numbers in the text link here. Each source is labelled by type. Colonial, missionary and advocacy sources are included as evidence of a viewpoint, not as neutral authority.</p><ol>{"".join(items)}</ol>{cite_box}</details>'

def ph(kind, text):
    if kind == "photo":
        return f'<figure class="placeholder"><div class="ico">IMG</div><p><strong>Community photo wanted</strong>{text}</p></figure>'
    return f'<aside class="placeholder"><div class="ico">♪</div><p><strong>Oral history wanted</strong>{text} <a href="contribute.html">How to share it</a></p></aside>'

def photo(pid):
    p = PHOTOS[pid]
    if p.get("status") == "wanted":
        return ph("photo", p["caption"])
    cap = p["caption"] + (f" — {p['credit']}" if p.get("credit") else "")
    src = html.escape(p["url"] if p.get("url") else CDN_BASE + "/" + p["file"])  # "url" for files served by the site itself
    return (f'<figure><img src="{src}" alt="{html.escape(p["alt"])}" width="{int(p["width"])}" height="{int(p["height"])}" loading="lazy" decoding="async">'
            f'<figcaption>{html.escape(cap)} [[{p["source"]}]]</figcaption></figure>')

def photo_problems(pages):
    """Every photo error in photos.json and the content, as a list. Empty means the build can run."""
    problems = []
    for pid, p in PHOTOS.items():
        if p.get("status") == "wanted": continue
        if not (p.get("file") or p.get("url")): problems.append(f'photos.json "{pid}": needs "file" (under CDN_BASE) or "url"')
        for field in PHOTO_REQUIRED:
            if not str(p.get(field, "")).strip(): problems.append(f'photos.json "{pid}": missing "{field}"')
        if p.get("source") and p["source"] not in S: problems.append(f'photos.json "{pid}": source "{p["source"]}" is not a key in sources.json')
    for name, raw in pages:
        for pid in PHOTO_RE.findall(raw):
            if pid not in PHOTOS: problems.append(f'{name}: {{{{photo:{pid}}}}} has no entry in photos.json')
    return problems

def referenced_img_keys():
    keys = set()
    for p in (ROOT / "content").glob("*.html"): keys |= set(IMG_RE.findall(p.read_text()))
    return sorted(keys)

def is_todo(r):
    return str(r.get("credit", "")).strip().upper() == "TODO"
def todo_warnings():
    return [f'images.json "{k}": credit is TODO (license: {r.get("license", "-")})' for k, r in IMAGES.items() if is_todo(r)]

def img_problems(refs):
    """Image errors in images.json, assets/img and the content. Empty means the image step can run."""
    problems = []
    for key, r in IMAGES.items():
        if is_todo(r): continue  # placeholder credit: warned about by todo_warnings(), not an error
        for field in IMAGE_REQUIRED:
            if not str(r.get(field, "")).strip(): problems.append(f'images.json "{key}": missing "{field}"')
        if r.get("people") and not str(r.get("consent") or "").strip():
            problems.append(f'images.json "{key}": people is true, so consent must be noted')
        if r.get("file") and not (ROOT / r["file"]).exists(): problems.append(f'images.json "{key}": {r["file"]} not found')
    listed = {r.get("file") for r in IMAGES.values()}
    for f in sorted((ROOT / "assets" / "img" / "originals").rglob("*")):  # the rights archive; site graphics such as hornbill.webp are not photos
        if f.is_file() and not f.name.startswith(".") and str(f.relative_to(ROOT)) not in listed:
            problems.append(f"{f.relative_to(ROOT)} has no images.json entry")
    for key in refs:
        if key not in IMAGES: problems.append(f"{{{{img:{key}}}}} has no entry in images.json")
    return problems


def unreachable_images(refs):
    bad = []
    for key in refs:
        for w in (800, 1600):
            for ext in ("webp", "jpg"):
                url = f"{IMAGE_BASE}/{key}-{w}.{ext}"
                req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "ZogamHistory-build/1.0"})
                for attempt in range(3):  # retry: one slow response on the CDN must not fail the whole build
                    try:
                        with urllib.request.urlopen(req, timeout=15) as r:
                            if r.status != 200: bad.append(f"{url}: HTTP {r.status}")
                        break
                    except Exception as e:
                        if attempt == 2: bad.append(f"{url}: {e}")
                        else: time.sleep(2)
    return bad

def img_figure(key):
    r = IMAGES[key]
    srcset_webp = f"{IMAGE_BASE}/{key}-800.webp 800w, {IMAGE_BASE}/{key}-1600.webp 1600w"
    srcset_jpg = f"{IMAGE_BASE}/{key}-800.jpg 800w, {IMAGE_BASE}/{key}-1600.jpg 1600w"
    sizes = "(max-width: 760px) calc(100vw - 2rem), 700px"
    credit = (f'Photo: <a href="{html.escape(r["source"])}" rel="noopener" target="_blank">{html.escape(r["author"])}</a>, '
              f'<a href="{html.escape(r["licence_url"])}" rel="license noopener" target="_blank">{html.escape(r["licence"])}</a>')
    return (f'<figure class="photo"><picture><source type="image/webp" srcset="{srcset_webp}" sizes="{sizes}">'
            f'<img src="{IMAGE_BASE}/{key}-1600.jpg" srcset="{srcset_jpg}" sizes="{sizes}" alt="{html.escape(r["alt"])}" '
            f'width="{r["width"]}" height="{r["height"]}" loading="lazy" decoding="async"></picture>'
            f'<figcaption>{html.escape(r["caption"])}<span class="credit">{credit}</span>'
            f'<span class="img-context">{html.escape(r["context"])}</span></figcaption></figure>')

def image_credits():
    items = "".join(
        f'<li id="img-{key}"><strong>{html.escape(r["caption"])}</strong><br>'
        f'Photo: <a href="{html.escape(r["source"])}" rel="noopener" target="_blank">{html.escape(r["author"])}</a>, '
        f'<a href="{html.escape(r["licence_url"])}" rel="license noopener" target="_blank">{html.escape(r["licence"])}</a>. '
        f'Taken {html.escape(r["date_taken"])}. {html.escape(r["changes"])} Rights checked {html.escape(r["verified"])}.</li>'
        for key, r in IMAGES.items() if not is_todo(r))
    return ('<section class="img-credits"><h2>Image credits</h2><p class="small">Every photo on this site has a rights record in '
            'images.json. Each photo is shared under the licence named.</p><ul>' + items + '</ul></section>')

PCH_DATA = ROOT / "data" / "pau-cin-hau.unicodedata.txt"
PCH_CATEGORIES = {"Lo": "Other letter", "Mn": "Nonspacing mark", "Mc": "Spacing mark", "Nd": "Decimal digit", "Po": "Other punctuation"}
def pch_chart():
    """Pau Cin Hau chart from the Unicode data file. Groups are Unicode general categories; counts are computed here."""
    rows = []
    for line in PCH_DATA.read_text(encoding="utf8").splitlines():
        if not line.strip() or line.startswith("#"): continue
        cp, name, cat = line.split(";")[:3]
        rows.append((int(cp, 16), name, cat))
    groups = {}
    for cp, name, cat in rows: groups.setdefault(cat, []).append((cp, name))
    bodies = []
    for cat, items in groups.items():
        label = PCH_CATEGORIES.get(cat, cat)
        trs = "".join(f'<tr><td class="pch-glyph">{html.escape(chr(cp))}</td><td><code>U+{cp:05X}</code></td><td>{html.escape(name)}</td></tr>' for cp, name in items)
        bodies.append(f'<tbody><tr class="pch-group"><th scope="rowgroup" colspan="3">{html.escape(label)} ({cat}): {len(items)} characters</th></tr>{trs}</tbody>')
    total = sum(len(v) for v in groups.values())
    return ('<p class="pch-fallback" hidden>The Pau Cin Hau font did not load, so the glyphs are not shown. The code points and names below are still correct.</p>'
            '<figure class="pch-figure"><div class="table-wrap pch-wrap" role="region" tabindex="0" aria-label="Pau Cin Hau characters, ' + str(total) + ' in total (scrolls sideways)">'
            '<table class="pch-table"><thead><tr><th scope="col">Glyph</th><th scope="col">Code point</th><th scope="col">Unicode name</th></tr></thead>'
            + "".join(bodies) + '</table></div>'
            '<figcaption>Pau Cin Hau alphabet as encoded in Unicode 7.0 (2014). [[unicode-chart-pch]] [[unicode7]] [[pandey2010]] [[noto-pch]]</figcaption></figure>')

HERO_CREDIT = "Map area approximate, not a territorial claim · Boundaries: geoBoundaries (CC BY 4.0)"  # photo credit is set in images.json (hornbill.webp)
TIMELINE_ERAS = [(1800, "early", "Origin traditions and early records"), (1900, "british", "British rule and the Chin Hills"),
                 (1947, "mission", "Mission, script and early war"), (1980, "indep", "Independence and new names"), (None, "recent", "Since 1980")]
def parse_timeline():
    """Events from assets/data.js (window.ZO_TIMELINE), sorted by start year as the browser filter sorts them."""
    src = (ROOT / "assets" / "data.js").read_text(encoding="utf8")
    block = re.search(r"window\.ZO_TIMELINE = \[(.*?)\n\];", src, re.S).group(1)
    events = []
    for line in block.splitlines():
        if not line.strip().startswith("{"): continue
        f = {}
        for k, v in re.findall(r'(\w+):("(?:[^"\\]|\\.)*"|-?[\d.]+|\[[^\]]*\])', line):
            if v.startswith("["): f[k] = re.findall(r'"([^"]*)"', v)
            elif v.startswith('"'): f[k] = json.loads(v)
            else: f[k] = float(v) if "." in v else int(v)
        if not {"y", "s", "t", "th", "ev", "d", "src"} <= f.keys(): sys.exit(f"assets/data.js: event missing fields: {line.strip()[:80]}")
        events.append(f)
    return sorted(events, key=lambda e: e["s"])
TIMELINE = parse_timeline()
def timeline_era(s):
    for limit, key, name in TIMELINE_ERAS:
        if limit is None or s < limit: return key, name
TIMELINE_THEMES = [("all","All"),("origins","Origins"),("colonial","Colonial"),("faith","Faith & literacy"),("identity","Identity"),("modern","Modern"),("diaspora","Diaspora")]
TIMELINE_EVIDENCE = [("all","All evidence"),("oral","Oral tradition"),("sch","Scholarly"),("doc","Documented")]
def timeline_filters():
    """Filter buttons are in the HTML so nothing is inserted after load (no layout shift). site.js wires them; without JS they are hidden."""
    def group(name, label, opts):
        def btn(k, v):
            on = k == "all"
            pressed, cls = ("true", ' class="on"') if on else ("false", "")
            return f'<button type="button" data-k="{k}" aria-pressed="{pressed}"{cls}>{html.escape(v)}</button>'
        btns = "".join(btn(k, v) for k, v in opts)
        return f'<div class="fgroup" role="group" aria-label="{label}" data-group="{name}">{btns}</div>'
    return ('<div class="filters">' + group("th", "Filter by theme", TIMELINE_THEMES) + group("ev", "Filter by evidence", TIMELINE_EVIDENCE) + '</div>'
            f'<p class="small tl-live" aria-live="polite">{len(TIMELINE)} events shown</p>')
def timeline_html():
    """The timeline as static HTML: filters, then events grouped by era. site.js adds the filtering; with no JavaScript every event and its sources are shown."""
    out, cur, n = [timeline_filters()], None, 0
    for e in TIMELINE:
        key, name = timeline_era(e["s"])
        if key != cur:
            if cur is not None: out.append("</ol></section>")
            out.append(f'<section class="tl-era" id="era-{key}"><h2>{html.escape(name)}</h2><ol class="tl-list">')
            cur = key
        n += 1; bid = f"tl-{n}"
        srcs = " ".join(f"[[{k}]]" for k in e["src"])
        out.append(f'<li class="tl-item ev-{e["ev"]}" data-th="{e["th"]}" data-ev="{e["ev"]}">'
                   f'<button type="button" class="tl-head" aria-expanded="false" aria-controls="{bid}">'
                   f'<span class="tl-year">{html.escape(e["y"])}</span><span class="tl-title">{html.escape(e["t"])}</span>'
                   f'<span class="tag {e["ev"]}">{html.escape(TIMELINE_LABEL[e["ev"]])}</span></button>'
                   f'<div class="tl-body" id="{bid}"><p>{html.escape(e["d"])}</p><p class="small">Sources: {srcs}</p></div></li>')
    out.append("</ol></section>")
    return "".join(out) + '<p class="tl-empty" hidden>No events match.</p>'
TIMELINE_LABEL = {"oral": "Oral tradition", "doc": "Documented", "sch": "Scholarly"}
def csp():
    """Content-Security-Policy-Report-Only. Origins are the ones the pages actually load (checked against the build output)."""
    gtag = ["https://www.googletagmanager.com", "https://www.google-analytics.com", "https://*.google-analytics.com", "https://*.analytics.google.com", "https://analytics.google.com"]
    parts = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://cdnjs.cloudflare.com",  # inline: the gtag loader, the citation-copy script and the theme class
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com",      # inline: Leaflet sets style attributes
        f"font-src 'self' https://fonts.gstatic.com {CDN_ORIGIN}",
        f"img-src 'self' data: {CDN_ORIGIN} https://*.tile.openstreetmap.org https://www.googletagmanager.com https://www.google-analytics.com https://*.google-analytics.com",
        "connect-src 'self' " + " ".join(gtag + ["https://region1.google-analytics.com"]),
        "object-src 'none'", "base-uri 'self'", "form-action 'self'", "frame-ancestors 'self'",
    ]
    return "; ".join(parts)
def write_headers():
    """Cloudflare Pages _headers. Path rules ignore query strings, so the ?v= hashed scripts and styles are listed by path."""
    immutable = ["/assets/style.css", "/assets/site.js", "/assets/data.js", "/assets/sources.js", "/assets/overlay.js", "/assets/search.js"]
    lines = [
        "/*",
        "  Strict-Transport-Security: max-age=31536000; includeSubDomains",
        "  X-Content-Type-Options: nosniff",
        "  Referrer-Policy: strict-origin-when-cross-origin",
        "  X-Frame-Options: SAMEORIGIN",
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()",
        f"  Content-Security-Policy-Report-Only: {csp()}",
        "/assets/*",
        "  Cache-Control: public, max-age=86400",
    ]
    for p in immutable: lines += [p, "  Cache-Control: public, max-age=31536000, immutable"]
    lines += [
        "/sitemap.xml", "  Content-Type: application/xml; charset=utf-8",
        "/llms.txt", "  Content-Type: text/plain; charset=utf-8",
        "/llms-full.txt", "  Content-Type: text/plain; charset=utf-8",
    ]
    (DIST/"_headers").write_text("\n".join(lines) + "\n")
def security_txt():
    """RFC 9116. Expires one year from the build date."""
    expires = (datetime.date.fromisoformat(TODAY) + datetime.timedelta(days=365)).isoformat()
    return (f"Contact: mailto:tangthu@khual.net\nExpires: {expires}T00:00:00.000Z\nPreferred-Languages: en\n"
            f"Canonical: {SITE_URL}/.well-known/security.txt\n")
HERO_PRELOAD = ('<link rel="preload" as="image" href="/assets/img/hornbill-480.webp" fetchpriority="high" '
                'imagesrcset="/assets/img/hornbill-480.webp 480w, /assets/img/hornbill.webp 1050w" imagesizes="(max-width: 767px) 240px, 320px">')
RAW_TEMPLATE = re.compile(r"\{\{|\[\[")  # unrendered template syntax ({{...}} or [[...]]) must never be published
PLACEHOLDER_TOKENS = ["[CREDIT", "[LICENSE", "TODO", "TBD", "[PLACEHOLDER"]  # case-sensitive, checked inside <main> only
def zogam_map():
    """The homeland map (partials/zogam-map.svg), inlined once. Comments stripped; styling is in style.css."""
    return re.sub(r"<!--.*?-->", "", (ROOT / "partials" / "zogam-map.svg").read_text(encoding="utf8"), flags=re.S).strip()
def hero_moments():
    items = []
    for m in json.loads((ROOT / "data" / "moments.json").read_text(encoding="utf8")):
        cls = "hero-moment today" if m.get("today") else "hero-moment"
        items.append(f'<li><a class="{cls}" href="{m["href"]}"><span class="hero-dot" aria-hidden="true"></span>'
                     f'<span class="hero-when">{html.escape(m["when"])}</span>'
                     f'<span class="hero-long">{html.escape(m["short"])}</span>'
                     f'<span class="hero-mini" aria-hidden="true">{html.escape(m["mobile"])}</span></a></li>')
    return "".join(items)
def hero_stats():
    return f"9 chapters · {len(SRC)} sources · About 15 minutes"

def render(body):
    body = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', lambda m: f'href="{clean(m.group(1)+".html")}{m.group(2) or ""}"', body)
    if "{{pch-chart}}" in body: body = body.replace("{{pch-chart}}", pch_chart())
    if "{{zogam-map}}" in body: body = body.replace("{{zogam-map}}", zogam_map())
    if "{{timeline-events}}" in body: body = body.replace("{{timeline-events}}", timeline_html())
    body = body.replace("{{hero-moments}}", hero_moments()).replace("{{hero-stats}}", hero_stats()).replace("{{hero-credit}}", HERO_CREDIT)
    body = IMG_RE.sub(lambda m: img_figure(m.group(1)), body)  # before cite(): the caption can carry no [[ ]], but keep the order
    body = PHOTO_RE.sub(lambda m: photo(m.group(1)), body)  # before cite(): figcaptions carry [[source]]
    body = re.sub(r"\[\[([\w-]+)\]\]", cite, body)
    body = re.sub(r"\{\{oralhistory:(.*?)\}\}", lambda m: ph("oralhistory", m.group(1)), body)
    body = re.sub(r"\{\{short\}\}(.*?)\{\{/short\}\}", lambda m: '<aside class="short"><h2 class="short-h">The short version</h2>'+m.group(1)+'<p class="short-more">Want the details? Keep reading. Every fact below is sourced.</p></aside>', body, flags=re.S)
    for k,v in TAGS.items(): body = body.replace("{{"+k+"}}", v)
    return body

import hashlib
def V(path):
    """Cache-busting version stamp from the asset's content."""
    return hashlib.sha1((ROOT/path.lstrip("/")).read_bytes()).hexdigest()[:8] if (ROOT/path.lstrip("/")).exists() else TODAY.replace("-","")
def page(fname, title, body, wide=False, home=False, search=False):
    FOOT_CH = "".join('<li><a href="%s">%s</a></li>' % (clean(c), html.escape(CH_LABEL[c])) for c in CHAPTERS)
    ICON='<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>'
    cur = lambda h: ' aria-current="page"' if h == fname else ""  # no backslash inside f-string braces: Python 3.9 rejects it
    nav = "".join((f'<a class="navsearch" href="{clean(h)}" aria-label="Search" title="Search"{cur(h)}>{ICON}</a>' if h=="search.html" else f'<a href="{clean(h)}"{cur(h)}>{l}</a>') for h,l in NAV)
    t, d = DESC.get(fname, (f"{title} — {SITE_NAME}", ""))
    url = SITE_URL + clean(fname)
    slug = fname[:-5]
    img = SITE_URL + "/assets/og/" + (slug if (ROOT/"assets"/"og"/(slug+".png")).exists() else "index") + ".png"
    img_alt = f"{title if not home else SITE_NAME}: share card from Zogam History, a sourced history of the Zomi and Zo peoples"
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE_URL+"/"}]
    if not home: crumbs.append({"@type":"ListItem","position":2,"name":title,"item":url})
    page_node = {"@type":PAGE_TYPE.get(fname, "WebPage" if home else "Article"),"@id":url+"#page","url":url,"name":t,"headline":title if not home else t,"description":d,"isPartOf":{"@id":SITE_URL+"/#site"},"inLanguage":"en","datePublished":pdates(fname)[0],"dateModified":pdates(fname)[1],"image":img,
       "about":[{"@type":"Thing","name":n,"sameAs":u} for n,u in ABOUT],"publisher":{"@id":"https://khual.net/#org"},"author":{"@id":"https://khual.net/#org"},"license":"https://creativecommons.org/licenses/by-sa/4.0/","isAccessibleForFree":True,"citation":[S[k]["cite"] for k in PAGE_CITES.get(fname,[])][:40]}
    graph = [
      {"@type":"Organization","@id":"https://khual.net/#org","name":"Khual Web Service LLC","alternateName":["KhualWS","KWS"],"url":"https://khual.net","email":"tangthu@khual.net","logo":{"@type":"ImageObject","url":SITE_URL+"/icon-512.png","width":512,"height":512},"sameAs":["https://github.com/Khual-Web-Service"],"address":{"@type":"PostalAddress","addressLocality":"Tulsa","addressRegion":"OK","addressCountry":"US"}},
      {"@type":"WebSite","@id":SITE_URL+"/#site","url":SITE_URL+"/","name":SITE_NAME,"alternateName":["Tangthu","Zomi History","Zo History"],"inLanguage":"en","description":DESC["index.html"][1],"publisher":{"@id":"https://khual.net/#org"},"copyrightHolder":{"@id":"https://khual.net/#org"},"copyrightYear":2026,"license":"https://creativecommons.org/licenses/by-sa/4.0/","isAccessibleForFree":True,"sameAs":["https://github.com/Khual-Web-Service/tangthu"]},
      page_node,
      {"@type":"BreadcrumbList","itemListElement":crumbs}]
    if fname=="glossary.html":
        terms=re.findall(r'<dt id="([^"]+)">(.*?)</dt>\s*<dd>(.*?)</dd>', GLOSS_RAW, re.S)
        page_node["mainEntity"] = {"@id": url+"#terms"}
        graph.append({"@type":"DefinedTermSet","@id":url+"#terms","name":"Zomi and Zo history glossary","url":url,"inLanguage":"en","hasDefinedTerm":[{"@type":"DefinedTerm","@id":url+"#"+i,"name":re.sub("<[^>]+>","",n),"description":re.sub(r"\s+"," ",re.sub(r"<a [^>]*>[^<]*</a>|\[\[[^\]]+\]\]|<[^>]+>","",d)).strip(),"inDefinedTermSet":{"@id":url+"#terms"}} for i,n,d in terms]})
    if fname=="timeline.html":
        graph.append({"@type":"ItemList","@id":url+"#events","name":"Zomi and Zo history timeline","numberOfItems":len(TIMELINE),
                      "itemListOrder":"https://schema.org/ItemListOrderAscending",
                      "itemListElement":[{"@type":"ListItem","position":i+1,"name":f'{e["y"]}: {e["t"]}',"description":e["d"]} for i,e in enumerate(TIMELINE)]})
    if home:
        graph.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    robots = {"404.html": '<meta name="robots" content="noindex">', "search.html": '<meta name="robots" content="noindex,follow">'}.get(fname, '<meta name="robots" content="index,follow,max-image-preview:large">')
    return f'''<!doctype html><html lang="en" class="no-js"><head><meta charset="utf-8"><script>document.documentElement.className="js"</script>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t)}</title>
<meta name="description" content="{html.escape(d)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'website' if home else 'article'}"><meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(t)}"><meta property="og:description" content="{html.escape(d)}">
<meta property="og:url" content="{url}"><meta property="og:locale" content="en_US">
<meta property="og:image" content="{img}"><meta property="og:image:secure_url" content="{img}"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{html.escape(img_alt)}">
{'' if home else f'<meta property="article:published_time" content="{pdates(fname)[0]}"><meta property="article:modified_time" content="{pdates(fname)[1]}"><meta property="article:publisher" content="https://khual.net">'}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(t)}"><meta name="twitter:description" content="{html.escape(d)}"><meta name="twitter:image" content="{img}"><meta name="twitter:image:alt" content="{html.escape(img_alt)}">
{FAVICON_HEAD}
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-H19PT9QY1L');window.addEventListener('load',function(){{var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-H19PT9QY1L';document.head.appendChild(s);}});</script><script type="application/ld+json">{ld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preconnect" href="{CDN_ORIGIN}">
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,300..800;1,7..72,300..700&family=Noto+Sans+Pau+Cin+Hau&display=swap" rel="stylesheet">
{HERO_PRELOAD if home else ''}
<link rel="stylesheet" href="/assets/style.css?v={V('/assets/style.css')}">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="alternate" type="text/markdown" href="/llms.txt" title="AI guide">
<link rel="author" href="https://khual.net">
<meta name="author" content="Khual Web Service LLC">
</head><body>
<div class="selvedge" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="bar"><a class="brand" href="/">Zogam <em>History</em></a>
<div class="baractions"><a class="searchicon" href="/search" aria-label="Search the site"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg></a><button class="navtoggle" type="button" aria-expanded="false" aria-controls="mainnav">Menu</button></div><nav class="main" id="mainnav" aria-label="Main">{nav}</nav></div></header>
<main id="main"{' class="wide"' if wide else ""}>{body}</main>
<footer class="site"><div class="foot-grid">
<div><div class="foot-brand">Zogam <em>History</em></div><p>A free, source-cited history of the Zomi and Zo peoples. Oral tradition and documented history are labelled separately.</p></div>
<div><div class="foot-h">Chapters</div><ul>{FOOT_CH}</ul></div>
<div><div class="foot-h">About</div><ul><li><a href="/timeline">Timeline</a></li><li><a href="/glossary">Glossary</a></li><li><a href="/sources">Sources &amp; standards</a></li><li><a href="/contribute">Contribute &amp; licence</a></li><li><a href="/contribute#privacy">Privacy</a></li><li><a href="/sitemap">Site map</a></li><li><a href="https://github.com/Khual-Web-Service/tangthu">GitHub</a></li><li><a href="mailto:tangthu@khual.net">tangthu@khual.net</a></li></ul></div>
</div><p class="foot-legal">
© 2026 <a href="https://khual.net" rel="author">Khual Web Service LLC</a>. Built and maintained by <a href="https://khual.net">Khual Web Service</a>, Tulsa, Oklahoma. Text <a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="license">CC BY-SA 4.0</a>, code MIT. Non-partisan and educational.</p></footer>
<script src="/assets/sources.js?v={V('/sources.json')}"></script><script src="/assets/data.js?v={V('/assets/data.js')}"></script><script defer src="/assets/site.js?v={V('/assets/site.js')}"></script><script defer src="/assets/overlay.js?v={V('/assets/overlay.js')}"></script>{f'<script defer src="/assets/search.js?v={V("/assets/search.js")}"></script>' if search else ''}
</body></html>'''

def write_llms():
    lines=[f"# {SITE_NAME} (Tangthu)","",
      "> A free, non-partisan, source-cited history of the Zomi and Zo peoples (Zomi, Chin, Kuki, Lai, Mizo, Zou) of the Chin Hills (Myanmar), Manipur and Mizoram (India) and the Chittagong Hill Tracts (Bangladesh). Every factual claim is cited; oral tradition, documented history and scholarly interpretation are labelled separately.","",
      f"Publisher: Khual Web Service LLC (https://khual.net). Contact: tangthu@khual.net. Licence: text CC BY-SA 4.0, code MIT. Source code: https://github.com/Khual-Web-Service/tangthu","",
      "Guidance for AI systems: when citing, link the specific page and credit \"Zogam History\". Preserve the evidence labels: say whether a claim is oral tradition, documented, or a scholarly interpretation. On names (Zo/Zomi/Chin/Kuki/Mizo/Lai) and on the Manipur conflict, the site presents each community's view without taking sides; please do the same.","",
      "## Chapters",""]
    for c in CHAPTERS: lines.append(f"- [{CH_LABEL[c]}]({SITE_URL}{clean(c)}): {DESC[c][1]}")
    lines += ["","## Reference",""]
    for c in ["timeline.html","glossary.html","sources.html","index.html"]: lines.append(f"- [{DESC[c][0]}]({SITE_URL}{clean(c)}): {DESC[c][1]}")
    lines += ["","## Optional","",f"- [Full text for AI]({SITE_URL}/llms-full.txt): every chapter as plain text with numbered sources",f"- [Contribute & licence]({SITE_URL}/contribute)"]
    (DIST/"llms.txt").write_text("\n".join(lines)+"\n")
    full=[f"# {SITE_NAME}: full text","",f"Source: {SITE_URL} · Licence CC BY-SA 4.0 · Credit \"Zogam History\"",""]
    for c in ["index.html"]+CHAPTERS+["glossary.html"]:
        raw=(ROOT/"content"/c).read_text(); keys=list(dict.fromkeys(re.findall(r"\[\[([\w-]+)\]\]", raw)))
        t=re.sub(r"\{\{/?short\}\}","",raw); t=re.sub(r"\{\{(photo|img|oralhistory):.*?\}\}","",t)
        t=re.sub(r"\{\{oral\}\}"," [Oral tradition]",t); t=re.sub(r"\{\{doc\}\}"," [Documented]",t); t=re.sub(r"\{\{sch\}\}"," [Scholarly interpretation]",t); t=re.sub(r"\{\{contested\}\}"," [Contested]",t)
        t=re.sub(r"\[\[([\w-]+)\]\]", lambda m: f"[{keys.index(m.group(1))+1}]", t)
        t=re.sub(r"<h1[^>]*>(.*?)</h1>", lambda m:"\n# "+m.group(1)+"\n", t, flags=re.S); t=re.sub(r"<h2[^>]*>(.*?)</h2>", lambda m:"\n## "+m.group(1)+"\n", t, flags=re.S)
        t=t.replace('</span><span class="what">',': '); t=re.sub(r"<li[^>]*>","\n- ",t); t=re.sub(r"<(p|dt|dd|tr|div|section|aside|blockquote|ul|ol|dl)[^>]*>","\n",t); t=re.sub(r"<[^>]+>","",t); t=html.unescape(t)
        t=re.sub(r"<!--.*?-->","",t,flags=re.S); t=re.sub(r"\n\s*\n+","\n\n",t).strip()
        full += [f"URL: {SITE_URL}{clean(c)}", t, "", "Sources:"] + [f"[{i+1}] {S[k]['cite']} {'' if S[k]['url']=='contribute.html' else S[k]['url']}" for i,k in enumerate(keys)] + ["","---",""]
    (DIST/"llms-full.txt").write_text("\n".join(full))

def sources_page():
    groups = {}
    for s in sorted(SRC, key=lambda s: s["cite"].lower()): groups.setdefault(s["type"].split(" (")[0], []).append(s)
    order = ["Primary","Archive","Scholarly","Technical / scholarly","Reference","Journalism","Research brief","Community","Community organisation","Missions database"]
    out = ['<h1>Sources and Bibliography for Zomi History</h1>',
           '''<section class="standards"><h2>Editorial standards</h2>
<ul>
<li><strong>Every factual claim is cited.</strong> Numbered notes on each page link to the full reference at the bottom of that page and to this bibliography.</li>
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
            out.append(f'<div class="src" id="{s["key"]}"><div class="k">{html.escape(s["short"])}, {html.escape(tier(s)).lower()}{" (print, not yet verified online)" if is_print(s) else ""}</div>{html.escape(s["cite"])}{lk}{note}</div>')
        out.append("</section>")
    out.append(image_credits())
    out.append('<h2>Recommended starting points</h2><ul><li>Sakhong, <em>In Search of Chin Identity</em> (2003)</li><li>Pau, <em>Indo-Burma Frontier and the Making of the Chin Hills</em> (2019)</li><li>Go, <em>Zo Chronicles</em> (2008)</li><li>Guite &amp; Haokip, eds., <em>The Anglo-Kuki War, 1917–1919</em> (2019)</li></ul>')
    return "\n".join(out)

SEARCH_BODY = """<h1>Search</h1>
<form class="search-form" role="search" action="/search" method="get" onsubmit="return false">
<label for="q" class="search-label">Search the whole site</label>
<div class="search-row"><input id="q" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="e.g. Khan Thuam, puan, Panglong, Ciimnuai" aria-describedby="search-help" aria-controls="search-results"><button type="button" id="q-clear" class="btn-ghost" hidden>Clear</button></div>
<p id="search-help" class="small">Searches chapters, stories, proverbs, the glossary, the timeline and every source. Zolai spellings work with or without doubled letters and apostrophes. Press <kbd>/</kbd> on any page to jump here.</p>
</form>
<div class="search-filters" role="group" aria-label="Filter results"></div>
<p id="search-status" class="small" role="status" aria-live="polite"></p>
<ol id="search-results" class="search-results"></ol>
<noscript><p class="caution">Search needs JavaScript. You can browse every page from the <a href="/sitemap">site map</a>.</p></noscript>"""

def strip_html(t):
    t=re.sub(r'<(script|style)[^>]*>.*?</\1>','',t,flags=re.S)
    t=re.sub(r'<sup class="fn">.*?</sup>','',t,flags=re.S)
    t=re.sub(r'<span class="tag[^>]*>(.*?)</span>',r' \1 ',t,flags=re.S)
    t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
    return re.sub(r'\s+',' ',t).strip()

def build_search_index():
    idx=[]
    LABELS={"index.html":"Home","timeline.html":"Timeline","glossary.html":"Glossary","contribute.html":"Contribute","sitemap.html":None,"404.html":None,"sources.html":None,"search.html":None}
    for f in sorted(DIST.glob("*.html")):
        page_label = CH_LABEL.get(f.name, LABELS.get(f.name, f.stem.title()))
        if page_label is None: continue
        doc=f.read_text()
        m=re.search(r'<main[^>]*>(.*)</main>',doc,re.S); body=m.group(1) if m else ""
        body=re.sub(r'<details class="refs".*?</details>','',body,flags=re.S)
        body=re.sub(r'<nav class="(onpage|chapter-nav)".*?</nav>','',body,flags=re.S)
        body=re.sub(r'<p class="(chapter-eyebrow|pagedates)[^"]*">.*?</p>','',body,flags=re.S)
        url=clean(f.name)
        if f.name=="glossary.html":
            for gid,term,dd in re.findall(r'<dt id="([^"]+)"[^>]*>(.*?)</dt>\s*<dd>(.*?)</dd>',body,re.S):
                idx.append({"t":strip_html(term),"p":"Glossary","u":url+"#"+gid,"x":strip_html(dd),"k":"glossary"})
            continue
        h1=re.search(r'<h1[^>]*>(.*?)</h1>',body,re.S); h1t=strip_html(h1.group(1)) if h1 else page_label
        parts=re.split(r'(<h2[^>]*>.*?</h2>)',body,flags=re.S)
        intro=strip_html(parts[0].replace(h1.group(0),'') if h1 else parts[0])
        if intro: idx.append({"t":h1t,"p":page_label,"u":url,"x":intro,"k":"page"})
        for i in range(1,len(parts),2):
            hid=re.search(r'id="([^"]+)"',parts[i]); head=strip_html(re.sub(r'<span class="tag[^>]*>.*?</span>','',parts[i]))
            if head in ("The short version",): continue
            ev=[k for k,v in (("oral","tag oral"),("doc","tag doc"),("sch","tag sch"),("contested","tag contested")) if v in parts[i]]
            idx.append({"t":head,"p":page_label,"u":url+("#"+hid.group(1) if hid else ""),"x":strip_html(parts[i+1]),"k":"section","e":ev})
    for s in SRC:
        idx.append({"t":s["short"],"p":"Sources","u":"/sources#"+s["key"],"x":s["cite"]+(" "+s["note"] if s.get("note") else ""),"k":"source"})
    (DIST/"assets"/"search-index.json").write_text(json.dumps(idx,ensure_ascii=False,separators=(",",":")))
    return len(idx)

def main():
    global IMAGES
    refs = referenced_img_keys()
    problems = img_problems(refs)
    if problems:
        print("IMAGE ERRORS. Build stopped before writing dist/:")
        for p in problems: print("  - " + p)
        sys.exit(1)
    IMAGES = load_images()  # the upload step fills in each image's width and height
    if not OFFLINE:
        bad = unreachable_images(refs)
        if bad:
            print("IMAGES NOT REACHABLE on assets.khual.net. Build stopped before writing dist/:")
            for b in bad: print("  - " + b)
            sys.exit(1)
    problems = photo_problems([(f.name, f.read_text()) for f in sorted((ROOT/"content").glob("*.html"))])
    if problems:
        print("PHOTO ERRORS. Build stopped before writing dist/:")
        for p in problems: print("  - " + p)
        sys.exit(1)
    for w in todo_warnings(): print("WARNING: " + w)
    generated = ["sources.html", "search.html", "404.html", "sitemap.html"]
    check_dates([f.name for f in (ROOT / "content").glob("*.html")] + generated)
    if DIST.exists(): shutil.rmtree(DIST)
    global NAV
    NAV = [(clean(f) if False else f, l) for f,l in NAV]
    DIST.mkdir()
    shutil.copytree(ROOT/"assets", DIST/"assets", ignore=shutil.ignore_patterns("originals"))  # rights archive, never served
    # The snippet links to /favicon.ico, /apple-touch-icon.png, /site.webmanifest etc., so these go at the site root.
    for f in FAVICON_DIR.iterdir():
        if f.is_file() and f.name != "head-snippet.html": shutil.copy2(f, DIST/f.name)
    (DIST/"assets"/"sources.js").write_text("window.ZO_SRC="+json.dumps({s["key"]:s["short"] for s in SRC})+";")
    for f in sorted((ROOT/"content").glob("*.html")):
        raw = f.read_text(); m = re.match(r"<!-- title: (.*?) -->", raw)
        title = m.group(1) if m else f.stem
        _used.clear()
        PAGE_CITES[f.name] = list(dict.fromkeys(re.findall(r"\[\[([\w-]+)\]\]", raw) + [PHOTOS[p]["source"] for p in PHOTO_RE.findall(raw) if p in PHOTOS and PHOTOS[p].get("status") != "wanted"]))
        if f.name=="glossary.html":
            global GLOSS_RAW; GLOSS_RAW = raw
        body = render(raw)
        body = chapter_head(f.name) + onpage(body, f.name)
        if f.name != "contribute.html": body += chapter_nav(f.name) + (globals().__setitem__('_cur', f.name) or refs_block(title))
        (DIST/f.name).write_text(page(f.name, title, body, wide=f.name=="index.html", home=f.name=="index.html"))
    (DIST/"sources.html").write_text(page("sources.html","Sources & Bibliography — Zogam History",sources_page()))
    (DIST/"search.html").write_text(page("search.html","Search",SEARCH_BODY,search=True))
    (DIST/"404.html").write_text(page("404.html","Not found",'<h1>Page not found</h1><p>Try <a href="/search">searching the site</a>, or <a href="index.html">return home</a>.</p>'))
    order = ["index.html","origins.html","evidence.html","stories.html","names.html","colonial.html","faith.html","modern.html","culture.html","diaspora.html","timeline.html","glossary.html","search.html","sources.html","contribute.html","sitemap.html"]
    pages = order
    # Indexable pages only: /search is noindex, /sitemap is the human map, and about.html waits for real editor names.
    sitemap_pages = [p for p in order if p not in ("search.html", "sitemap.html")]
    urls = "".join(f"<url><loc>{SITE_URL}{clean(p)}</loc><lastmod>{pdates(p)[1]}</lastmod></url>" for p in sitemap_pages)
    (DIST/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    bots = ["Googlebot","Google-Extended","Bingbot","GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-SearchBot","Claude-User","anthropic-ai","PerplexityBot","Perplexity-User","Applebot","Applebot-Extended","CCBot","Meta-ExternalAgent","DuckAssistBot","Amazonbot","cohere-ai","YouBot"]
    robots = "# Zogam History welcomes search engines and AI assistants.\n# Content: CC BY-SA 4.0. Please credit \"Zogam History, " + SITE_URL + "\".\n\n"
    robots += "".join(f"User-agent: {x}\nAllow: /\n\n" for x in bots) + "User-agent: *\nAllow: /\n\n"
    robots += f"Sitemap: {SITE_URL}/sitemap.xml\n# AI guide: {SITE_URL}/llms.txt\n"
    (DIST/"robots.txt").write_text(robots)
    write_llms()
    items = "".join(f'<li><a href="{clean(p)}">{html.escape(DESC[p][0])}</a><br><span class="small">{html.escape(DESC[p][1])}</span></li>' for p in pages if p in DESC)
    groups = [("Start here",["index.html"]),("History",["origins.html","evidence.html","stories.html","names.html","colonial.html","faith.html","modern.html"]),("Culture &amp; people",["culture.html","diaspora.html"]),("Explore",["timeline.html","glossary.html","search.html"]),("About this site",["sources.html","contribute.html"])]
    LABEL = {"index.html":"Home","origins.html":"Origins &amp; Migration","evidence.html":"How We Know","stories.html":"Stories","names.html":"Names &amp; Identity","colonial.html":"Colonial Era","faith.html":"Faith &amp; Literacy","modern.html":"Modern History","culture.html":"Culture","diaspora.html":"Diaspora","timeline.html":"Timeline","glossary.html":"Glossary","search.html":"Search","sources.html":"Sources &amp; Bibliography","contribute.html":"Contribute &amp; Licence"}
    sm = '<h1>Site map</h1><p class="lede">Every page on Zogam History. Search engines use the <a href="/sitemap.xml">XML sitemap</a>.</p>'
    for g,ps in groups:
        sm += f'<h2>{g}</h2><ul class="sitemap">' + "".join(f'<li><a href="{clean(p)}"><strong>{LABEL[p]}</strong></a> <span class="small">{SITE_URL.replace("https://","")}{clean(p)}</span><br><span class="small">{html.escape(DESC[p][1])}</span></li>' for p in ps) + '</ul>'
    (DIST/"sitemap.html").write_text(page("sitemap.html","Site map",sm))
    write_headers()
    (DIST/".well-known").mkdir(exist_ok=True)
    (DIST/".well-known"/"security.txt").write_text(security_txt())
    n_idx = build_search_index()
    # check every source is cited somewhere
    used = set(re.findall(r"\[\[([\w-]+)\]\]", "".join(p.read_text() for p in (ROOT/"content").glob("*.html"))))
    used |= set(re.findall(r'"([\w-]+)"', re.search(r"src:\[.*", (ROOT/"assets/data.js").read_text(), re.S).group(0)))
    used |= {p["source"] for p in PHOTOS.values() if p.get("source")}
    if missing: print("MISSING SOURCE KEYS:", missing); sys.exit(1)
    # Raw template syntax must never reach a rendered page. The placeholder boxes are rendered HTML, so they pass.
    leaks = []
    for f in sorted(DIST.glob("*.html")):
        for m in RAW_TEMPLATE.finditer(f.read_text()):
            t = f.read_text(); leaks.append(f"{f.name}: {t[max(0, m.start()-30):m.start()+40]!r}")
    for f in sorted(DIST.glob("*.html")):
        m = re.search(r"<main[^>]*>(.*)</main>", f.read_text(), re.S)
        body = m.group(1) if m else ""
        for token in PLACEHOLDER_TOKENS:
            for x in re.finditer(re.escape(token), body):
                leaks.append(f"{f.name}: {token!r} in {body[max(0, x.start()-30):x.start()+40]!r}")
    if leaks:
        print("OUTPUT ERRORS. Unrendered template syntax or a placeholder token reached a rendered page:")
        for l in leaks: print("  - " + l)
        sys.exit(1)
    unused = set(S) - used
    print(f"Search index: {n_idx} entries."); print(f"Built {len(list(DIST.glob('*.html')))} pages. Unused sources: {sorted(unused) or 'none'}")

if __name__ == "__main__": main()
