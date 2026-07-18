import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  // generateId: keep ids path-based (e.g. "zh/hello-world") — otherwise the
  // glob loader uses the frontmatter `slug` as id, and zh/en pairs that share
  // a slug would collide and silently drop one entry.
  loader: glob({
    pattern: '**/*.md',
    base: './src/content/blog',
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    lang: z.enum(['zh', 'en']),
    slug: z.string(),
    translationOf: z.string().optional(),
  }),
});

export const collections = { blog };
