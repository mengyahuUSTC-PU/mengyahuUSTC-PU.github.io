export type Lang = 'zh' | 'en';

export const SITE_TITLE = 'Mengya (Mia) Hu';
export const SITE_URL = 'https://mengyahuustc-pu.github.io';

export const ui = {
  en: {
    'nav.home': 'Home',
    'nav.writing': 'Writing',
    'nav.about': 'About',
    'nav.projects': 'Projects',
    'home.tagline': 'Notes on Responsible AI — safety, evaluation, and governance from an engineering point of view.',
    'home.latest': 'Latest writing',
    'home.readMore': 'Read more',
    'article.translation': '中文版',
    'article.readIn': 'Read this post in Chinese',
    'list.title': 'Writing',
    'list.empty': 'No posts yet.',
    'footer.rss': 'RSS',
    'about.title': 'About',
    'projects.title': 'Projects',
  },
  zh: {
    'nav.home': '首页',
    'nav.writing': '文章',
    'nav.about': '关于',
    'nav.projects': '项目',
    'home.tagline': '负责任 AI 笔记——从工程视角看安全、评测与治理。',
    'home.latest': '最新文章',
    'home.readMore': '阅读全文',
    'article.translation': 'English version',
    'article.readIn': '阅读本文英文版',
    'list.title': '文章',
    'list.empty': '暂无文章。',
    'footer.rss': 'RSS 订阅',
    'about.title': '关于',
    'projects.title': '项目',
  },
} as const;

export function t(lang: Lang, key: keyof (typeof ui)['en']): string {
  return ui[lang][key];
}

export function langHome(lang: Lang): string {
  return `/${lang}/`;
}

export function postUrl(lang: Lang, slug: string): string {
  return `/${lang}/${slug}/`;
}
