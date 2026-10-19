# Zogam History: Research Notes & Project Record
*Last updated 19 Oct 2026 (third pass: textiles, Zopuan colours, hornbill)*

## Project
- **What it is:** an educational, evidence-based, neutral history website covering the Zo, Zomi and Zou peoples (Chin Hills, Manipur, Mizoram, Chittagong Hill Tracts). Audience: community members, diaspora youth and general readers.
- **Build:** static site. Build command `python3 build.py`, output directory `dist/`.
- **Source files:** `content/*.html` holds the page bodies; `sources.json` is the single bibliography (82 entries); `assets/data.js` holds the timeline and map data.
- **Markup conventions:**
  - Citations: `[[key]]`.
  - Evidence labels: `{{oral}}` `{{doc}}` `{{sch}}` `{{contested}}`.
  - Placeholders: `{{photo:…}}` and `{{oralhistory:…}}`.
- **Pages:** Home, Origins, How We Know, Stories, Names & Identity, Colonial, Faith & Literacy, Modern, Culture, Diaspora, Sources, Contribute.
- **Design mockup:** Claude Design canvas "Zogam History — Mockup" (artboards: home desktop, How We Know desktop, home mobile).
  - Look: archival editorial. Fonts are Fraunces (headings), Source Serif 4 (body) and IBM Plex Mono (labels).
  - Palette: paper #EFE6D6, ink #1F1A14, clay #8E3B1F, forest #3E5537. A striped band based on woven *puan* cloth separates sections.
  - Not yet applied to the live site's CSS.
- **Open to-dos:**
  - Add a contact form or email to the Contribute page.
  - Verify the unconfirmed sources (listed at the end).
  - Find figures for the Europe diaspora.
  - Collect weavers' own names and meanings for textile patterns.
  - Confirm the map loads after deploy.

## Editorial rules
- Every claim is cited.
- Oral tradition, documented history and scholarly interpretation are labelled separately.
- No side is taken between communities on names, borders or the Manipur conflict.
- Colonial and missionary sources are flagged as perspectival.

## Key findings by topic

### Origins
- **Origin traditions:** Khul (Kuki), Chhinlung/Sinlung (Mizo/Chin, Hmar) and Ciimnuai (Chin). These were first written down by Shaw, Shakespeare, and Carey & Tuck (Haokip & Milli 2026).
- **Migration sequence:** Shan region → Kabaw Valley → Khampat → Chin Hills.
  - Chin tradition dates the valley settlement to about AD 700–800 and the move into the hills to the late 1300s (Chan Khar).
  - These dates come from traditional reckoning, not archaeology.
- **Khampat:** the banyan-tree (*bungpui*) tradition remembers the departure from Khampat under Shan pressure, c. 1370–1400. Gougin-tradition writers describe a Zo realm reaching Khampat in the 13th–15th centuries (Khalvontawi 2024).
- **Lehman's view:** a series of regional movements driven by Shan expansion and by Burmese and Manipuri warfare, not one single migration.
- **Ciimnuai (near Tedim) and Lailun (near Falam):** settlements dated to the 1400s by genealogy. Clans dispersed from them (Vumson 1986; Sing Khaw Khai 1995).

### Evidence (How We Know)
- **Early external records:**
  - *Man Shu*, c. 862 (Fan Ch'o): "Zo/Jo". This is Vumson's identification, building on Luce's reading. Treat it as an attributed interpretation, not proof.
  - 12th-century Burmese inscriptions mention Khyan/Chin near the middle Chindwin (per Lehman).
  - Rawlins (1790s): "Cucis" (Kuki).
  - Carey & Tuck (1896): "they call themselves Yo".
  - Grierson (1904): the Kuki-Chin language group.
- **Indigenous record-keeping:** clan genealogies (15–25 generations), metered songs (*la*), memorial stones (*mualsuang*) and customary law.
- **Supported:** related languages; real collective memory; varied pre-colonial polities.
- **Not supported:** a single ancient kingdom; a known origin site.

### Names
- **Zomi and Mizo:** both mean "Zo people".
- **Zomi as an organisational name:**
  - The name was proposed at a Baptist meeting in Rangoon in 1950 and adopted by the Zomi Baptist Convention at Saikah in 1953 (Thangsuanhau & Jamkhanpau, unverified).
  - A formal proclamation of the name is dated 6 December 1988 (Go 2008).
- **Chin:** comes from Burmese *Khyan*. Its etymology is debated: "basket" (Lehman) or a Chinese word for "man" (via Grierson). Hau Go calls it foreign and derogatory, but many communities embrace it.
- **Lushai and Mizo:** "Lushai" first appears in the Cachar reports around 1850; "Mizo" was formally adopted around 1946.
- **Zou:** a distinct tribe. Do not conflate with the umbrella term "Zo".

### Colonial era
- **Annexation:** Chin-Lushai Expedition 1889–90, followed by resistance from 1890 to 1896.
- **Chin-Lushai Conference, Fort William, 1892:** the plan to unite the hills under one administration failed.
- **Chin Hills Regulation, 1896:** indirect rule through the chiefs.
- **Anglo-Kuki War / Zou Gal, 1917–19:**
  - Triggered by recruitment for the Labour Corps; covered more than 6,000 square miles.
  - Hiangtam, under chief Goulun, was a Zou headquarters.
  - Leather hand-cannons (*pumpi*) from the war are held at the Pitt Rivers Museum, Oxford.

### Faith and literacy
- **Missions:**
  - The Carsons arrived in Hakha on 15 March 1899.
  - The Chin Hills Baptist Association formed in 1907.
  - Cope served in Tedim for about 30 years.
  - Missionaries who arrived after 1947 were expelled in 1966.
- **Tedim scriptures:** New Testament 1932; full Bible 1983 (other sources give 1977).
- **Pau Cin Hau (1859–1948):** founder of the Laipian movement.
  - Logographic script of about 1,050 characters (1902).
  - Alphabet of 57 characters (final revision 1931), added to Unicode 7.0 in 2014 at U+11AC0–11AFF.

### Modern history
- **Panglong, 12 February 1947:** the Chin signatories were Hlur Hmung, Thawng Za Khup and Kio Mang.
- **Chin National Day, 20 February 1948:** an assembly voted to end hereditary chieftainship. It was designated Chin National Day in 1950 and banned in 1994.
- **Armed groups:** Chin Independence Army 1961; Chin National Front 1985; Mizo National Front rising 1966; Chin National Army 1988.
- **T. Gougin (1925/26–2012):**
  - First organisation: either a United Zomi Organisation (1961) or a United Manipur Zou Organisation (1959). The sources conflict.
  - Founded the Zomi National Congress at Daijang on 28 January 1972.
- **Reunification organisations:** ZORO founded at Champhai on 20 May 1988 (non-violent); ZRO/ZRA formed at Phapian in 1993.
- **Displacement after the 2021 coup:**
  - 9,247 people had reached Mizoram by June 2021.
  - UN OCHA (2022): 46,200 internally displaced within Chin State and 47,200 refugees from Chin State in India.
  - Later Mizoram counts are around 29,000–33,000.
- **Manipur, from 3 May 2023:** government figures give 258 killed and 60,000 displaced (Nov 2024). The site reports figures only, neutrally.

### Culture and diaspora
- **Khuado:** harvest and New Year festival, celebrated in October.
- **Older festivals:** Mim Kut and others; traditional instruments include phit, tamngai and others (Thangtungnung).
- **Indianapolis:** about 20,000 Burmese refugees, roughly 75% Chin. The Chin Community of Indiana was founded in 2001 and reports more than 30,000 members (2024).
- **Malaysia:** the Zomi Education Centre in Taman Cheras, Kuala Lumpur, publishes introductions to Zomi history. Its population estimates are undated.

## Stories (added 19 Oct 2026)
- **Ciimnuai:** about 2.5 miles southwest of Tedim, near Saizang; Carey & Tuck called it the "Eden of the Chins".
  - The Guite chronicle (Ngul Lian Zam 2018) names Guimang I (c. 1050) and Mangsuum I (c. 1250), and says Geeltui, Kalzang and Tedim were founded from Ciimnuai.
  - Thadou tradition credits Song Thu with a migration around 1500.
- **Khampat bungpui (banyan):** in 2016 India asked Myanmar to help protect the tree (The Wire, 20 Oct 2016), after campaigning by a preservation committee and ZORO.
- **Khan Thuam (died 1848):** Sukte chief raised at Mualbem. The midnight rope-ferry escape is oral tradition (S. Khup Pau 2011, via Wikipedia). His son Kam Hau gave his name to the Kamhau chiefdom.
- **Khai Kam (1864–1919):** led Sizang resistance; attacked a British road party on 7 December 1888; Fort White was built in 1889. Surrendered on 16 May 1894 to protect hostages; exiled to the Andaman Islands; released 14 May 1910.
- **Pau Cin Hau:** dreams from 1900; no followers for about three years; first followers around 1906; about 37,500 followers in 1931 and about 5,000 today, centred on Siang Sawn (Aeon, 17 Oct 2024).
- **Mautam famine, 1959:** led to the MNF rising (independence declared 1 March 1966; Aizawl bombed 5 March 1966); Mizo Accord 1986 (Newslaundry 2015).
- **Weaving:** backstrap loom; patterns picked out with a porcupine quill. Tedim stripes are black, green, white and red; the "hen and her chicks" motif (McDougall 2018).
- **Malaysia:** in 2019, about 15,000 of the more than 18,000 Chin registered with UNHCR were in Malaysia; UNHCR dropped its plan to end Chin refugee status (FMT, 14 Mar 2019).
- **Thangsuanhau & Jamkhanpau:** the article appeared in a December 2013 journal issue (web version September 2017).

## Verified links supplied by Khual (19 Oct 2026)
- **Thangsuanhau & Jamkhanpau:** JTICI 1(2), Dec 2013, pp. 51–65 — http://www.ticijournals.org/zomi-diaspora-culture-and-politics/
  - The name "Zomi" was proposed by Sukte T. Haugou (1950); the Zomi Baptist Convention adopted it at Saikah (1953); UZO founded at Singtom (1961); ZRO formed at Phapian (1993).
  - Diaspora: youth exodus to Indian cities from the 1990s; abroad, Myanmar military abuses are named as the main cause.
- **Lehman, "Chin" (Encyclopedia of World Cultures):** 12th-century inscriptions; Shan conquest pushed Chin groups into the hills; Southern Chin had no hereditary chiefs; villages sited as a balance between defence and water.
- **Grierson 1904:** Glottolog record 118757. **Carey & Tuck 1896:** NLA catalogue 1180560.
- **Lalsangpuii 2023 (Senhri 8(1)):** Chhinlung as "a mnemonic of shared ancestry"; upland life as chosen autonomy. Its chronology is internally inconsistent, so it is not relied on.
- **Lalhmingliana 2018 (MZU J. Hum & Soc Sci 4(2)):** Lewin, "generic name ... is Dzo"; "Mizo" popular from the 1940s; Lusei entered Mizoram around 1600–1700 (Rongenga).
- **Thangtungnung (JNEIS 5(1)):** argues the Lost Tribe (Manasseh) theory; the Chief Rabbi recognised the Bnei Menashe in 2005.
- **Chakraborty 2010 (Identity, Culture and Politics 11(2)):** the Zopui banyan near the Tiau valley as a memory symbol; trauma from insurgency-era sexual violence in collective memory.
- **Suan Za Dong 2023 (Chin Archive blog):** argues "Laimi" is a regional name and "Zo" the generic one. A community view only.
- Wikipedia articles: Zo peoples; Zomi people.

## Source audit, 19 Oct 2026
- **Method:** four independent reviewers checked every cited sentence against its source (about 230 citations). A fifth reviewer replaced Wikipedia and opinion citations with stronger ones.
- **Corrections made:**
  - Tedim Bible: 1977 (Bible Society of Myanmar), not 1983. The New Testament date is disputed (1932 or 1935).
  - Ciimnuai: 6.5 miles south-west of Tedim (Carey & Tuck vol. II, "Chinnwe"), not 2.5.
  - Lai Chin as a common school language: Columbus, Ohio, not Indianapolis.
  - ZRA (armed wing) formed in 1997; ZRO in April 1993.
  - CNF: most often dated 1988, sometimes 1985.
  - Political Officers from 1892; Superintendents from 1896.
  - Manipur: 258 dead, including militants (PTI, 22 Nov 2024); more than 50,000 displaced by June 2023 (state government). The 60,000 figure was dropped as unsourced.
  - Mizoram refugee figures: over 33,000 (July 2025) and over 29,000 (August 2025).
  - The Panglong signatory's name is spelled Hlur Mung.
  - Several overstatements softened: "historians call", "most scholarship", the Sinlung city-state, and "strongest evidence".
- **Verified primary source:** Carey & Tuck vol. I (archive.org): "The Northern Chins call themselves Yo, the Tashons, Haka, and more southern tribes Lai, while the Chins of Lower Burma give their name as Shu." The name "Chin" is said to be "a Burmese corruption of the Chinese 'Jin,' or 'Yen,' meaning 'man.'" The Political Officer's headquarters was at Falam.
- **New primary sources:** Chin Hills Regulation 1896 (India Code); Lushai Hills (Change of Name) Act 1954; UNHCR (14 Mar 2019); Unicode 7.0; Pitt Rivers Museum object 1923.85.805 (*pumpi*); ABS 2021 census, which lists Zomi as language code 6105; Lewin 1874 ("Dzo").
- **Catalogue or scan records found:** Vumson (Burma Library 66177); Sing Khaw Khai (Glottolog 556007); Lehman 1963 (D-PLACE); Stevenson (Glottolog 686772); *Man Shu* (Cornell eCommons, open access); Sangermano (Wellcome scan); Rawlins (Asiatick Researches vol. 2, 1790).
- **Still without a strong source:** Lawki (no scholarly source found); ZORO's founding date, 20 vs 19 May 1988; ZNC at Daijang, 1972; Cope's roughly 30 years in Tedim; Khai Kam's release on 14 May 1910; Europe population counts.

## Sources still unverified (from contributed briefs)
- Vumson 1986.
- Sing Khaw Khai 1995.
- Vum Kho Hau 1963.
- Gougin 1984.
- Lehman 1963, the book (the inscription claim is now confirmed via his Encyclopedia of World Cultures entry).
- Stevenson 1943.
- *Man Shu*, translated by Luce.
- Sangermano.
- Rawlins.
- Ngul Lian Zam 2018 and S. Khup Pau 2011 (both cited via Wikipedia).
- Left off the site entirely until checked: the 1508 "Yo" reference via Yule, Buchanan-Hamilton's 1799 wordlists, and the Khuplian stone.

## Source links added 19 Oct 2026
- https://zeccheras.cfsites.org/custom.php?pageid=47430
- https://zeccheras.cfsites.org/custom.php?pageid=47432
- https://zeccheras.cfsites.org/custom.php?pageid=47433
- https://www.khalvontawi.in/2024/06/the-origin-of-zomi-pu-t-gougin.html

## Textiles, Zopuan colours and hornbill (19 Oct 2026, third pass)
- **Puan facts on the Culture page:**
  - Red and black are the most commonly worn colours on Chin cloths. The Tedim cloth is woven of cotton and silk on a mechanised backstrap loom and worn by women for the harvest festival and dances (Maroondah).
  - A puan is about 36 × 44–54 in, woven in two halves and then stitched together. Black, white and red dominate. Early puans were undyed white, then naturally dyed, and synthetic dyes have now largely replaced natural ones (MAP Academy).
  - The Hmar *puon laisen* has a red middle section with two black stripes (IGNCA).
- **Zopuan colours:** no written source found. Colours were taken from five photos Khual supplied (a jacket trim, women's skirts and shawls, men's shirts):
  - Deep maroon ground with fine dark pinstripes.
  - White lines and zigzags.
  - A green, red and gold centre band.
  - A navy-black hem.
  - Small blue, yellow and green motifs.
- **Site palette is now Zopuan:** ink #1B1626, green #2E7A3E, maroon #7A1830, gold #E3A92B, red accent #C8283C, white #EDE6E3. The stripe (`--weave`) is plain stripes only; motifs are not drawn.
- **Hornbill (Culture page, labelled oral tradition):**
  - A noble, sacred bird that eats only fruit; a model of faithful lifelong marriage.
  - Feathers were worn on important occasions; the hornbill is used as a Zomi emblem tying together Zomi in India, Myanmar and Bangladesh.
  - Source: "The Hornbill Emblem" (Chin People in the World, 2011), citing Sing Khaw Khai 1995 p. 194, which is still unverified. The CNF/CNA use a pair of hornbills as their symbol (Progressive Voice 2021).
- **New sources:** mapacademy, sialki2011, progressivevoice2021.
- **Repo:** GitHub Khual-Web-Service/tangthu. Every change is logged in `CHANGELOG.md`.
- **Standing rule from Khual:** always include the source, both on the site and in replies.
