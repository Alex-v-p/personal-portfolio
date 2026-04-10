from __future__ import annotations

PROFILE_ROW = {'avatar_file_id': 'file-avatar-alex',
 'created_at': '2025-09-28T10:00:00Z',
 'cta_primary_label': 'Download CV',
 'cta_primary_url': '/assets/mock-resume.pdf',
 'cta_secondary_label': 'Contact me',
 'cta_secondary_url': '/contact',
 'email': 'hello@shuzu.dev',
 'first_name': 'Alex',
 'headline': 'Software Engineer',
 'hero_image_file_id': 'file-hero-portrait',
 'id': 'profile-alex-van-poppel',
 'is_public': True,
 'last_name': 'van Poppel',
 'location': 'Lommel, Belgium',
 'long_bio': 'I build portfolio sites, data-heavy student projects, and full-stack applications with a focus on '
             'maintainable architecture, thoughtful UI, and future-friendly structure.',
 'phone': '+32 470 31 34 39',
 'resume_file_id': 'file-resume',
 'short_intro': 'With a strong foundation in web development and UX design, I enjoy building user-centred experiences '
                'that are practical, clear, and pleasant to use.',
 'updated_at': '2025-10-01T12:00:00Z'}

PROJECT_ROWS = [{'company_name': 'Personal project',
  'cover_image_alt': 'Portfolio shell project cover',
  'cover_image_file_id': 'file-project-portfolio-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'demo_url': None,
  'description_markdown': 'Designed the shell, mock-data layer, and reusable layout pieces for a future CMS-backed '
                          'portfolio.',
  'duration_label': '3 months',
  'ended_on': None,
  'github_repo_name': 'personal-portfolio',
  'github_repo_owner': 'shuzu',
  'github_url': 'https://github.com/shuzu',
  'id': 'project-personal-portfolio',
  'is_featured': True,
  'published_at': '2025-10-01',
  'slug': 'personal-portfolio',
  'sort_order': 1,
  'started_on': '2025-07-01',
  'state': 'published',
  'status': 'Published',
  'summary': 'Designed and built a portfolio foundation around Angular, Tailwind, and modular page sections so content '
             'can move from mock data to real APIs without a redesign.',
  'teaser': 'A portfolio platform with a strong component system, room for CMS features, and a structure that can grow '
            'into full API-backed content.',
  'title': 'Personal Portfolio Platform',
  'updated_at': '2025-10-01T09:00:00+00:00'},
 {'company_name': 'Thomas More',
  'cover_image_alt': 'Plant care planning dashboard cover',
  'cover_image_file_id': 'file-project-plant-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'demo_url': None,
  'description_markdown': 'Focused on product thinking, schedules, and useful screens for plant care guidance.',
  'duration_label': '6 months',
  'ended_on': '2025-02-28',
  'github_repo_name': None,
  'github_repo_owner': None,
  'github_url': None,
  'id': 'project-plant-care-app',
  'is_featured': False,
  'published_at': '2025-03-01',
  'slug': 'plant-care-app',
  'sort_order': 2,
  'started_on': '2024-09-01',
  'state': 'completed',
  'status': 'Completed',
  'summary': 'Worked through the product and architecture side of a plant care app, focusing on useful flows, clear '
             'information presentation, and a structure that supports growth over time.',
  'teaser': 'A web application that helps users take care of plants with schedules, instructions, and a '
            'community-oriented concept.',
  'title': 'Plant Care App',
  'updated_at': '2025-10-01T09:00:00+00:00'},
 {'company_name': 'Thomas More',
  'cover_image_alt': 'MotoGP ticketing reservation flow cover',
  'cover_image_file_id': 'file-project-motogp-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'demo_url': 'https://example.com/motogp-demo',
  'description_markdown': 'Built an event-booking flow with React components, order forms, and confirmation logic.',
  'duration_label': '6 months',
  'ended_on': '2025-02-28',
  'github_repo_name': None,
  'github_repo_owner': None,
  'github_url': None,
  'id': 'project-motogp-ticketing',
  'is_featured': False,
  'published_at': '2025-03-12',
  'slug': 'motogp-ticketing',
  'sort_order': 3,
  'started_on': '2024-09-01',
  'state': 'completed',
  'status': 'Completed',
  'summary': 'Built React-based ticket ordering and management flows with clean state handling, user-friendly '
             'confirmation screens, and backend integration patterns.',
  'teaser': 'A reservation flow with order screens, confirmation logic, and ticket-management interactions for event '
            'bookings.',
  'title': 'MotoGP Ticket Reservation System',
  'updated_at': '2025-10-01T09:00:00+00:00'},
 {'company_name': 'Thomas More',
  'cover_image_alt': 'Dinosaur classifier training pipeline cover',
  'cover_image_file_id': 'file-project-dino-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'demo_url': None,
  'description_markdown': 'Worked on data preparation, augmentation, training structure, and reproducible '
                          'experimentation.',
  'duration_label': '4 months',
  'ended_on': '2025-05-31',
  'github_repo_name': 'dinosaur-image-classifier',
  'github_repo_owner': 'shuzu',
  'github_url': 'https://github.com/shuzu',
  'id': 'project-dino-classifier',
  'is_featured': False,
  'published_at': '2025-06-01',
  'slug': 'dino-classifier',
  'sort_order': 4,
  'started_on': '2025-04-01',
  'state': 'completed',
  'status': 'Completed',
  'summary': 'Cleaned datasets, set up augmentation, and trained a TensorFlow/Keras model while documenting the '
             'pipeline clearly enough to iterate on results later.',
  'teaser': 'A machine learning project using image datasets and EfficientNet to classify dinosaur species.',
  'title': 'Dinosaur Image Classifier',
  'updated_at': '2025-10-01T09:00:00+00:00'},
 {'company_name': 'Thomas More',
  'cover_image_alt': 'Auction house API architecture cover',
  'cover_image_file_id': 'file-project-auction-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'demo_url': None,
  'description_markdown': 'Implemented REST endpoints and pattern-focused services in a Spring Boot project.',
  'duration_label': '3 months',
  'ended_on': '2025-06-30',
  'github_repo_name': 'auction-house',
  'github_repo_owner': 'shuzu',
  'github_url': 'https://github.com/shuzu',
  'id': 'project-auction-house-api',
  'is_featured': False,
  'published_at': '2025-07-01',
  'slug': 'auction-house-api',
  'sort_order': 5,
  'started_on': '2025-06-01',
  'state': 'completed',
  'status': 'Completed',
  'summary': 'Designed endpoints for bidding workflows and observer registration while keeping the architecture '
             'focused on testable patterns and clear responsibilities.',
  'teaser': 'A Spring Boot API project that implements Singleton and Observer patterns in a practical auction domain.',
  'title': 'Auction House REST API',
  'updated_at': '2025-10-01T09:00:00+00:00'}]

PROJECT_SKILL_NAMES_BY_PROJECT_SLUG = {'auction-house-api': ['Java', 'Spring Boot', 'REST APIs', 'Design Patterns'],
 'dino-classifier': ['Python', 'TensorFlow', 'EfficientNet', 'ML'],
 'motogp-ticketing': ['React', 'REST APIs', 'State Management'],
 'personal-portfolio': ['Angular', 'Tailwind CSS', 'TypeScript', 'Nx'],
 'plant-care-app': ['Laravel', 'Livewire', 'Tailwind CSS', 'UX']}

BLOG_POST_ROWS = [{'content_markdown': '# Start with the shell\n'
                      '\n'
                      'When a portfolio starts to grow, the first page is almost never the hard part. The real '
                      'challenge is whether the structure underneath can absorb more content **without forcing a '
                      'redesign** every few weeks.\n'
                      '\n'
                      '## Why stage the work\n'
                      '\n'
                      'Breaking the project into layout, mock data, pages, API, database, and admin phases makes each '
                      'decision smaller and more deliberate.\n'
                      '\n'
                      '- It keeps the front end moving while the backend is still undefined.\n'
                      '- It makes design issues visible before real data arrives.\n'
                      '- It reduces the temptation to solve everything at once.\n'
                      '\n'
                      '## What the shell needs to do\n'
                      '\n'
                      'The shell should give every page the same foundation:\n'
                      '\n'
                      '1. stable navigation\n'
                      '2. a predictable page container\n'
                      '3. consistent spacing\n'
                      '4. footer and utility actions\n'
                      '\n'
                      '> A good shell turns future work into a content problem instead of a redesign problem.\n'
                      '\n'
                      '## The practical payoff\n'
                      '\n'
                      'Once the shell is stable, later stages become much safer. You can focus on projects, blog '
                      'posts, stats, and API responses without having to rewrite the outer frame each time.\n'
                      '\n'
                      '### Small structure, big leverage\n'
                      '\n'
                      'Even simple reusable pieces such as cards, chips, buttons, and section headers create a lot of '
                      'leverage. They make the portfolio feel coherent early and keep later polish cheap.',
  'cover_image_alt': 'Portfolio shell layout illustration',
  'cover_image_file_id': 'file-blog-shell-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'excerpt': 'A look at why locking the layout, route structure, and reusable UI early makes the later content and API '
             'stages easier to manage.',
  'id': 'post-building-a-portfolio-shell',
  'is_featured': True,
  'published_at': 'July 29, 2025',
  'reading_time_minutes': 5,
  'seo_description': 'Why a strong shell makes later portfolio stages easier.',
  'seo_title': 'Building a scalable portfolio shell',
  'slug': 'building-a-portfolio-shell',
  'status': 'published',
  'title': 'Building a Portfolio Shell That Can Scale Later',
  'updated_at': '2025-10-01T09:00:00+00:00'},
 {'content_markdown': '# Model the content before the API exists\n'
                      '\n'
                      'Mock data turns vague placeholders into actual content shapes. It forces you to decide what a '
                      'project, a blog post, or a stat card **really needs to contain**.\n'
                      '\n'
                      '## What good mock data gives you\n'
                      '\n'
                      'It helps answer questions early:\n'
                      '\n'
                      '- Which fields are required for the page to feel complete?\n'
                      '- Which values are only display helpers?\n'
                      '- Which repeated shapes deserve reusable components?\n'
                      '\n'
                      '## What to avoid\n'
                      '\n'
                      'Mock data should not stay random lorem ipsum forever. The closer it gets to your real portfolio '
                      'content, the less rewrite you create for yourself later.\n'
                      '\n'
                      '### A useful rule\n'
                      '\n'
                      'Keep the mock data close to your future schema. That way the page can switch from local files '
                      'to an API response with minimal changes.\n'
                      '\n'
                      'The main content can still be authored as markdown in the database and rendered cleanly on the '
                      'front end.',
  'cover_image_alt': 'Mock data objects represented as cards',
  'cover_image_file_id': 'file-blog-mock-data-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'excerpt': 'Using realistic mock objects first helps shape pages, models, and edge cases before the backend becomes '
             'a dependency.',
  'id': 'post-mock-data-first',
  'is_featured': True,
  'published_at': 'August 10, 2025',
  'reading_time_minutes': 4,
  'seo_description': 'Why realistic mock data sharpens front-end and API work.',
  'seo_title': 'Mock data before real endpoints',
  'slug': 'mock-data-first',
  'status': 'published',
  'title': 'Why I Prefer Mock Data Before Real Endpoints',
  'updated_at': '2025-10-01T09:00:00+00:00'},
 {'content_markdown': '# Lead with context\n'
                      '\n'
                      'A project list is not the same as a portfolio. Readers need to understand **what the project '
                      'was**, **why it mattered**, and **what your role was**.\n'
                      '\n'
                      '## Explain the setting\n'
                      '\n'
                      'Start with the context:\n'
                      '\n'
                      '- Was it a school assignment?\n'
                      '- A client exercise?\n'
                      '- A personal build?\n'
                      '- A team project with a defined role?\n'
                      '\n'
                      '## Show responsibility clearly\n'
                      '\n'
                      'Even a short line about what you owned makes a project much more useful to readers. It helps '
                      'them understand your contribution without making them guess.\n'
                      '\n'
                      '## End with outcome\n'
                      '\n'
                      'The strongest portfolio stories usually end with one of these:\n'
                      '\n'
                      '1. what shipped\n'
                      '2. what improved\n'
                      '3. what you learned\n'
                      '\n'
                      'That is what turns a coursework item into a convincing portfolio piece.',
  'cover_image_alt': 'Cards representing project storytelling',
  'cover_image_file_id': 'file-blog-storytelling-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'excerpt': 'A practical way to present school and personal work so each project communicates context, '
             'responsibility, and outcome.',
  'id': 'post-student-projects-and-storytelling',
  'is_featured': False,
  'published_at': 'September 02, 2025',
  'reading_time_minutes': 6,
  'seo_description': 'A practical way to present student work clearly.',
  'seo_title': 'Student projects as portfolio stories',
  'slug': 'student-projects-and-storytelling',
  'status': 'published',
  'title': 'Turning Student Projects Into Clear Portfolio Stories',
  'updated_at': '2025-10-01T09:00:00+00:00'},
 {'content_markdown': '# Start with the repeated pieces\n'
                      '\n'
                      'The temptation is always to jump straight into beautiful one-off screens. I prefer to stabilise '
                      'the repeated UI first.\n'
                      '\n'
                      '## Components reduce friction\n'
                      '\n'
                      'A reusable button, chip, card, or section title does more than save time. It also keeps the '
                      'design language consistent while the product is still changing.\n'
                      '\n'
                      '## What deserves a component first\n'
                      '\n'
                      '- anything that appears on multiple pages\n'
                      '- anything with repeated spacing and typography\n'
                      '- anything that is likely to gain variants later\n'
                      '\n'
                      '## Polish lands better later\n'
                      '\n'
                      'Once the repeated pieces are stable, polish becomes easier. You stop fighting duplicated markup '
                      'and start refining the system instead.\n'
                      '\n'
                      'A small component layer is usually more valuable than an early animation pass.',
  'cover_image_alt': 'UI components arranged in a grid',
  'cover_image_file_id': 'file-blog-components-cover',
  'created_at': '2025-10-01T09:00:00+00:00',
  'excerpt': 'Reusable UI pieces are not the glamorous part of a build, but they make the later polish stage much '
             'faster and safer.',
  'id': 'post-components-before-polish',
  'is_featured': False,
  'published_at': 'September 21, 2025',
  'reading_time_minutes': 3,
  'seo_description': 'Why reusable UI pieces are worth stabilising early.',
  'seo_title': 'Components before polish',
  'slug': 'components-before-polish',
  'status': 'published',
  'title': 'Components Before Polish',
  'updated_at': '2025-10-01T09:00:00+00:00'}]

BLOG_TAG_NAMES_BY_POST_SLUG = {'building-a-portfolio-shell': ['Angular', 'Architecture', 'UI'],
 'components-before-polish': ['Components', 'Tailwind', 'Design Systems'],
 'mock-data-first': ['Mock Data', 'Planning', 'TypeScript'],
 'student-projects-and-storytelling': ['Career', 'Projects', 'Writing']}

