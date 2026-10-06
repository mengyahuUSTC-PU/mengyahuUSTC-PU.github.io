import type { APIRoute } from 'astro';
import { siteCard, png } from '../../lib/og';
import type { Lang } from '../../lib/i18n';

export function getStaticPaths() {
  return [{ params: { lang: 'zh' } }, { params: { lang: 'en' } }];
}

export const GET: APIRoute = async ({ params }) => png(await siteCard(params.lang as Lang));
