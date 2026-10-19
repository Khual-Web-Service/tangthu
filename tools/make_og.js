// Generates 1200x630 social share images into assets/og/.
// Run locally: node tools/make_og.js   (needs Playwright; not part of the site build)
const { chromium } = require('playwright');
const path = require('path');

const PAGES = [
  ['index', '', 'Zomi & Zo History', 'Nine short chapters. Every fact sourced.'],
  ['origins', 'Chapter 1', 'Origins & Migration', 'Khul, Chhinlung and the road through the Kabaw Valley'],
  ['evidence', 'Chapter 2', 'How We Know', 'Songs, memorial stones and old records'],
  ['stories', 'Chapter 3', 'Stories', 'Ciimnuai, Khai Kam, Pau Cin Hau, Mautam'],
  ['names', 'Chapter 4', 'Names & Identity', 'Zo, Zomi, Chin, Kuki, Lai, Mizo, Zou'],
  ['colonial', 'Chapter 5', 'The Colonial Era', 'British rule and the Zou Gal, 1889–1919'],
  ['faith', 'Chapter 6', 'Faith & Literacy', 'Missions, the Tedim Bible and Pau Cin Hau’s script'],
  ['modern', 'Chapter 7', 'Modern History', 'Panglong, Chin National Day and today'],
  ['culture', 'Chapter 8', 'Culture', 'Khuado, puan weaving, language and clans'],
  ['diaspora', 'Chapter 9', 'Diaspora', 'From Indianapolis to Malaysia and Australia'],
  ['timeline', '', 'Timeline', 'From the origin stories to today'],
  ['glossary', '', 'Glossary', 'Puan, Khuado, Zogam and 22 more words, explained'],
  ['sources', '', 'Sources & Standards', 'Where every fact on this site comes from'],
  ['contribute', '', 'Share Your Family’s Story', 'Photos, lineages and elders’ memories'],
];

const weave = 'repeating-linear-gradient(90deg,#171815 0 22px,#2E5B45 22px 46px,#F6F7F2 46px 51px,#A8262D 51px 63px,#F6F7F2 63px 68px,#2E5B45 68px 80px,#171815 80px 101px,#C99A3B 101px 106px)';
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

function card([, kicker, title, sub]) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  *{margin:0;box-sizing:border-box}
  body{width:1200px;height:630px;background:#ECEEE7;color:#171815;font-family:Lora,Georgia,serif;display:grid;grid-template-columns:1fr 300px}
  .l{padding:70px 64px 56px 80px;display:flex;flex-direction:column;justify-content:space-between;border-left:18px solid transparent;border-image:${weave.replace('90deg','180deg')} 18}
  .k{font-size:28px;font-style:italic;color:#66655C;height:34px}
  h1{font-size:${title.length > 18 ? 84 : 104}px;line-height:1.02;font-weight:500;letter-spacing:-2px;max-width:760px}
  .s{font-size:32px;line-height:1.35;color:#3A3C35;max-width:720px;margin-top:22px}
  .b{display:flex;justify-content:space-between;align-items:flex-end;font-size:28px}
  .b strong{font-weight:700}.b em{font-weight:400}
  .u{font-size:24px;color:#2E5B45}
  .r{background:${weave};position:relative}
  .r:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0 4px,rgba(0,0,0,.1) 4px 5px)}
  </style></head><body><div class="l"><div><div class="k">${esc(kicker)}</div><h1>${esc(title)}</h1><p class="s">${esc(sub)}</p></div>
  <div class="b"><span><strong>Zogam</strong> <em>History</em></span><span class="u">tangthu.kws.site</span></div></div><div class="r"></div></body></html>`;
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const pg of PAGES) {
    await p.setContent(card(pg));
    await p.waitForTimeout(100);
    await p.screenshot({ path: path.join(__dirname, '..', 'assets', 'og', pg[0] + '.png') });
  }
  await b.close();
  console.log('made', PAGES.length);
})();
