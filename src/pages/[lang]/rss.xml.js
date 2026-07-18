import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE_TITLE } from '../../lib/i18n';

export function getStaticPaths() {
  return [{ params: { lang: 'zh' } }, { params: { lang: 'en' } }];
}

export async function GET(context) {
  const lang = context.params.lang;
  const posts = (await getCollection('blog', (p) => p.data.lang === lang)).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );
  return rss({
    title: lang === 'zh' ? `${SITE_TITLE}（中文）` : `${SITE_TITLE} (English)`,
    description:
      lang === 'zh'
        ? '负责任 AI 笔记——从工程视角看安全、评测与治理。'
        : 'Notes on Responsible AI — safety, evaluation, and governance from an engineering point of view.',
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/${lang}/${post.data.slug}/`,
    })),
    customData: `<language>${lang === 'zh' ? 'zh-CN' : 'en'}</language>`,
  });
}
