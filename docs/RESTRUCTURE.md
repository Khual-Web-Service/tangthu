# Restructure plan: Python static build

Phase 0 (audit, no code changes). Goal: visitors see the same URLs, the same rendered HTML (apart from whitespace) and the same features.

## 1. Current setup

| Part | Where it lives | Notes |
|---|---|---|
| Build script | `build.py` (481 lines, one file) | Reads content, renders, writes `dist/`. Functions in order: data loading, citations (`cite`, `refs_block`), placeholders (`photo`, `img_figure`, `ph`), `render`, `page` (head, nav, footer, JSON-LD), `write_llms`, `sources_page`, `build_search_index`, `main`. |
| Chapter bodies | `content/*.html`, 17 files (9 chapters, `index`, `timeline`, `glossary`, `contribute`, `names`, plus `evidence`, etc.) | Inline HTML with custom tags: `{{short}}…{{/short}}`, `{{oral}}`/`{{doc}}`/`{{sch}}`/`{{contested}}` tags, `[[source-key]]` citations, `{{photo:id}}`, `{{img:key}}`, `{{oralhistory:…}}`. |
| Sources | `sources.json` (135 entries, key → citation) | Generated `assets/sources.js` for the timeline page. |
| Photos | `photos.json` (wanted placeholders), `images.json` (rights records, 2 photos) | Image files on R2 (`assets.khual.net`). `assets/img/originals/` is the rights archive, excluded from `dist/`. |
| Timeline and places | `assets/data.js` (`ZO_TIMELINE`, `ZO_PLACES`, `ZO_REGIONS`) | JavaScript, loaded on every page. |
| Client JS | `assets/site.js`, `assets/search.js`, `assets/overlay.js`, `assets/sources.js` (generated) | Hand-written, no bundler. |
| CSS | `assets/style.css` (one file, design tokens on `:root`) | Dark mode via `prefers-color-scheme`. |
| Asset versioning | `?v=<sha1 of file>` in HTML (`V()` in `build.py`) | Only CSS and JS. |
| Structured data | JSON-LD built in `page()` (Organization, WebSite, WebPage/Article, BreadcrumbList, FAQPage, DefinedTermSet) | Also `<meta>` OG/Twitter tags, canonical. |
| SEO files | `sitemap.xml`, `sitemap.html`, `robots.txt`, `llms.txt`, `llms-full.txt` | Written by `main()`. |
| Headers | `dist/_headers` (written by `main()`) | Cloudflare Pages / Workers static assets config in `wrangler.jsonc`. |
| Output | `dist/` (gitignored), 51 files, about 1.7 MB | |
| Reference copy | `dist_before/` (built from the current code before this audit, kept outside the repo) | Used for the before/after comparison below. |

## 2. Target structure (from the request)

```
content/chapters/01-origins.md … 09-diaspora.md
content/stories/*.md
content/pages/*.md
data/{glossary,timeline,sources,proverbs,site}.yaml
templates/{base,chapter,story,page,search}.html, partials/{header,footer,onpage-nav,citation,shortcallout}.html
assets/{css,js,img,fonts}
build/{__main__,content,render,citations,search_index,assets,seo,validate,serve}.py
tests/   dist/   requirements.txt or pyproject.toml (pinned)
```

## 3. Mapping: current → target

| Current | Target |
|---|---|
| `content/*.html` bodies | `content/chapters/*.md` (Markdown + YAML header). Inline HTML stays allowed where Markdown can't express it (figures, tables, the short callout), via shortcodes. |
| `sources.json` | `data/sources.yaml`, same keys as ids (`carey1896` becomes `carey-tuck-1896`, see Risks). |
| `data.js` (timeline, places) | `data/timeline.yaml`; places stay in JS if the map needs them unchanged. |
| `glossary` and `proverbs` in `content/*.html` | `data/glossary.yaml`, `data/proverbs.yaml`. |
| `page()` head, header, footer | `templates/base.html` with partials. |
| `render()`, placeholders | `build/render.py` (Jinja2 environment, filters, shortcodes). |
| `cite()`, `refs_block()` | `build/citations.py`: `[@id]` → numbered footnotes, per-page reference list. |
| `build_search_index()` | `build/search_index.py`, writes `dist/assets/search-index.json`. |
| `V()` cache stamps | `build/assets.py` writes `manifest.json` and hashed names. |
| JSON-LD, sitemap, robots, llms | `build/seo.py`. |
| Checks now in `main()` (photo, image, missing source) | `build/validate.py`, same rules, run before any output is written. |
| `python3 build.py` | `python -m build` (`--dev` for the rebuild-on-save server, `--serve` to host it). |
| `scripts/serve_dist.py` | `build/serve.py`, using `watchfiles`. |

## 4. Risks and how each one is checked

1. **Visitors must not notice.** Same URLs (`/origins`, not `/origins.html`), same status codes, same HTML apart from whitespace. Check: normalise whitespace in `dist_before/` and the new `dist/`, then diff every page. Any difference must be explained or fixed before old code is removed.
2. **Hashed asset names change the HTML.** Visitors won't see this, but `?v=` stamps become `app.3f9a1c.css`. Old cached copies still work until they expire. Check: `manifest.json` covers every asset the HTML names.
3. **Citation numbering.** Footnotes are numbered per page in order of first use. The rewrite must produce the same numbers and the same reference list. Check: the same diff as (1), plus a count of citations per page.
4. **Source ids.** Renaming `carey1896` → `carey-tuck-1896` changes every anchor (`/sources#carey1896`) and any link from outside the site. Decision needed: keep the old keys as aliases, or do not rename.
5. **Markdown with HTML.** Some content uses inline tags the Markdown parser would change (`<details>`, `<figure>`, `<picture>`, `<dl>`). Check: the rendered-HTML diff catches any drift. Shortcodes keep the output identical.
6. **Search index.** The index and the search engine must produce the same results. Check: the parity queries used for the overlay (Khan Thuam, kam hau, Cimnuai) plus a fixed list of ~30 queries, compared against `dist_before/`.
7. **SEO and structured data.** JSON-LD and `dateModified` come from `page-dates.json`. The move to YAML must keep the dates. Check: diff of the `<script type="application/ld+json">` blocks.
8. **Image rights.** `images.json` checks and the reachability check run before output is written. They must still fail the build on the same bad inputs (tested before: missing key, missing consent, missing source).
9. **Dependencies.** The site has no Python dependencies today. The new build needs Jinja2, markdown-it-py, PyYAML, watchfiles, plus boto3 and Pillow for the image step. Pinned in `requirements.txt`. Node is not needed.
10. **Deleting the old code.** Done last, only after the diff from (1) and (3) is empty and the tests pass. Until then `build.py` stays in the repo.

## 5. Phases

1. **Audit** (this document, plus `dist_before/`). No code changes.
2. **Scaffold the new build** next to the old one (`build/` package, `dist_new/`). Nothing in `dist/` changes.
3. **Port the data**: sources, timeline, glossary, proverbs into `data/`. Validate: every citation key used in content exists.
4. **Port the content** chapter by chapter to Markdown. After each chapter, diff that page against `dist_before/` (whitespace-normalised). Stop on any difference.
5. **Port templates, citations, SEO, search index, assets.** Diff all pages, `sitemap.xml`, `robots.txt`, `llms*.txt`, `search-index.json`.
6. **Port the dev server** (`build/serve.py`) and tests (`tests/`).
7. **Switch over**: `dist/` built by the new code. Re-run the full diff. Remove `build.py`, `scripts/serve_dist.py` and the old asset stamps only after step 7 passes.

## 6. Decisions needed before phase 2

- Keep the old source keys as aliases (recommended), or rename them?
- Convert all 17 HTML files to Markdown, or only the chapters and pages, leaving `timeline`, `glossary` and `contribute` as HTML templates?
- Does the timeline/map (`data.js`) move to YAML now, or stay as JavaScript?
