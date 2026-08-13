import { getCollection } from 'astro:content';

const SITE = 'https://mengyahu.com';

export async function GET() {
  const posts = (await getCollection('blog')).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf(),
  );
  const deep = (lang: string) =>
    posts.filter(
      (p) =>
        p.data.lang === lang &&
        !p.data.tags.includes('briefing') &&
        p.data.slug !== 'hello-world',
    );
  const line = (p: (typeof posts)[number]) =>
    `- [${p.data.title}](${SITE}/${p.data.lang}/${p.data.slug}/): ${p.data.description}`;

  const body = [
    '# Mengya (Mia) Hu — AI Frontier & Safety',
    '',
    '> First-hand essays on AI safety, industry shifts, and building with AI,',
    '> by Mengya Hu (Mia Hu), Senior Applied Scientist working on Responsible AI.',
    '> Every essay is published in English (/en/) and Chinese (/zh/).',
    '> Append `.md` to any article URL for the raw markdown version.',
    '',
    '## Essays (English)',
    ...deep('en').map(line),
    '',
    '## 文章（中文）',
    ...deep('zh').map(line),
    '',
    '## Daily briefings',
    `- English: ${SITE}/en/briefing/`,
    `- 中文: ${SITE}/zh/briefing/`,
    '',
    '## About',
    `- ${SITE}/en/about/`,
  ].join('\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
