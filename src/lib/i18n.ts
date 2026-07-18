export type Lang = 'zh' | 'en';

export const SITE_TITLE = 'Mengya (Mia) Hu';
export const SITE_URL = 'https://mengyahuustc-pu.github.io';

export const ui = {
  en: {
    'nav.home': 'Home',
    'nav.writing': 'Writing',
    'nav.about': 'About',
    'nav.projects': 'Projects',
    'home.tagline': 'First-hand notes on AI safety, industry shifts, and building with AI. Every post bilingual; opinions are my own.',
    'home.latest': 'Latest writing',
    'home.deepDives': 'Deep dives',
    'home.briefings': 'Daily briefing',
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
    'home.tagline': 'AI 安全、行业趋势与工程实践的第一手笔记。每篇中英双语，观点全属个人。',
    'home.latest': '最新文章',
    'home.deepDives': '深度文章',
    'home.briefings': '每日快讯',
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
