import fs from 'node:fs/promises';

const BASE_URL = 'https://yourdomain.com';
const API_URL = 'https://yourdomain.com/api/public/blog-posts';

const staticRoutes = [
  '/',
  '/projects',
  '/blog',
  '/contact',
  '/stats',
];

function urlEntry(path, changefreq = 'monthly', priority = '0.7') {
  return `  <url>
    <loc>${BASE_URL}${path}</loc>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`;
}

async function main() {
  const response = await fetch(API_URL);
  const posts = await response.json();

  const staticEntries = [
    urlEntry('/', 'weekly', '1.0'),
    urlEntry('/projects', 'weekly', '0.9'),
    urlEntry('/blog', 'weekly', '0.9'),
    urlEntry('/contact', 'monthly', '0.7'),
    urlEntry('/stats', 'monthly', '0.5'),
  ];

  const postEntries = posts.map((post) =>
    urlEntry(`/blog/${post.slug}`, 'monthly', '0.8')
  );

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[...staticEntries, ...postEntries].join('\n')}
</urlset>
`;

  await fs.writeFile('apps/web-service/public/sitemap.xml', xml, 'utf8');
  console.log('sitemap.xml generated');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});