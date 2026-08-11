import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { lang: post.data.lang, slug: post.data.slug },
    props: { post },
  }));
}

export async function GET({ props }: { props: { post: any } }) {
  const { post } = props;
  const head = `# ${post.data.title}\n\n> ${post.data.description}\n\n`;
  return new Response(head + (post.body ?? ''), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
}
