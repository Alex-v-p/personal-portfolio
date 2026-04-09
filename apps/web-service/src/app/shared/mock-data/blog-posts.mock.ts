import { BlogPostTag } from '../models/blog-post-tag.model';
import { BlogPost } from '../models/blog-post.model';
import { BLOG_TAGS } from './skills.mock';
import { MEDIA_FILES } from './media-files.mock';
import { BlogPostRecord, buildBlogPostViews } from './content.selectors';

export const BLOG_POST_RECORDS: BlogPostRecord[] = [
  {
    id: 'post-building-a-portfolio-shell',
    slug: 'building-a-portfolio-shell',
    title: 'Building a Portfolio Shell That Can Scale Later',
    excerpt:
      'A look at why locking the layout, route structure, and reusable UI early makes the later content and API stages easier to manage.',
    contentMarkdown: `# Start with the shell

When a portfolio starts to grow, the first page is almost never the hard part. The real challenge is whether the structure underneath can absorb more content **without forcing a redesign** every few weeks.

## Why stage the work

Breaking the project into layout, mock data, pages, API, database, and admin phases makes each decision smaller and more deliberate.

- It keeps the front end moving while the backend is still undefined.
- It makes design issues visible before real data arrives.
- It reduces the temptation to solve everything at once.

## What the shell needs to do

The shell should give every page the same foundation:

1. stable navigation
2. a predictable page container
3. consistent spacing
4. footer and utility actions

> A good shell turns future work into a content problem instead of a redesign problem.

## The practical payoff

Once the shell is stable, later stages become much safer. You can focus on projects, blog posts, stats, and API responses without having to rewrite the outer frame each time.

### Small structure, big leverage

Even simple reusable pieces such as cards, chips, buttons, and section headers create a lot of leverage. They make the portfolio feel coherent early and keep later polish cheap.
`,
    coverImageFileId: 'file-blog-shell-cover',
    coverImageAlt: 'Portfolio shell layout illustration',
    readingTimeMinutes: 5,
    status: 'published',
    isFeatured: true,
    publishedAt: 'July 29, 2025',
    seoTitle: 'Building a scalable portfolio shell',
    seoDescription: 'Why a strong shell makes later portfolio stages easier.',
    category: 'Frontend'
  },
  {
    id: 'post-mock-data-first',
    slug: 'mock-data-first',
    title: 'Why I Prefer Mock Data Before Real Endpoints',
    excerpt:
      'Using realistic mock objects first helps shape pages, models, and edge cases before the backend becomes a dependency.',
    contentMarkdown: `# Model the content before the API exists

Mock data turns vague placeholders into actual content shapes. It forces you to decide what a project, a blog post, or a stat card **really needs to contain**.

## What good mock data gives you

It helps answer questions early:

- Which fields are required for the page to feel complete?
- Which values are only display helpers?
- Which repeated shapes deserve reusable components?

## What to avoid

Mock data should not stay random lorem ipsum forever. The closer it gets to your real portfolio content, the less rewrite you create for yourself later.

### A useful rule

Keep the mock data close to your future schema. That way the page can switch from local files to an API response with minimal changes.


the main content can still be authored as markdown in the database and rendered cleanly on the front end.
`,
    coverImageFileId: 'file-blog-mock-data-cover',
    coverImageAlt: 'Mock data objects represented as cards',
    readingTimeMinutes: 4,
    status: 'published',
    isFeatured: true,
    publishedAt: 'August 10, 2025',
    seoTitle: 'Mock data before real endpoints',
    seoDescription: 'Why realistic mock data sharpens front-end and API work.',
    category: 'Workflow'
  },
  {
    id: 'post-student-projects-and-storytelling',
    slug: 'student-projects-and-storytelling',
    title: 'Turning Student Projects Into Clear Portfolio Stories',
    excerpt:
      'A practical way to present school and personal work so each project communicates context, responsibility, and outcome.',
    contentMarkdown: `# Lead with context

A project list is not the same as a portfolio. Readers need to understand **what the project was**, **why it mattered**, and **what your role was**.

## Explain the setting

Start with the context:

- Was it a school assignment?
- A client exercise?
- A personal build?
- A team project with a defined role?

## Show responsibility clearly

Even a short line about what you owned makes a project much more useful to readers. It helps them understand your contribution without making them guess.

## End with outcome

The strongest portfolio stories usually end with one of these:

1. what shipped
2. what improved
3. what you learned

That is what turns a coursework item into a convincing portfolio piece.
`,
    coverImageFileId: 'file-blog-storytelling-cover',
    coverImageAlt: 'Cards representing project storytelling',
    readingTimeMinutes: 6,
    status: 'published',
    isFeatured: false,
    publishedAt: 'September 02, 2025',
    seoTitle: 'Student projects as portfolio stories',
    seoDescription: 'A practical way to present student work clearly.',
    category: 'Career'
  },
  {
    id: 'post-components-before-polish',
    slug: 'components-before-polish',
    title: 'Components Before Polish',
    excerpt:
      'Reusable UI pieces are not the glamorous part of a build, but they make the later polish stage much faster and safer.',
    contentMarkdown: `# Start with the repeated pieces

The temptation is always to jump straight into beautiful one-off screens. I prefer to stabilise the repeated UI first.

## Components reduce friction

A reusable button, chip, card, or section title does more than save time. It also keeps the design language consistent while the product is still changing.

## What deserves a component first

- anything that appears on multiple pages
- anything with repeated spacing and typography
- anything that is likely to gain variants later

## Polish lands better later

Once the repeated pieces are stable, polish becomes easier. You stop fighting duplicated markup and start refining the system instead.


a small component layer is usually more valuable than an early animation pass.
`,
    coverImageFileId: 'file-blog-components-cover',
    coverImageAlt: 'UI components arranged in a grid',
    readingTimeMinutes: 3,
    status: 'published',
    isFeatured: false,
    publishedAt: 'September 21, 2025',
    seoTitle: 'Components before polish',
    seoDescription: 'Why reusable UI pieces are worth stabilising early.',
    category: 'Frontend'
  }
];

export const BLOG_POST_TAGS: BlogPostTag[] = [
  { postId: 'post-building-a-portfolio-shell', tagId: 'tag-angular' },
  { postId: 'post-building-a-portfolio-shell', tagId: 'tag-architecture' },
  { postId: 'post-building-a-portfolio-shell', tagId: 'tag-ui' },
  { postId: 'post-mock-data-first', tagId: 'tag-mock-data' },
  { postId: 'post-mock-data-first', tagId: 'tag-planning' },
  { postId: 'post-mock-data-first', tagId: 'tag-typescript' },
  { postId: 'post-student-projects-and-storytelling', tagId: 'tag-career' },
  { postId: 'post-student-projects-and-storytelling', tagId: 'tag-projects' },
  { postId: 'post-student-projects-and-storytelling', tagId: 'tag-writing' },
  { postId: 'post-components-before-polish', tagId: 'tag-components' },
  { postId: 'post-components-before-polish', tagId: 'tag-tailwind' },
  { postId: 'post-components-before-polish', tagId: 'tag-design-systems' }
];

export const BLOG_POSTS: BlogPost[] = buildBlogPostViews(BLOG_POST_RECORDS, MEDIA_FILES, BLOG_TAGS, BLOG_POST_TAGS);
export const FEATURED_BLOG_POSTS = BLOG_POSTS.filter((post) => post.isFeatured);
