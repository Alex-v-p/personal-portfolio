from __future__ import annotations

PROFILE_ROW = {'id': 'profile-alex-van-poppel',
 'first_name': 'Alex',
 'last_name': 'van Poppel',
 'headline': 'Applied Computer Science Student & Full-Stack Builder',
 'short_intro': 'I enjoy building software that feels useful in practice, whether that means a polished web interface, '
                'a data-heavy school project, or a system that I can actually deploy and maintain myself.',
 'long_bio': 'My work sits at the intersection of web development, software architecture, data projects, and '
             'self-hosting. I like understanding the systems behind a product, not just the screen in front of the '
             'user - so alongside building applications, I spend time learning about deployment, networking, storage, '
             'and maintainable structure.\n'
             '\n'
             'A lot of my recent work has come from school projects: client workshops, analysis assignments, machine '
             'learning experiments, and full-stack builds. Across all of them, I try to keep the same approach: make '
             'the problem clear, build something practical, and leave the project in a state that would still make '
             'sense a few months later.',
 'location': 'Lommel, Belgium',
 'email': 'alex@shuzu.dev',
 'phone': '+32 472 31 34 79',
 'avatar_file_id': 'file-avatar-alex',
 'hero_image_file_id': 'file-hero-portrait',
 'resume_file_id': 'file-resume',
 'cta_primary_label': 'Download Resume',
 'cta_primary_url': 'media://resume',
 'cta_secondary_label': 'Contact me',
 'cta_secondary_url': '/contact',
 'is_public': True,
 'created_at': '2026-03-28T10:00:00Z',
 'updated_at': '2026-04-01T12:00:00Z'}

PROJECT_ROWS = [{'id': 'project-portfolio-rebuild',
  'slug': 'portfolio-rebuild',
  'title': 'Portfolio Platform Rebuild',
  'teaser': 'A CMS-backed rebuild of my portfolio that turns a static student showcase into a more maintainable '
            'platform.',
  'summary': 'Reframed my earlier Laravel portfolio into a multi-part platform with a typed front end, API-backed '
             'content, admin tooling, media handling, and a structure that is easier to evolve over time.',
  'description_markdown': '## Context\n'
                          '\n'
                          'My earlier portfolio did its job well, but updating it still felt too manual. A lot of the '
                          'content lived in seeders, and every structural change pushed me back into the code.\n'
                          '\n'
                          '## What I changed\n'
                          '\n'
                          'For this rebuild, I focused on **separating content from presentation**:\n'
                          '\n'
                          '- an Angular front end for the public site and CMS\n'
                          '- a FastAPI backend for profile, project, blog, and stats data\n'
                          '- database-backed content instead of one-off static records\n'
                          '- public and admin routes that mirror the same content model\n'
                          '\n'
                          '## Why it matters\n'
                          '\n'
                          'The real goal was not just a redesign. I wanted a portfolio that could grow without turning '
                          'every content update into a mini refactor.\n'
                          '\n'
                          '## What I learned\n'
                          '\n'
                          'This project pushed me to think beyond a single page layout and into **systems design**: '
                          'schemas, reusable mappings, migration-friendly content, media storage, and how admin '
                          'workflows shape the public experience.\n',
  'cover_image_file_id': 'file-project-portfolio-rebuild-cover',
  'cover_image_alt': 'Portfolio rebuild cover with CMS and API themes',
  'github_url': 'https://github.com/shuzu/personal-portfolio',
  'github_repo_name': 'personal-portfolio',
  'demo_url': None,
  'company_name': 'Personal project',
  'started_on': '2026-02-01',
  'ended_on': None,
  'duration_label': 'Ongoing',
  'status': 'In progress',
  'state': 'published',
  'is_featured': True,
  'sort_order': 1,
  'published_at': '2026-03-26T09:00:00Z',
  'created_at': '2026-03-26T09:00:00Z',
  'updated_at': '2026-04-01T09:00:00Z'},
 {'id': 'project-laravel-portfolio-website',
  'slug': 'laravel-portfolio-website',
  'title': 'Laravel Portfolio Website',
  'teaser': 'My earlier TALL-stack portfolio, built to showcase projects, skills, and course work in one place.',
  'summary': 'Built a responsive portfolio in Laravel, Livewire, Tailwind CSS, and Alpine.js, with dynamic project '
             'filtering, seeded content, and self-hosted deployment on my own infrastructure.',
  'description_markdown': '## Context\n'
                          '\n'
                          'This was the portfolio that gave me a first complete end-to-end showcase: design, database, '
                          'backend logic, dynamic components, and deployment.\n'
                          '\n'
                          '## Stack\n'
                          '\n'
                          '- Laravel\n'
                          '- Livewire\n'
                          '- Tailwind CSS\n'
                          '- Alpine.js\n'
                          '- SQLite\n'
                          '\n'
                          '## My role\n'
                          '\n'
                          'This was a solo build, so I handled the full flow: planning, data modelling, '
                          'implementation, component reuse, hosting, and iteration.\n'
                          '\n'
                          '## Deployment angle\n'
                          '\n'
                          'One part I especially valued was hosting it myself. I used my own server setup with routing '
                          'and domain management, which made the project feel much closer to a real production system '
                          'than a classroom-only assignment.\n',
  'cover_image_file_id': 'file-project-laravel-portfolio-cover',
  'cover_image_alt': 'Laravel portfolio cover with cards and self-hosting theme',
  'github_url': None,
  'github_repo_name': None,
  'demo_url': None,
  'company_name': 'Personal project',
  'started_on': '2025-03-01',
  'ended_on': '2025-04-30',
  'duration_label': '2 months',
  'status': 'Completed',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 2,
  'published_at': '2025-05-05T09:00:00Z',
  'created_at': '2025-05-05T09:00:00Z',
  'updated_at': '2025-05-05T09:00:00Z'},
 {'id': 'project-placement-prediction-ml',
  'slug': 'placement-prediction-ml',
  'title': 'Placement Prediction with Machine Learning',
  'teaser': 'A machine learning project that explored how academic and background data can predict student placement '
            'outcomes.',
  'summary': 'Cleaned a student placement dataset, analysed relationships between features, and compared '
             'classification models to predict whether a student would be placed or not.',
  'description_markdown': '## Goal\n'
                          '\n'
                          'The aim was to build a model that could predict placement outcomes from education, '
                          'specialization, and background information while still keeping the analysis '
                          'understandable.\n'
                          '\n'
                          '## What I handled\n'
                          '\n'
                          '- dataset cleaning and missing value handling\n'
                          '- categorical encoding\n'
                          '- exploratory data analysis\n'
                          '- model comparison and evaluation\n'
                          '\n'
                          '## Tools\n'
                          '\n'
                          'Python, Pandas, Matplotlib, and Scikit-learn formed the core workflow.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'What made this project useful was not just the final model accuracy, but the way it forced '
                          'me to think about data quality, imbalance, and how to explain technical decisions to '
                          'someone who is not staring at the notebook with me.\n',
  'cover_image_file_id': 'file-project-placement-cover',
  'cover_image_alt': 'Machine learning project cover with charts and model cards',
  'github_url': None,
  'github_repo_name': None,
  'demo_url': None,
  'company_name': 'Thomas More',
  'started_on': '2025-02-01',
  'ended_on': '2025-03-31',
  'duration_label': '2 months',
  'status': 'Completed',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 3,
  'published_at': '2025-04-10T09:00:00Z',
  'created_at': '2025-04-10T09:00:00Z',
  'updated_at': '2025-04-10T09:00:00Z'},
 {'id': 'project-iot-security-system',
  'slug': 'iot-security-system',
  'title': 'IoT Security System',
  'teaser': 'A playful but technically demanding security demo that combined computer vision, motor control, and '
            'custom 3D design.',
  'summary': 'Built an AI-assisted turret prototype that could detect a person, aim a water gun, and trigger a '
             'smoke-screen effect, while dealing with the practical limits of embedded hardware.',
  'description_markdown': '## Concept\n'
                          '\n'
                          'The project combined software, hardware, and mechanical design in one system. A camera feed '
                          'was used to detect a person, then motors aimed a mounted water blaster in that direction.\n'
                          '\n'
                          '## Technical areas\n'
                          '\n'
                          '- computer vision and object detection\n'
                          '- hardware integration and control logic\n'
                          '- 3D modelling for physical parts\n'
                          '- problem solving around power, movement, and calibration\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'This project reminded me that real-world builds rarely fail for only one reason. Software, '
                          'physical tolerances, and hardware limitations all interact, which makes debugging much more '
                          'interesting than in a purely digital project.\n',
  'cover_image_file_id': 'file-project-iot-cover',
  'cover_image_alt': 'IoT turret project cover with hardware and computer vision theme',
  'github_url': None,
  'github_repo_name': None,
  'demo_url': None,
  'company_name': 'Thomas More',
  'started_on': '2024-11-01',
  'ended_on': '2025-01-15',
  'duration_label': '10 weeks',
  'status': 'Completed',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 4,
  'published_at': '2025-01-22T09:00:00Z',
  'created_at': '2025-01-22T09:00:00Z',
  'updated_at': '2025-01-22T09:00:00Z'},
 {'id': 'project-training-session-analysis',
  'slug': 'training-session-analysis',
  'title': 'Training Session Management Analysis',
  'teaser': 'A business analysis project focused on workshops, user questions, requirements, and turning discussion '
            'into clear deliverables.',
  'summary': 'Worked in a team to interview a client, capture requirements, structure workflows, and translate '
             'workshop findings into a clearer proposal for a training session management system.',
  'description_markdown': '## Problem space\n'
                          '\n'
                          'Not every valuable IT project ends with a deployed application. This one focused on '
                          'understanding a client problem properly before jumping into implementation.\n'
                          '\n'
                          '## My contribution\n'
                          '\n'
                          '- preparing workshop questions\n'
                          '- helping structure notes and next steps\n'
                          '- identifying user needs and process gaps\n'
                          '- turning discussion into a more concrete system view\n'
                          '\n'
                          '## Why I keep this project in my portfolio\n'
                          '\n'
                          'It shows a side of development that matters a lot to me: the ability to listen carefully, '
                          'ask good follow-up questions, and avoid building the wrong thing well.\n',
  'cover_image_file_id': 'file-project-analysis-cover',
  'cover_image_alt': 'Analysis project cover with workshops, diagrams, and prototype notes',
  'github_url': None,
  'github_repo_name': None,
  'demo_url': None,
  'company_name': 'Thomas More',
  'started_on': '2024-10-01',
  'ended_on': '2024-11-15',
  'duration_label': '6 weeks',
  'status': 'Completed',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 5,
  'published_at': '2024-11-20T09:00:00Z',
  'created_at': '2024-11-20T09:00:00Z',
  'updated_at': '2024-11-20T09:00:00Z'},
 {'id': 'project-exchange-student-portal',
  'slug': 'exchange-student-portal',
  'title': 'International Exchange Student Portal',
  'teaser': 'A concept and prototype centered on helping exchange students navigate practical information more easily.',
  'summary': 'Designed a portal concept for students preparing for an international exchange, with a focus on clear '
             'information, task flow, and reducing uncertainty during preparation.',
  'description_markdown': '## Idea\n'
                          '\n'
                          'Students preparing for an exchange often have to piece together information from many '
                          'different places. This concept explored how a single portal could bring the most important '
                          'steps together.\n'
                          '\n'
                          '## Focus areas\n'
                          '\n'
                          '- user journey before departure\n'
                          '- practical planning and checklist thinking\n'
                          '- layout and information hierarchy\n'
                          '- creating something approachable for stressed users\n'
                          '\n'
                          '## Takeaway\n'
                          '\n'
                          'What I liked most here was designing around uncertainty. The challenge was less about a '
                          'complex algorithm and more about making a confusing experience feel manageable.\n',
  'cover_image_file_id': 'file-project-exchange-cover',
  'cover_image_alt': 'Exchange portal cover with travel, planning, and student workflow theme',
  'github_url': None,
  'github_repo_name': None,
  'demo_url': None,
  'company_name': 'Thomas More',
  'started_on': '2024-09-15',
  'ended_on': '2024-10-20',
  'duration_label': '5 weeks',
  'status': 'Completed',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 6,
  'published_at': '2024-10-28T09:00:00Z',
  'created_at': '2024-10-28T09:00:00Z',
  'updated_at': '2024-10-28T09:00:00Z'}]

PROJECT_SKILL_NAMES_BY_PROJECT_SLUG = {'portfolio-rebuild': ['Angular', 'TypeScript', 'FastAPI', 'REST APIs', 'SQL', 'Git', 'Nx'],
 'laravel-portfolio-website': ['Laravel', 'Livewire', 'Tailwind CSS', 'Alpine.js', 'SQLite', 'Self-hosting'],
 'placement-prediction-ml': ['Python', 'Pandas', 'Matplotlib', 'Scikit-learn', 'Machine Learning'],
 'iot-security-system': ['Python', 'IoT Electronics', 'Orange Pi', 'FreeCAD', 'Linux'],
 'training-session-analysis': ['Requirements Analysis', 'Formal Communication', 'UML', 'Team Workshops'],
 'exchange-student-portal': ['Prototyping', 'Requirements Analysis', 'Formal Communication']}

BLOG_POST_ROWS = [{'id': 'blog-rebuilding-my-portfolio-from-laravel-to-cms',
  'slug': 'rebuilding-my-portfolio-from-laravel-to-cms',
  'title': 'Rebuilding My Portfolio from a Laravel Showcase into a CMS-Backed Platform',
  'excerpt': 'Why I moved away from a mostly static portfolio and started treating my own site more like a product '
             'with content workflows.',
  'content_markdown': 'My first portfolio did exactly what I needed at the time: it let me present projects, write an '
                      'about section, and show the skills I had been building. But after living with it for a while, I '
                      'noticed that every small content change still felt like a developer task.\n'
                      '\n'
                      'That became the trigger for a bigger rebuild. I wanted a portfolio where content could be '
                      'managed more cleanly, where stats and blog posts belonged to the same system, and where the '
                      'public site and admin area were clearly connected.\n'
                      '\n'
                      'The interesting part was that the technical challenge was not just visual redesign. It was '
                      'deciding where content should live, how it should be shaped in the API, and how the admin '
                      'experience should influence the public pages. Once I started viewing the portfolio as a '
                      'platform instead of a single site, a lot of design decisions became easier.\n'
                      '\n'
                      'The result is still very personal, but it is structured more like a real product. That matters '
                      'to me because it better reflects how I like to work: clear models, maintainable structure, and '
                      'content that can evolve without rewriting the entire app.\n',
  'cover_image_file_id': 'file-blog-portfolio-rebuild-cover',
  'cover_image_alt': 'Blog cover for rebuilding a portfolio platform',
  'reading_time_minutes': 6,
  'status': 'published',
  'is_featured': True,
  'published_at': '2026-03-30T08:00:00Z',
  'seo_title': 'Rebuilding My Portfolio from Laravel to a CMS-Backed Platform',
  'seo_description': 'A reflection on rebuilding a student portfolio into a structured platform with a CMS, API, and '
                     'better long-term maintainability.',
  'created_at': '2026-03-30T08:00:00Z',
  'updated_at': '2026-03-30T08:00:00Z'},
 {'id': 'blog-what-an-iot-security-demo-taught-me',
  'slug': 'what-an-iot-security-demo-taught-me',
  'title': 'What an IoT Security Demo Taught Me About Real-World Debugging',
  'excerpt': 'A small reflection on why hardware projects humble you faster than software-only builds.',
  'content_markdown': 'The funny thing about hardware-heavy projects is that they rarely break in a clean, isolated '
                      'way. In an IoT security demo, software logic, motor control, power limits, and even how a '
                      'component is mounted all influence each other.\n'
                      '\n'
                      'That made the project frustrating at times, but also genuinely useful. I had to debug across '
                      'layers instead of assuming the bug lived in one file. A good-looking detection result on screen '
                      'meant very little if the physical movement was inaccurate or too slow to be useful.\n'
                      '\n'
                      'It reminded me that building technical systems in the real world means accepting imperfect '
                      'conditions. Sensors are noisy, movement is messy, and elegant code does not automatically '
                      'produce elegant behaviour. That is exactly why I still value the project.\n',
  'cover_image_file_id': 'file-blog-iot-cover',
  'cover_image_alt': 'Blog cover about lessons from an IoT security project',
  'reading_time_minutes': 4,
  'status': 'published',
  'is_featured': False,
  'published_at': '2025-01-29T08:00:00Z',
  'seo_title': 'Lessons from Building an IoT Security Demo',
  'seo_description': 'A reflection on embedded debugging, hardware constraints, and why real-world builds behave '
                     'differently from pure software projects.',
  'created_at': '2025-01-29T08:00:00Z',
  'updated_at': '2025-01-29T08:00:00Z'},
 {'id': 'blog-translating-client-workshops-into-analysis',
  'slug': 'translating-client-workshops-into-analysis',
  'title': 'Translating Client Workshops into Useful Analysis',
  'excerpt': 'Notes on why asking the right follow-up questions can save a project from heading in the wrong '
             'direction.',
  'content_markdown': 'When a project starts with workshops and interviews instead of code, it can be tempting to see '
                      'that as the part before the real work. I do not think that is true anymore.\n'
                      '\n'
                      'In analysis-heavy projects, the quality of the solution is deeply tied to the quality of the '
                      'questions. What does the client actually struggle with day to day? Which workaround exists '
                      'already? Who loses time, and where? Without those details, it is easy to build something '
                      'polished that still misses the point.\n'
                      '\n'
                      'What I took away from these assignments is that good analysis is not passive note-taking. It is '
                      'structured listening. You are trying to surface assumptions, reduce ambiguity, and translate '
                      'messy conversations into something the team can act on.\n',
  'cover_image_file_id': 'file-blog-analysis-cover',
  'cover_image_alt': 'Blog cover about client workshops and requirements analysis',
  'reading_time_minutes': 5,
  'status': 'published',
  'is_featured': False,
  'published_at': '2024-11-26T08:00:00Z',
  'seo_title': 'Turning Client Workshops into Better Requirements Analysis',
  'seo_description': 'A short reflection on workshops, clarifying requirements, and why early analysis matters more '
                     'than it first appears.',
  'created_at': '2024-11-26T08:00:00Z',
  'updated_at': '2024-11-26T08:00:00Z'},
 {'id': 'blog-cleaning-placement-data-for-a-better-model',
  'slug': 'cleaning-placement-data-for-a-better-model',
  'title': 'Cleaning Placement Data for a Better Model',
  'excerpt': 'The least glamorous part of a machine learning project often decides whether the end result is '
             'trustworthy.',
  'content_markdown': 'The model gets the attention, but data preparation does most of the heavy lifting. In the '
                      'placement prediction project, the most important work happened before training a classifier.\n'
                      '\n'
                      'Missing values, categorical fields, class imbalance, and inconsistent formatting all changed '
                      'how meaningful the final output could be. Once I started treating cleaning as part of the '
                      'modelling process instead of a separate chore, the project became easier to reason about.\n'
                      '\n'
                      'That shift stuck with me. I still enjoy the modelling side, but I trust a project much more '
                      'when the path from raw input to final result is clearly understood and documented.\n',
  'cover_image_file_id': 'file-blog-placement-cover',
  'cover_image_alt': 'Blog cover about cleaning data for a machine learning model',
  'reading_time_minutes': 4,
  'status': 'published',
  'is_featured': False,
  'published_at': '2025-04-15T08:00:00Z',
  'seo_title': 'Cleaning Placement Data for Better Machine Learning Results',
  'seo_description': 'A short note on why data cleaning, encoding, and documentation matter so much in student machine '
                     'learning projects.',
  'created_at': '2025-04-15T08:00:00Z',
  'updated_at': '2025-04-15T08:00:00Z'}]

BLOG_TAG_NAMES_BY_POST_SLUG = {'rebuilding-my-portfolio-from-laravel-to-cms': ['Portfolio', 'Architecture', 'CMS'],
 'what-an-iot-security-demo-taught-me': ['IoT', 'Hardware', 'Python'],
 'translating-client-workshops-into-analysis': ['Analysis', 'Workshops', 'Communication'],
 'cleaning-placement-data-for-a-better-model': ['Machine Learning', 'Data', 'Python']}
