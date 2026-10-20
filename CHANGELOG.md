# Changelog

All notable changes to Zogam History are recorded here.

## 2026-10-20 (essay origin claims)

### Added
- **Stories page, "The essay's wider origin story":** every remaining claim from Mang Ngaih Cin's essay, stated as written, including the Zhou "Zo dynasty", the flight from the Qin, five explanations of "Chin", the central-Burma word origins, the AD 800 valley date and the Ciimnuai/Lailun split. Labelled contested, each marked "not enough evidence" where that applies.

## 2026-10-20 (mobile search icon)

### Added
- **Search icon on mobile and tablet:** a magnifier button at the top left of the header (screens up to 1100px) opens the search page. It has a 44px tap target and a screen-reader label.

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
