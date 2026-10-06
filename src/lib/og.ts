// Share cards (1200×630) for every page, rendered at build time.
// LinkedIn, WeChat and Google all read og:image; until 2026-10 the site had
// none, so every shared link showed up without a picture.
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { getCollection, type CollectionEntry } from 'astro:content';
import { SITE_TITLE, t, type Lang } from './i18n';

const W = 1200;
const H = 630;
const LABELS = { zh: { essay: '深度', briefing: 'AI 快讯' }, en: { essay: 'ESSAY', briefing: 'AI BRIEFING' } };

// Google Fonts hands an old browser plain TrueType (satori cannot read
// woff2), and `text=` trims the CJK face from ~10 MB to the glyphs in use.
const OLD_UA =
  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1';

async function fetchFont(family: string, weight: number, text?: string): Promise<ArrayBuffer> {
  const query = `family=${family.replace(/ /g, '+')}:wght@${weight}` + (text ? `&text=${encodeURIComponent(text)}` : '');
  const css = await (await fetch(`https://fonts.googleapis.com/css2?${query}`, { headers: { 'User-Agent': OLD_UA } })).text();
  const url = css.match(/url\((\S+?)\) format\('(?:truetype|opentype)'\)/)?.[1];
  if (!url) throw new Error(`no TrueType source for ${family}`);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`font download for ${family} failed: ${res.status}`);
  return res.arrayBuffer();
}

type Font = { name: string; data: ArrayBuffer; weight: 700; style: 'normal' };
let fonts: Promise<Font[]> | undefined;
// satori keeps one font per family name, so each CJK subset gets its own
// name and the card's font-family lists all of them.
let family = 'Source Serif 4';

/** One download per build: Latin in full, CJK as subsets of every title. */
function loadFonts(): Promise<Font[]> {
  fonts ??= (async () => {
    const posts = await getCollection('blog');
    const text = posts.map((p) => p.data.title).join('') + JSON.stringify(LABELS) + t('zh', 'home.tagline');
    const cjk = [...new Set([...text].filter((ch) => ch.codePointAt(0)! >= 0x2e80))].sort().join('');
    const chunks: string[] = [];
    for (let i = 0; i < cjk.length; i += 300) chunks.push(cjk.slice(i, i + 300));
    const [latin, ...cjkFonts] = await Promise.all([
      fetchFont('Source Serif 4', 700),
      ...chunks.map((chunk) => fetchFont('Noto Serif SC', 700, chunk)),
    ]);
    const named = [latin, ...cjkFonts].map((data, i) => ({
      name: i === 0 ? 'Source Serif 4' : `Noto Serif SC ${i}`, data, weight: 700 as const, style: 'normal' as const,
    }));
    family = named.map((f) => `'${f.name}'`).join(', ');
    return named;
  })();
  return fonts;
}

const el = (style: Record<string, unknown>, children: unknown) => ({ type: 'div', props: { style, children } });

/** Title size by visual length: a CJK character is about two Latin letters wide. */
function titleSize(title: string): number {
  const len = [...title].reduce((n, ch) => n + (ch.codePointAt(0)! >= 0x2e80 ? 1 : 0.5), 0);
  return len <= 16 ? 80 : len <= 26 ? 68 : len <= 38 ? 58 : len <= 52 ? 50 : 44;
}

function card(label: string, title: string, footRight: string, fontFamily: string) {
  return el(
    {
      width: W, height: H, display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
      padding: '64px 76px', color: '#f3ead8', fontFamily,
      backgroundImage: 'linear-gradient(135deg, #33351f 0%, #241c10 100%)',
    },
    [
      el({ display: 'flex', fontSize: 28, color: '#e8965a', letterSpacing: 3 }, label),
      el({ display: 'flex', fontSize: titleSize(title), lineHeight: 1.28 }, title),
      el(
        { display: 'flex', justifyContent: 'space-between', fontSize: 26, color: '#b9b09a',
          borderTop: '2px solid #57503c', paddingTop: 22 },
        [el({ display: 'flex' }, 'mengyahu.com'), el({ display: 'flex' }, footRight)],
      ),
    ],
  );
}

/** Background only: what a card falls back to if the fonts cannot be fetched,
 *  so a Google Fonts outage can never block a deploy. */
function plain(): Uint8Array {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#33351f"/><stop offset="1" stop-color="#241c10"/></linearGradient></defs><rect width="100%" height="100%" fill="url(#g)"/></svg>`;
  return new Resvg(svg).render().asPng();
}

async function render(label: string, title: string, footRight: string): Promise<Uint8Array> {
  try {
    const loaded = await loadFonts();
    const svg = await satori(card(label, title, footRight, family) as never, { width: W, height: H, fonts: loaded });
    return new Resvg(svg, { fitTo: { mode: 'width', value: W } }).render().asPng();
  } catch (err) {
    console.warn(`[og] share card fell back to a plain background: ${err}`);
    return plain();
  }
}

export function articleCard(post: CollectionEntry<'blog'>): Promise<Uint8Array> {
  const lang = post.data.lang as Lang;
  const kind = post.data.tags.includes('briefing') || post.data.slug.startsWith('briefing') ? 'briefing' : 'essay';
  const date = new Intl.DateTimeFormat(lang === 'zh' ? 'zh-CN' : 'en-US', {
    year: 'numeric', month: lang === 'zh' ? 'long' : 'short', day: 'numeric', timeZone: 'UTC',
  }).format(post.data.pubDate);
  // The label already says it is a briefing; the title need not repeat it.
  const title = post.data.title.replace(/^(AI 快讯[：:]\s*|AI briefing:\s*)/i, '');
  return render(LABELS[lang][kind], title, date);
}

export function siteCard(lang: Lang): Promise<Uint8Array> {
  return render(SITE_TITLE, t(lang, 'home.tagline').split(/[。.]/)[0], lang === 'zh' ? '中英双语' : 'English · 中文');
}

export const png = (body: Uint8Array) =>
  new Response(body as BodyInit, { headers: { 'Content-Type': 'image/png' } });
