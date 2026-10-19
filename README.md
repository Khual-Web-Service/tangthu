# Zogam History: static site

An educational, source-cited history of the Zo, Zomi and Zou peoples.

## Structure
- `content/*.html`: page bodies. Use `[[sourcekey]]` for citations, `{{oral}}` `{{doc}}` `{{sch}}` `{{contested}}` for evidence labels, and `{{photo:...}}` / `{{oralhistory:...}}` for community placeholders.
- `sources.json`: the single bibliography. The build fails if a page cites a key that isn't listed here.
- `assets/data.js`: timeline events, map places and map regions.
- `build.py`: generates `dist/` (no dependencies; Python 3.8+).

## Deploy on Cloudflare Pages
**Option A: Git (recommended)**
1. Push this folder to a GitHub repo.
2. In Cloudflare, open Workers & Pages → Create → Pages → Connect to Git and choose the repo.
3. Set the build command to `python3 build.py` and the build output directory to `dist`.
4. Deploy. Every push then rebuilds the site.

**Option B: Direct upload**
Run `python3 build.py`, then drag the `dist/` folder into Pages → Create → Upload assets. Alternatively, run `npx wrangler pages deploy dist --project-name zogam-history`.

## Adding content
Add a source to `sources.json`, cite it with `[[key]]`, and rebuild. Mark anything that comes from oral tradition with `{{oral}}`.

## Domain & SEO (tangthu.kws.site)
- The site address is set in `build.py` (`SITE_URL`, default `https://tangthu.kws.site`). It can be overridden with the `SITE_URL` environment variable.
- Each build generates `sitemap.xml`, `robots.txt`, an HTML `/sitemap` page, canonical URLs, Open Graph/Twitter cards (`assets/og.png`), and JSON-LD structured data (WebSite, Article, BreadcrumbList, and FAQPage on the home page).
- **Connect the domain:** in Cloudflare, open the Pages project → Custom domains → add `tangthu.kws.site`. If kws.site's DNS is on Cloudflare, the CNAME record is created automatically.
- **After the first deploy:**
  1. Add `https://tangthu.kws.site` as a property in Google Search Console and verify it with a DNS TXT record on kws.site.
  2. Submit `https://tangthu.kws.site/sitemap.xml`.
  3. Use URL Inspection on the home page and request indexing.
  4. Do the same in Bing Webmaster Tools; you can import the site from Google Search Console.
