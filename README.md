<div align="center">

# Zogam History · *Tangthu*

**A free, source-cited history of the Zomi and Zo peoples:**
**Chin · Kuki · Lai · Mizo · Zou**

[![Live site](https://img.shields.io/badge/live-tangthu.kws.site-9a4a2a?style=for-the-badge)](https://tangthu.kws.site)
[![Sources](https://img.shields.io/badge/sources-119-3e5537?style=for-the-badge)](https://tangthu.kws.site/sources)
[![Content: CC BY-SA 4.0](https://img.shields.io/badge/content-CC%20BY--SA%204.0-c58b3a?style=for-the-badge)](LICENSE-CONTENT.md)
[![Code: MIT](https://img.shields.io/badge/code-MIT-1f1a14?style=for-the-badge)](LICENSE)

[**Visit the site**](https://tangthu.kws.site) · [**Contribute**](#-contribute) · [**Sources & standards**](https://tangthu.kws.site/sources)

</div>

---

## About

From the Chin Hills to Manipur, Mizoram and the Chittagong Hill Tracts, the Zo peoples share a history that predates the borders now dividing them. **Zogam History** tells that story for community members, diaspora youth and anyone curious, without taking sides.

**Every fact is footnoted.** Each page lists its sources, labelled by type, and every source was checked against the sentence that cites it.

| | |
|---|---|
| 🟣 **Oral tradition** | Songs, genealogies and family memory |
| 🟢 **Documented** | Contemporary records, archives and official data |
| 🟠 **Scholarly interpretation** | Arguments made by historians |

## What’s inside

| Page | Covers |
|---|---|
| **Origins & Migration** | Khul, Chhinlung, the Kabaw Valley, Ciimnuai |
| **How We Know** | Chronicles, inscriptions, genealogies, songs, memorial stones |
| **Stories** | Ciimnuai, the Khampat banyan, Khan Thuam, Khai Kam, Pau Cin Hau, Mautam |
| **Names & Identity** | Zo, Zomi, Chin, Kuki, Lai, Mizo, Zou: each view, fairly |
| **Colonial Era** | Annexation, the Chin Hills Regulation 1896, the Anglo-Kuki War / Zou Gal |
| **Faith & Literacy** | Missions, the Tedim Bible, the Pau Cin Hau script |
| **Modern History** | Panglong, Chin National Day, reunification, displacement |
| **Culture** | Language, clans, Khuado, music, weaving |
| **Diaspora** | Indianapolis, Malaysia, Australia, Europe |

It also includes an interactive timeline, a regional map, a site map, and spaces reserved for community photos and oral histories.

## 🤝 Contribute

**Email [tangthu@khual.net](mailto:tangthu@khual.net)** with corrections, sources, photos or oral histories. No GitHub account is needed.

> Ask an elder three questions: *What village? What clan? What song?* Then send us the answers.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for what to include and how we handle consent.

## Run it locally

```bash
python3 build.py              # builds the site into dist/
python3 -m http.server -d dist
```

No dependencies: just Python 3.8+. Citations are written `[[key]]` in `content/*.html` and resolved from `sources.json`. The build fails if a citation key is missing.


## Licence

- **Written content:** [CC BY-SA 4.0](LICENSE-CONTENT.md). Share and adapt freely, with credit and under the same licence.
- **Code:** [MIT](LICENSE).
- Quotations stay with their authors; community photos and oral histories stay with their contributors.

<div align="center">

Made with care by **[Khual Web Service](https://khual.net)** · Tulsa, Oklahoma

</div>

## Adding images

- Only images with a verified licence, or public-domain images, go into `images.json`. Check the licence on the source page before you add anything.
- Every image needs its rights record in `images.json` before it is used: author, licence and licence URL, source, date taken, changes, and context.
- No stock photos and no hotlinks. Originals live in `assets/img/originals/`, which is the rights archive and is never published. The site serves only the web versions from `https://assets.khual.net/tangthu/img/`.
- If a photo shows identifiable people, set `people` to `true` and record the consent in `consent`. The build fails without it.
- Use `{{img:key}}` in a page to place an image. The width and height are filled in from the file when you upload.
- Upload with `python3 scripts/upload_images.py --dry-run` first, then without the flag. Uploads never overwrite and never delete. A changed photo gets a new key, such as `kennedy-peak-v2`.
- `python3 build.py` uploads new images and checks they are reachable. Use `python3 build.py --no-upload` for an offline build. The preview server always builds offline.
- Credentials go in `.env` (git-ignored): `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`. Never commit them.
