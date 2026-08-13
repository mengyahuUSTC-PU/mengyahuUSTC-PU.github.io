import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://mengyahu.com',
  integrations: [sitemap()],
  trailingSlash: 'ignore',
});
