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
    contentMarkdown: '## Why stage the work\nBreaking the work into layers keeps the portfolio maintainable.',
    coverImageFileId: 'file-blog-shell-cover',
    coverImageAlt: 'Portfolio shell layout illustration',
    readingTimeMinutes: 5,
    status: 'published',
    isFeatured: true,
    publishedAt: 'July 29, 2025',
    seoTitle: 'Building a scalable portfolio shell',
    seoDescription: 'Why a strong shell makes later portfolio stages easier.',
    category: 'Frontend',
    intro: [
      'When a portfolio starts to grow, the problem is rarely the first page. The problem is whether the structure underneath can support more content without forcing you to redesign everything again.',
      'That is why I prefer to lock the shell, shared UI, and page regions early. It keeps later decisions about content, APIs, and admin features much more manageable.'
    ],
    sections: [
      {
        heading: 'Why stage the work',
        paragraphs: [
          'Breaking the project into layout, mock data, pages, API, database, and admin phases makes each decision smaller and more deliberate.',
          'It also means you can validate the user-facing experience long before the backend is finished.'
        ]
      },
      {
        heading: 'What the shell needs to do',
        paragraphs: [
          'The shell needs consistent navigation, a stable page container, a footer, and a layout that future sticky and hide-on-scroll behavior can attach to later.',
          'Once that structure is in place, the rest of the portfolio becomes a content problem instead of a redesign problem.'
        ]
      }
    ]
  },
  {
    id: 'post-mock-data-first',
    slug: 'mock-data-first',
    title: 'Why I Prefer Mock Data Before Real Endpoints',
    excerpt:
      'Using realistic mock objects first helps shape pages, models, and edge cases before the backend becomes a dependency.',
    contentMarkdown: '## What good mock data gives you\nIt reveals the right fields before APIs exist.',
    coverImageFileId: 'file-blog-mock-data-cover',
    coverImageAlt: 'Mock data objects represented as cards',
    readingTimeMinutes: 4,
    status: 'published',
    isFeatured: true,
    publishedAt: 'August 10, 2025',
    seoTitle: 'Mock data before real endpoints',
    seoDescription: 'Why realistic mock data sharpens front-end and API work.',
    category: 'Workflow',
    intro: [
      'Mock data turns vague placeholders into concrete content shapes. It forces you to decide what a project, blog post, stat, and profile section actually need to contain.',
      'That early clarity helps avoid mismatches later, especially once APIs and a database enter the picture.'
    ],
    sections: [
      {
        heading: 'What good mock data gives you',
        paragraphs: [
          'It gives the front end something realistic to render, which immediately reveals missing fields, layout problems, and duplication.',
          'It also reduces the amount of guessing between front-end and back-end work.'
        ]
      },
      {
        heading: 'What to avoid',
        paragraphs: [
          'Mock data should not stay as random lorem ipsum forever. The closer it is to your actual content, the less rework you create for yourself later.'
        ]
      }
    ]
  },
  {
    id: 'post-student-projects-and-storytelling',
    slug: 'student-projects-and-storytelling',
    title: 'Turning Student Projects Into Clear Portfolio Stories',
    excerpt:
      'A practical way to present school and personal work so each project communicates context, responsibility, and outcome.',
    contentMarkdown: '## Lead with context\nContext makes projects easier to understand.',
    coverImageFileId: 'file-blog-storytelling-cover',
    coverImageAlt: 'Cards representing project storytelling',
    readingTimeMinutes: 6,
    status: 'published',
    isFeatured: false,
    publishedAt: 'September 02, 2025',
    seoTitle: 'Student projects as portfolio stories',
    seoDescription: 'A practical way to present student work clearly.',
    category: 'Career',
    intro: [
      'A project list is not the same as a portfolio. People need to understand what the project was, why it mattered, what your role was, and what decisions you made.',
      'That is especially true for student projects, where the context often matters as much as the final output.'
    ],
    sections: [
      {
        heading: 'Lead with context',
        paragraphs: [
          'Explain what the project was for, who it was made for, and what constraints shaped it. That makes the rest of the details easier to understand.'
        ]
      },
      {
        heading: 'Be specific about your role',
        paragraphs: [
          'Even a short description of the parts you owned can make a project feel much more credible and useful to readers.'
        ]
      }
    ]
  },
  {
    id: 'post-components-before-polish',
    slug: 'components-before-polish',
    title: 'Components Before Polish',
    excerpt:
      'Reusable UI pieces are not the glamorous part of a build, but they make the later polish stage much faster and safer.',
    contentMarkdown: '## Start with the repeated pieces\nRepeated patterns deserve components first.',
    coverImageFileId: 'file-blog-components-cover',
    coverImageAlt: 'UI components arranged in a grid',
    readingTimeMinutes: 3,
    status: 'published',
    isFeatured: false,
    publishedAt: 'September 21, 2025',
    seoTitle: 'Components before polish',
    seoDescription: 'Why reusable UI pieces are worth stabilising early.',
    category: 'Frontend',
    intro: [
      'The temptation is always to jump straight into beautiful one-off screens. I prefer to stabilise the basic button, chip, card, and section patterns first.',
      'Once those pieces are reliable, the rest of the UI tends to come together much faster.'
    ],
    sections: [
      {
        heading: 'Start with the repeated pieces',
        paragraphs: [
          'If a visual pattern appears in multiple places, it should probably exist as a reusable component before the project gets too large.'
        ]
      }
    ]
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
