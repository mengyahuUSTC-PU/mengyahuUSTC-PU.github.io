import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { readdirSync, readFileSync } from 'node:fs';

// lastmod for every article, from its frontmatter: tells crawlers which URLs
// are new. Google was leaving fresh articles undiscovered for weeks.
const lastmod = {};
for (const lang of ['zh', 'en']) {
  for (const file of readdirSync(`./src/content/blog/${lang}`)) {
    if (!file.endsWith('.md')) continue;
    const fm = readFileSync(`./src/content/blog/${lang}/${file}`, 'utf8').split('---')[1] ?? '';
    const slug = fm.match(/^slug:\s*["']?([^"'\n]+)/m)?.[1]?.trim();
    const date = fm.match(/^pubDate:\s*["']?(\d{4}-\d{2}-\d{2})/m)?.[1];
    if (slug && date) lastmod[`https://mengyahu.com/${lang}/${slug}/`] = date;
  }
}

export default defineConfig({
  site: 'https://mengyahu.com',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/og/'),
      serialize(item) {
        const date = lastmod[item.url];
        if (date) item.lastmod = new Date(`${date}T12:00:00Z`).toISOString();
        return item;
      },
    }),
  ],
  trailingSlash: 'ignore',
});
