import type { APIRoute } from 'astro';
import { getCollection, type CollectionEntry } from 'astro:content';
import { articleCard, png } from '../../../lib/og';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({ params: { lang: post.data.lang, slug: post.data.slug }, props: { post } }));
}

export const GET: APIRoute = async ({ props }) =>
  png(await articleCard((props as { post: CollectionEntry<'blog'> }).post));
