import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://mengyahuustc-pu.github.io',
  integrations: [sitemap()],
  trailingSlash: 'ignore',
});
