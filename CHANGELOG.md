# Changelog

All notable changes to Zogam History are recorded here.

## 2026-10-20 (phone moments: swipe row)

### Changed
- Phones: "The story in six moments" is one horizontal swipe row again, with cards 150px wide, snap points, and no vertical scrolling. Cards grow to fit their text.
- Replaces the two-column grid from the previous commit.

## 2026-10-20 (phone moments grid)

### Changed
- Phones: "The story in six moments" is a two-column grid (three rows) instead of a horizontal scroller. The row no longer scrolls sideways (scroll width equals client width at 390px). Cards grow to fit their text, so none are clipped. The moments sit below the fold; the fold for the title, one-liner, buttons and link is unchanged (link bottom 836px).

## 2026-10-20 (phone hero gutter)

### Changed
- Phones: hero text, moments heading and timeline cards start 24px from the edge (was 16px), clear of the 6px weave border. Button spans 24–366px at 390px wide. Fold unchanged: link bottom 836px.

## 2026-10-20 (build runs on Python 3.9)

### Fixed
- `build.py` no longer uses a backslash inside an f-string expression (the `aria-current` attribute in the header nav). Python 3.9 rejects that syntax, so the build failed there. Output is unchanged.

## 2026-10-20 (A3 hero, desktop map clears the timeline)

### Changed
- Desktop (1024px and up): the map column is sized from the hero height and stops 260px above the bottom, so it no longer runs into the "Six moments" strip. Width follows the map's 420:680 aspect ratio, so the map is no longer forced to the full column width.
- Hornbill positions are percentages of the map column, so it stays on the homeland at every width.
- Measured: map bottom 17px above the moments strip at 1024×768, 41px at 1342×900 and 1440×900. Hero fits the 900px viewport at 1342 and 1440.
- Known: at 1024×768 the hero is 760px tall (minimum), so it runs 65px past a 768px viewport.

## 2026-10-20 (A3 hero, phone fixes)

### Changed
- Phones (under 768px): map scale 0.75 (307×497 px) at top −50px, so the homeland clears the fade. Map block 330px, so the text link ends at 836px in an 844px viewport.
- Hornbill: 240px wide, 8px below the header, bird's own cutout (1050×708). Alpha hit test: 0 hits on every label and dot at 390×844 and 430×932.
- Labels: 20 units inside the map (about 15px on screen), halo kept. Kalemyo is hidden below 768px. Tedim clears the fade by 40px.
- INDIA 21px from the left edge (16px minimum).
- "Start reading": #102014 text, weight 600.

### Changed (build)
- `HERO_CREDIT` no longer includes "Photo: [CREDIT / LICENSE]". Photo credit lives in `images.json`: `hornbill.webp` is `"credit": "TODO"`. The build prints a warning and does not publish the entry.

### Known gaps
- Headroom above the land is not achieved: the homeland begins at the top of the block. Clearing the bird from the land needs either a shorter fade, a smaller map, or a taller block, and the fold rules out a taller block.
- The Churachandpur dot is 0.4px below the nearest wing tip.

## 2026-10-20 (analytics privacy note)

### Added
- **Privacy & analytics** section on the Contribute page (`#privacy`). It says what Google Analytics collects, that names and emails are not collected through it, how to opt out, and links Google's policy pages.
- **Privacy** link in the footer, to `/contribute#privacy`, on every page.

## 2026-10-20 (Pau Cin Hau alphabet chart)

### Added
- **Pau Cin Hau chart** on the Faith & Literacy page: all 57 characters of U+11AC0–11AF8, with glyph, code point and Unicode name. The rows are generated at build time from `data/pau-cin-hau.unicodedata.txt` (UnicodeData.txt). Every character is general category Lo (other letter) and was assigned in Unicode 7.0, per DerivedAge.txt. The table scrolls sideways within its own box on phones. If the font does not load, a note replaces the glyphs.
- **Noto Sans Pau Cin Hau** (subset covering this block, 7.3 KB, woff2) self-hosted at `https://assets.khual.net/tangthu/fonts/`, with its OFL-1.1 licence file. Source files are in `fonts/`.
- `scripts/upload_images.py` also uploads the files listed in `fonts.json`, under the same never-overwrite rule.

## 2026-10-20 (Google Analytics)

### Added
- Google tag (G-H19PT9QY1L) on every page, added in the build's page head.

## 2026-10-20 (uploads out of the build)

### Changed
- `python3 build.py` no longer uploads images or needs R2 credentials. It only checks that images are reachable on assets.khual.net. Uploads are run manually with `scripts/upload_images.py`. `--no-upload` is replaced by `--offline`, which skips the reachability check.

## 2026-10-20 (landing hero, A3 design)

### Changed
- **Home hero rebuilt to the approved A3 design.** A dark hero with the headline, the homeland map (`partials/zogam-map.svg`, inlined once and cropped per breakpoint with CSS), the great hornbill cut-out (`assets/img/hornbill.webp`, placeholder until the licensed photo arrives), and the six-moments timeline. On phones the timeline is swipe cards; on tablets a 3 x 2 grid; on desktop a 6-column timeline across the bottom.
- **Six moments come from one list** (`data/moments.json`). The old six-moments section below the hero has been removed, since the hero timeline replaces it. The long descriptions are gone; each moment links to its chapter.
- **Map labels** INDIA, MYANMAR and BANGLADESH added; Churachandpur labelled to the left of its dot.
- **Leaflet** no longer loads with the home page. It loads when the map section nears the screen.
- The hero's bird and map animate in (CSS only); the bird stays still. Reduced motion turns the animation off.

### Credit
- The photo credit is a placeholder, `[CREDIT / LICENSE]`, in `build.py` (`HERO_CREDIT`). The map boundaries credit (geoBoundaries, CC BY 4.0) is shown beside it.

## 2026-10-20 (live search overlay)

### Added
- **Search overlay on every page.** Opens from the header search icon, from `/` and from Ctrl/Cmd+K. It shows the top 8 results grouped as Pages, Glossary, Timeline and Sources, each with a highlighted snippet. Arrow keys move through the results, Enter opens one, and Esc closes it. The last row, "See all N results", goes to `/search?q=…`. With no query it suggests three searches. It has a focus trap, a labelled dialog, a combobox, and it locks page scrolling.
- **Lazy loading.** The overlay script is small. The search engine (`search.js`, 5.7 KB) and the index (about 103 KB raw, about 36 KB gzipped) load the first time the overlay opens, or when the search icon is hovered or focused. Pages that are never searched don't download them.

### Changed
- **One search engine.** `assets/search.js` exposes `ZoSearch.search(query, {type, limit})`, used by both the `/search` page and the overlay. Ranking, Zolai spelling handling (doubled vowels, apostrophes) and highlighting are unchanged. `/search` gives the same results as before on the queries checked.
- `/` now opens the overlay on chapter pages. On `/search` it still focuses the page's own box.

## 2026-10-20 (desktop reading layout)

### Changed
- **Text size and column (shared tokens).** From 1024px the root text is 110%, so body text is about 19.4px, with line-height 1.68. The column is `--measure` at 39rem (686px), about 70 characters a line. Headings, the lead and the short-version box are rem-based, so they scale with it. Below 1024px nothing changes.
- **Minimum 15px** for meta text, footnote text, captions, labels and table headings, through the `--meta` token. Footnote numbers are at least 15px too. The pill bar below 1200px is unchanged.
- **"On this page" at 1200px and wider** is a sticky vertical list in the left gutter (200px, 40px gaps). It uses the same markup and links as the pill bar. The active section gets a green label and left border. Below 1200px it stays the pill bar.
- **Wide tables at 1200px and wider** span the text column and the right gutter, up to 900px. They stay left-aligned with the text, so they don't overlap the sidebar. Below 1200px, tables scroll sideways inside their own box, which has a subtle edge cue.
- **Section highlighting** uses one IntersectionObserver in `assets/site.js`, replacing the old scroll-spy that measured the pill bar.
- In-page links scroll smoothly, unless the user prefers reduced motion. Headings clear the sticky header on desktop.

## 2026-10-20 (rights-checked images)

### Added
- **`images.json`**, the rights record for every photo. Each entry gives the author, licence and licence URL, source, date taken, changes, context and the date rights were checked. People need a consent note.
- **`{{img:key}}` tag.** It renders a `<figure>` with a `<picture>` (WebP, JPG fallback, 800 and 1600 px), lazy loading and the credit line. Photos are served only from `https://assets.khual.net/tangthu/img/`.
- **Two photos, both CC BY-SA 4.0 by Ericwinny (Wikimedia Commons):** Kennedy Peak on the Origins page, and Tedim seen from the south in the Ciimnuai section of Stories.
- **`scripts/upload_images.py`** makes the web versions (1600 and 800 px, WebP and JPG, EXIF removed) and uploads what R2 does not have. It has `--dry-run`, skips identical files, never overwrites and never deletes.
- **Image credits** section on the Sources page, generated from `images.json`.
- **Build checks.** The build stops if an image key is missing, a rights field is empty, consent is missing for a photo of people, or an original has no record. It also checks that every `{{img:…}}` image is reachable on assets.khual.net. `--no-upload` skips the upload and the reachability check.

### Changed
- The Kennedy Peak photo moved from `photos.json` to `images.json`. Its old site-hosted copy was removed.
- `assets/img/originals/` is excluded from the published site.
- The preview server builds with `--no-upload`, so saving a file never uploads anything.
- `README.md` gains an "Adding images" section.

## 2026-10-20 (Kennedy Peak photo)

### Added
- **Photo on the Origins page:** "Kennedy Peak, seen from the Kalay–Tedim road." Photo by Ericwinny, licensed CC BY-SA 4.0, from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:KennedyPeak.jpg). Resized to 1200 px and converted to WebP, and the credit line says so. Served from `assets/photos/origins/`, not from R2, because `wrangler` is currently broken on this machine. Move it to R2 once that's fixed.
- A `url` option in `photos.json` for photos served by the site itself. Entries with `file` still use R2.

## 2026-10-20 (Zogam favicons)

### Changed
- **Site icons** now come from `zogam-favicons/`. The build copies its icon files to the site root (`favicon.ico`, `favicon.svg`, `favicon-16/32.png`, `apple-touch-icon.png`, `icon-192/512.png`, `site.webmanifest`) and puts `zogam-favicons/head-snippet.html` into every page's `<head>`. This replaces the old `/assets/favicon.svg` link.
- The theme colour is now `#E4133D` (from the favicon snippet), replacing `#9a4a2a`.

## 2026-10-20 (site images on R2)

### Added
- **Photo registry `photos.json`**, keyed by photo id (for example `culture/puan-tedim`). Each entry gives the file, alt text, caption, credit, source key, width and height.
- **`{{photo:<id>}}` placeholders** render as a `<figure>` with the image served from `https://assets.khual.net/tangthu/img/`. The figcaption's source goes through the normal citation pipeline, so it appears as a numbered note and in that page's source list. The base URL is `CDN_BASE` in `build.py`, overridable with `TANGTHU_CDN`.
- **`scripts/upload_images.sh`** converts `images/` to WebP (at most 1600 px wide, via `cwebp` or Pillow) and uploads to R2 bucket `kws-assets` under `tangthu/img/`. It never overwrites: a changed original is published as `-v2`, `-v3`, and a name already in the bucket is treated the same way. Published files are recorded in `images/.uploaded`.
- **`images/README.md`** documents the naming rules and folder layout.
- A `<link rel="preconnect">` to `assets.khual.net` on every page. The site sends no Content-Security-Policy, so nothing needed changing there.

### Changed
- The build stops with a list of errors, and writes nothing to `dist/`, if a `{{photo:…}}` id is missing from `photos.json`, a published photo has no `alt` or `source`, or a `source` is not a key in `sources.json`.
- Nine photos still wanted in the chapters (`colonial`, `origins`, `modern`, `diaspora`, `culture` ×2, `stories`, `faith`, `evidence`) moved from free-text placeholders to ids, marked `"status": "wanted"`. They render exactly as before, so their page dates are unchanged.
- `images/` is git-ignored, except its README.

## 2026-10-20 (puan palette)

### Changed
- **Site colours and weave stripe** now follow the green-red-white puan in Khual's photo: white ground, thin gold edge lines, broad green bands and a red centre split by a white line. Replaces the earlier maroon Zopuan palette. Source: photo supplied by Khual (no written source).

## 2026-10-20 (essay origin claims)

### Added
- **Stories page, "The essay's wider origin story":** every remaining claim from Mang Ngaih Cin's essay, stated as written, including the Zhou "Zo dynasty", the flight from the Qin, five explanations of "Chin", the central-Burma word origins, the AD 800 valley date and the Ciimnuai/Lailun split. Labelled contested, each marked "not enough evidence" where that applies.

## 2026-10-20 (mobile search icon)

### Added
- **Search icon on mobile and tablet:** a magnifier button to the left of the Menu button (screens up to 1100px) opens the search page. It has a 44px tap target and a screen-reader label. On desktop the "Search" menu word is now the same icon.

## 2026-10-20 (naming traditions)

### Added
- **Stories page, "How the Tedim-area groups got their names":** traditions for Zo, Teizang, Saizang, Sihzang, Vangteh, Diim and Khuano, plus the essay's account of how Tedim speech formed. Labelled oral tradition, with a warning box marking them as speculation.
- **Source:** Mang Ngaih Cin, “Zo Khang Tangthu” (Academia.edu). Its Zhou-dynasty and Qin claims are not used.

## 2026-10-20 (site search)

### Added
- **Search page (`/search`):** searches every section of every chapter, the glossary, all timeline events and every source, with results that highlight the matched words, link straight to the section, and show its evidence label. Filter by Pages, Glossary, Timeline or Sources.
- **Zolai-friendly matching:** ignores apostrophes and accents, treats doubled vowels as single (so "Cimnuai" finds Ciimnuai), and matches joined or split names ("kamhau" finds Kam Hau).
- **"Search" in the main menu** at every screen size; press `/` on any page to jump to search. Searches are shareable as links (`/search?q=…`).
- **Accessible:** labelled form, result count announced to screen readers, filter buttons report their state, Enter moves to the first result, and a message for readers without JavaScript.
- **Build:** `build.py` now writes `assets/search-index.json`; the 404 page and site map link to search.

### Fixed
- **Search layout:** the Clear button is visible in dark mode, and the header search box was replaced by a "Search" menu item so the menu fits on one line.
- **Updates reach readers immediately:** stylesheet and scripts are now loaded with a version stamp (`?v=…`) that changes whenever the file changes, so the 24-hour asset cache no longer serves an old design after an update.

## 2026-10-19 (mobile and accessibility)

### Changed
- **Focus outline:** keyboard focus is now a dark ink outline in light mode (the gold one was too faint, 1.8:1); gold is kept in dark mode and on dark panels.
- **Controls:** filter buttons, section-menu pills, copy buttons and the menu button have clearer borders, and tap targets are at least 44px (footnote numbers, footer links, copy buttons, section pills).
- **Phones (under 640px):** tighter side margins (16px), slightly smaller body text, single-column chapter links, wrapping evidence labels, and long URLs or words wrap instead of causing sideways scrolling.
- **Mobile menu:** closes with Escape, when a link is chosen, or when tapping outside; moves focus into the menu when opened; scrolls if taller than the screen; and stays visible as a plain list if JavaScript is off.
- **Timeline:** filter buttons report their pressed state and are grouped with labels; screen readers hear how many events are shown after filtering; each event's button is linked to its details.
- **Evidence tables:** can be scrolled sideways with the keyboard and are labelled for screen readers.
- **Map:** keyboard navigation enabled.
- **Tap targets:** the site name, footnote numbers and source links are now larger to tap.
- **Motion and contrast:** smooth scrolling is turned off for readers who ask for reduced motion; labels and buttons keep visible edges in Windows high-contrast mode.

## 2026-10-19 (LTTuang Scribd archive)

Ten Zolai documents uploaded to Scribd by L. T. Tuang were read and decoded from an old non-Unicode font; every claim added below was checked against the decoded text, and doubtful words were confirmed with Khual.

### Added
- **Names & Identity, "Beh and phung":** what a *beh* is, and Thang Lian Pau's 2002 list of about 200 beh and 12 phung, with a note that the list mixes tribe and area names.
- **Origins, "Six theories in a Zomi newsletter":** the 1983 *Workers' New Letter* review of six origin theories (via Zomi Messenger) and Khen Za Sian's Zhou/Qin argument, labelled contested.
- **Stories:** the Khan Thuam plot of 1783, the nine chiefs, refuge at Rallang, and the two lists of his sons; a new story on Kam Hau, the founding of Tedim (c. 1804 and 1810), its five *veng*, the eight-member council and the *Kamhau Upadi* (from 1848; printed 1972, and per Nang also 1925); and the Kamhau chief line 1820–1948.
- **Culture, textiles:** seven weaving motifs (*pheleu*), dye plants, traditional garments, and the 1966 Zomi National Dress Committee.
- **Faith & Literacy:** first Tedim-area baptisms (4 April 1904), Zomi Baptist baptism figures 1915–1980, Cope's Matthew (1915), and the 1931 Census and Bible Society references to the Pau Cin Hau script.
- **Modern:** new "Second World War" section (1942 road via Tonzang, 1943 Chin Levy, the Chin Defence Army and Bo Mang Za Thang); Thang Za Tuan's account of the 1946 and 1947 Panglong conferences.
- **Sources:** thangliampau2002, thangliampau2010, zomimsg-piancil, khenzasian, zomimsg-khanthuam, zomimsg-kamhau, thangzatuan-pzm, khupzago1980, zomimsg-puan, cda-mzt.

### Flagged (not resolved)
- Khan Thuam's death: 1848 (site), 1840 (Nang); Kam Hau's rule from 1820 (Thang Lian Pau).
- Khan Thuam's sons: five or seven.
- Pau Cin Hau alphabet: 37 letters (Khup Za Go) vs 57 (Unicode proposal).
- Chin delegation's 1947 Panglong arrival: 6 February (published documents) vs 2 February (Thang Za Tuan).

### Changed
- **Page dates:** Names, Origins, Stories, Culture, Faith and Modern updated to 2026-10-19.

## 2026-10-19 (proverbs and new sources)

### Added
- **Culture page, "Paunak: Zomi proverbs":** 13 proverbs in Zolai with English translations and meanings, labelled as oral tradition. Zolai wording follows a community collection; translations are the site's own and still need checking by a native speaker.
- **Sources:** Thang Thawn Tuang Guite, “Zomite Paunak” (Zogam History blog, 2023); Gin Khan Nang, “Zomi Life and Culture” (Fuller Theological Seminary paper, 2007, via Zomi Daily).
- **Styles:** layout for the proverb list.

### Changed
- **Culture page, "The hornbill":** the hornbill-couple emblem is now also cited to Gin Khan Nang (2007), so it no longer rests on the 2011 blog alone; the source note is updated to match.
- **Page dates:** Culture page `updated` remains 2026-10-19 (already today's date).

## 2026-10-19 (dates and citations)

### Added
- **Page dates:** every chapter shows when it was published and last updated (kept in `page-dates.json`; update a page's date whenever its content changes).
- **Cite this page:** ready-made APA 7, MLA 9 and Chicago citations with the page's update date and URL, a copy button for each, and the reader's access date filled in automatically.
- **Search data:** published and modified dates in the page metadata and sitemap now come from `page-dates.json`.

## 2026-10-19 (hornbill)

### Added
- **Culture page, "The hornbill":** its place in Zomi tradition as a noble bird and a symbol of faithful marriage, hornbill feathers as a mark of honour, and the hornbill as a Zomi emblem. Labelled as oral tradition, with a note that the underlying book is not yet verified.
- **Sources:** “The Hornbill Emblem” (Chin People in the World, 2011); Progressive Voice (2021).

## 2026-10-19 (colours)

### Changed
- **Site colours now match the Zopuan:** text ink is navy-black, links and the documented-history label use Zopuan green, the red accent is Zopuan maroon, and the gold accent matches the cloth's gold thread. Dark mode uses lighter versions of the same colours.

## 2026-10-19 (refined)

### Changed
- **Zopuan stripe refined from four more photos** (women's skirts and shawls, men's shirts): the ground is now a deep maroon with fine dark pinstripes rather than bright red, white lines frame a green, red and gold centre band, and the edge is navy-black like a skirt hem. Gold is reduced to a thin accent.

## 2026-10-19 (later)

### Changed
- **Site stripe now follows the Zopuan:** a red ground edged in green, with thin gold, black and white lines, replacing the earlier Tedim-based red/black band. Colours were sampled from a photograph of Zopuan trim and are approximate.

## 2026-10-19

### Fixed
- **Puan colours:** the woven band, page edge and footer stripe used a green-heavy palette with gold, which does not match the Tedim cloth. They now use a red and black ground with thin white and green lines, following the sources on the Culture page.

### Added
- **Culture page, "What a puan looks like":** the most common colours, the size and two-panel construction, the shift from undyed to natural to synthetic dyes, and the red-centred *puon laisen*, all cited.
- **Culture page:** the materials (cotton and silk) and occasions (harvest festival, traditional dances) for the Tedim cloth.
- **Source:** MAP Academy, “Mizo Puan.”
