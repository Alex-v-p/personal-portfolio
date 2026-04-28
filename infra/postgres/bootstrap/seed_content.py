from __future__ import annotations

# CMS backup exported on 2026-04-28, then enriched with non-placeholder portfolio copy.
# These rows are intentionally static so a fresh database rebuild restores the same public content.

PROFILE_ROW = {'id': 'affede64-54ea-5bf3-ac15-87fc0bbb642b',
 'first_name': 'Alex',
 'last_name': 'van Poppel',
 'headline': 'a software engineering and AI student',
 'headline_nl': 'een softwareontwikkelaar en AI-student',
 'short_intro': 'I am a Software Engineering student at Thomas More in Geel who enjoys experimenting with new tools '
                'and building applications to run on my infrastructure.',
 'short_intro_nl': 'Ik ben een Software Engineering student aan Thomas More in Geel die geniet van het experimenteren '
                   'met nieuwe tools en het bouwen van applicaties die kunnen worden uitgevoerd op mijn '
                   'infrastructuur.',
 'long_bio': 'Hi, I’m Alex van Poppel, a Software Development student at Thomas More in Geel. I chose Applied Computer '
             'Science because I’ve always been curious about how technology works behind the scenes, not just how to '
             'use apps, but how they are built and kept running.\n'
             '\n'
             'I enjoy building web applications, experimenting with my homelab, and figuring out how different systems '
             'fit together. I’m especially interested in the practical side of software, like deployment, networking, '
             'storage, and understanding how everything works around the application itself.\n'
             '\n'
             'Outside of school, I like working on small personal tools, upgrading PCs, and experimenting with my NAS '
             'and homelab. When I’m not doing something tech-related, I enjoy gaming and spending time with friends, '
             'which helps me recharge and keeps things balanced.',
 'long_bio_nl': 'Hallo, ik ben Alex van Poppel, een Student Softwareontwikkeling aan de Thomas More in Geel. Ik heb '
                'Gebruikte Computerwetenschap gekozen omdat ik altijd ben geïnteresseerd in hoe technologie werkt '
                'achter de schermen, niet alleen hoe apps worden gebruikt, maar ook hoe ze worden gebouwd en worden '
                'gehouden in werking.\n'
                '\n'
                'Ik geniet het om web-apps te bouwen, experimenteer met mijn homelab en figureren uit hoe '
                'verschillende systemen bij elkaar passen. Ik ben bijzonder geïnteresseerd in de praktische kant van '
                'software, zoals implementatie, netwerken, opslag en begrijpen hoe alles werkt rondom de applicatie '
                'zelf.\n'
                '\n'
                "Buiten school, geniet ik ervan kleine persoonlijke hulpmiddelen te bouwen, PC's te upgraden en "
                'experimenteer met mijn NAS en homelab. Wanneer ik niet iets technisch doe, geniet ik van spelen en '
                'tijd met vrienden, wat me herstelt en hielp me even te balanceren.',
 'location': 'Lommel, Belgium',
 'email': 'vanpoppel.alex@pm.me',
 'phone': '+32 472 31 34 79',
 'avatar_file_id': '4cb5bc60-f606-5fe1-9fdd-e6bf3b08af26',
 'hero_image_file_id': '2b4b1004-f658-5d39-b5de-2fcd0e4d2fec',
 'resume_file_id': 'a98b5896-2b94-4d25-97c7-fb82be8144b1',
 'resume_file_id_nl': '55936bda-0554-48f3-8ece-32fc3f6e273e',
 'cta_primary_label': 'Download Resume',
 'cta_primary_label_nl': 'Download CV',
 'cta_primary_url': 'media://resume',
 'cta_secondary_label': 'Contact me',
 'cta_secondary_label_nl': 'Contact me',
 'cta_secondary_url': '/contact',
 'is_public': True,
 'created_at': '2026-04-17T10:00:00+00:00',
 'updated_at': '2026-04-28T12:23:30.861323+00:00'}

PROJECT_ROWS = [{'id': '33c06683-2241-54d8-b352-3104dc61a77d',
  'slug': 'laravel-portfolio-website',
  'title': 'Old Laravel Portfolio',
  'title_nl': 'Oude Laravel-portfolio',
  'teaser': 'My earlier self-hosted portfolio, built to present projects, skills, and achievements in a dynamic way.',
  'teaser_nl': 'Mijn eerdere zelfgehoste portfolio, gebouwd om projecten, skills en prestaties dynamisch te tonen.',
  'summary': 'This was my previous portfolio website, built with the TALL stack so I could present my work more '
             'dynamically. It gave me a full end-to-end project of my own, from data modelling and UI work to hosting '
             'it on infrastructure I managed myself.',
  'summary_nl': 'Dit was mijn vorige portfolio-website, gebouwd met de TALL-stack zodat ik mijn werk dynamischer kon '
                'presenteren. Het gaf me een volledig end-to-end project van mezelf, van datamodellering en UI-werk '
                'tot hosting op infrastructuur die ik zelf beheerde.',
  'description_markdown': '## Why I built it\n'
                          '\n'
                          'I wanted a portfolio that did more than show static text. The site was designed to present '
                          'my projects, skills, and course work clearly while also giving me a chance to practise '
                          'building and hosting something of my own.\n'
                          '\n'
                          '## Stack\n'
                          '\n'
                          '- Laravel\n'
                          '- Livewire\n'
                          '- Tailwind CSS\n'
                          '- Alpine.js\n'
                          '- SQLite\n'
                          '\n'
                          '## What I handled\n'
                          '\n'
                          'This was a solo project, so I was responsible for the full process: design ideas, data '
                          'modelling, migrations, seeders, backend logic, reusable Blade components, filtering '
                          'behaviour, styling, and deployment.\n'
                          '\n'
                          '## Deployment and hosting\n'
                          '\n'
                          'One of the most valuable parts of this project was hosting it myself. I routed traffic '
                          'through my own setup using Cloudflare, Nginx, Docker, and a TrueNAS-based server '
                          'environment. That made the portfolio feel much closer to a real deployment than a project '
                          'that only ever runs locally.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'Building this portfolio taught me a lot about modular design, self-hosting, and how quickly '
                          'content can become hard to manage if it lives too close to the code. That lesson is also '
                          'what pushed me toward rebuilding my portfolio later with a cleaner content workflow.',
  'description_markdown_nl': '## Waarom ik dit bouwde\n'
                             '\n'
                             'Ik wilde een portfolio dat meer deed dan alleen statische tekst tonen. De site was '
                             'bedoeld om mijn projecten, skills en schoolwerk duidelijk te presenteren en mij tegelijk '
                             'de kans te geven om zelf iets te bouwen én te hosten.\n'
                             '\n'
                             '## Stack\n'
                             '\n'
                             '- Laravel\n'
                             '- Livewire\n'
                             '- Tailwind CSS\n'
                             '- Alpine.js\n'
                             '- SQLite\n'
                             '\n'
                             '## Wat ik heb gedaan\n'
                             '\n'
                             'Dit was een solo-project, dus ik was verantwoordelijk voor het volledige proces: '
                             'ontwerpideeën, datamodellering, migraties, seeders, backendlogica, herbruikbare '
                             'Blade-componenten, filtergedrag, styling en deployment.\n'
                             '\n'
                             '## Deployment en hosting\n'
                             '\n'
                             'Een van de meest waardevolle onderdelen van dit project was dat ik het zelf hostte. Ik '
                             'stuurde verkeer via mijn eigen setup met Cloudflare, Nginx, Docker en een op TrueNAS '
                             'gebaseerde serveromgeving. Daardoor voelde dit portfolio veel dichter bij een echte '
                             'deployment dan een project dat alleen lokaal draait.\n'
                             '\n'
                             '## Reflectie\n'
                             '\n'
                             'Het bouwen van dit portfolio heeft me veel geleerd over modulair ontwerp, self-hosting '
                             'en hoe snel content moeilijk te beheren wordt als die te dicht op de code leeft. Die les '
                             'heeft me er ook toe aangezet om mijn portfolio later opnieuw te bouwen met een veel '
                             'schonere contentworkflow.',
  'cover_image_file_id': 'e059f2b2-311f-4447-b22b-178b2f4ca165',
  'github_url': 'https://github.com/Alex-v-p/Personal-Portfolio-laravel',
  'github_repo_owner': 'Alex-v-p',
  'github_repo_name': 'laravel-portfolio-website',
  'demo_url': 'https://www.alex-vp.com',
  'company_name': 'Personal project',
  'started_on': '2025-03-01',
  'ended_on': '2025-04-30',
  'duration_label': '2 months',
  'duration_label_nl': '2 maanden',
  'status': 'Completed',
  'status_nl': 'Afgerond',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 3,
  'published_at': '2025-05-05T09:00:00+00:00',
  'created_at': '2025-05-05T09:00:00+00:00',
  'updated_at': '2026-04-28T13:11:55.516331+00:00'},
 {'id': '1d221f50-522f-5faa-a12c-191e19db6a44',
  'slug': 'internal-exchange-student-portal',
  'title': 'Internal Exchange Student Portal',
  'title_nl': 'Intern portaal voor uitwisselingsstudenten',
  'teaser': 'A student portal for managing international exchanges and guiding students through the academic process '
            'abroad.\n'
            '\n'
            '\n'
            '[Download '
            'EchangePortal_UserGuide](/api/public/media-files/762ac5ca-cc40-494f-9c61-c5f7171b533c/annotated-ExchangePortal_User_Guide.pdf '
            '"download")\n',
  'teaser_nl': 'Een studentenportaal om internationale uitwisselingen te beheren en studenten door het academische '
               'proces in het buitenland te begeleiden.\n'
               '\n'
               '\n'
               '[Download '
               'EchangePortal_UserGuide](/api/public/media-files/762ac5ca-cc40-494f-9c61-c5f7171b533c/annotated-ExchangePortal_User_Guide.pdf '
               '"download")',
  'summary': 'This client-facing school project focused on building a clear, user-friendly platform for international '
             'exchange students. Our team first reviewed the work of three other teams, combined their strongest ideas '
             'into a single prototype, and then developed the approved solution iteratively using Scrum.',
  'summary_nl': 'Dit schoolproject met een echte klant draaide om het bouwen van een helder en gebruiksvriendelijk '
                'platform voor internationale uitwisselingsstudenten. Ons team bekeek eerst het werk van drie andere '
                'teams, combineerde hun sterkste ideeën in één prototype en werkte de goedgekeurde oplossing daarna '
                'iteratief uit met Scrum.',
  'description_markdown': '## Project overview\n'
                          '\n'
                          'This project was built to support international exchange students throughout their study '
                          'journey. The goal was to create a platform that could make the process less confusing by '
                          'centralising guidance, resources, and communication in one place.\n'
                          '\n'
                          '## My role\n'
                          '\n'
                          'I took the lead during the analysis phase. My team reviewed the solution documents created '
                          'by three other teams, identified the strongest ideas in each one, and combined them into a '
                          'single prototype that we later presented to the client. Once the concept was approved, I '
                          'worked heavily on the frontend and on shaping the underlying data structure of the '
                          'application. I also stayed in regular contact with the product owner so we could validate '
                          'features early and keep the platform easy to use.\n'
                          '\n'
                          '## Stack and workflow\n'
                          '\n'
                          '- Laravel and Livewire for the application\n'
                          '- Tailwind CSS for styling\n'
                          '- Figma for prototyping and review\n'
                          '- Git and GitHub for collaboration\n'
                          '- Scrum for planning and iterative delivery\n'
                          '\n'
                          '## Challenges\n'
                          '\n'
                          'One of the biggest challenges was combining different design ideas and technical approaches '
                          'into one coherent direction. We solved that by discussing trade-offs openly, justifying '
                          'each feature, and keeping the client close to the process. That helped reduce confusion '
                          'later and gave the final platform a clearer identity.\n'
                          '\n'
                          '## Outcome\n'
                          '\n'
                          'By the end of the project, we had a complete portal that could support students from '
                          'enrolment and planning through to the wider exchange process. More importantly, it taught '
                          'me a lot about leadership, analysis, and how much smoother development becomes when the '
                          'prototype phase is handled well.',
  'description_markdown_nl': '## Projectoverzicht\n'
                             '\n'
                             'Dit project werd gebouwd om internationale uitwisselingsstudenten tijdens hun volledige '
                             'traject te ondersteunen. Het doel was om een platform te maken dat het proces minder '
                             'verwarrend zou maken door begeleiding, middelen en communicatie op één plek te '
                             'centraliseren.\n'
                             '\n'
                             '## Mijn rol\n'
                             '\n'
                             'Ik nam de leiding tijdens de analysefase. Mijn team bekeek de oplossingsdocumenten van '
                             'drie andere teams, haalde uit elk team de sterkste ideeën en combineerde die tot één '
                             'prototype dat we later aan de klant presenteerden. Zodra het concept was goedgekeurd, '
                             'werkte ik veel aan de frontend en aan de onderliggende datastructuur van de applicatie. '
                             'Ik bleef ook in regelmatig contact met de product owner zodat we features vroeg konden '
                             'valideren en het platform gebruiksvriendelijk konden houden.\n'
                             '\n'
                             '## Stack en werkwijze\n'
                             '\n'
                             '- Laravel en Livewire voor de applicatie\n'
                             '- Tailwind CSS voor styling\n'
                             '- Figma voor prototyping en review\n'
                             '- Git en GitHub voor samenwerking\n'
                             '- Scrum voor planning en iteratieve oplevering\n'
                             '\n'
                             '## Uitdagingen\n'
                             '\n'
                             'Een van de grootste uitdagingen was om verschillende ontwerpideeën en technische '
                             'aanpakken samen te brengen in één duidelijke richting. Dat hebben we opgelost door open '
                             'over afwegingen te praten, elke feature te onderbouwen en de klant dicht bij het proces '
                             'te houden. Zo verminderden we latere verwarring en kreeg het uiteindelijke platform een '
                             'veel duidelijkere identiteit.\n'
                             '\n'
                             '## Resultaat\n'
                             '\n'
                             'Tegen het einde van het project hadden we een volledig portaal dat studenten kon '
                             'ondersteunen vanaf inschrijving en planning tot het bredere uitwisselingsproces. '
                             'Belangrijker nog: het project heeft me veel geleerd over leiderschap, analyse en hoeveel '
                             'vlotter ontwikkeling verloopt wanneer de prototypefase goed wordt aangepakt.',
  'cover_image_file_id': '1200a60d-19d8-5888-a268-fdb5072b14ce',
  'github_url': None,
  'github_repo_owner': 'Alex-v-p',
  'github_repo_name': 'InternationalStudent-portal',
  'demo_url': None,
  'company_name': 'Thomas More client project',
  'started_on': '2025-02-01',
  'ended_on': '2025-06-30',
  'duration_label': '5 months',
  'duration_label_nl': '5 maanden',
  'status': 'Completed',
  'status_nl': 'Afgerond',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 1,
  'published_at': '2025-07-05T09:00:00+00:00',
  'created_at': '2025-07-05T09:00:00+00:00',
  'updated_at': '2026-04-28T13:11:07.442269+00:00'},
 {'id': '65b1b1fc-cfda-52c7-9090-cf105b461e41',
  'slug': 'iot-security-system',
  'title': 'IoT Security System',
  'title_nl': 'IoT-beveiligingssysteem',
  'teaser': 'A playful security prototype that combined computer vision, embedded control, and custom 3D-printed '
            'hardware.\n'
            '\n'
            '\n'
            '[Download '
            'SecuritySystemIot_Report](/api/public/media-files/f1499b84-1e62-47b6-9fcb-fa3e11a5afde/Iot_SecuritySystem_Report.pdf '
            '"download")\n',
  'teaser_nl': 'Een speels beveiligingsprototype dat computer vision, embedded aansturing en op maat geprinte hardware '
               'combineerde.\n'
               '\n'
               '\n'
               '[Download '
               'SecuritySystemIot_Report](/api/public/media-files/f1499b84-1e62-47b6-9fcb-fa3e11a5afde/Iot_SecuritySystem_Report.pdf '
               '"download")',
  'summary': 'For this IoT project, my team built a hardware-software demo that detects a person, aims a water gun at '
             'them, and triggers a smoke-screen effect when they get too close. It was a fun concept, but also a '
             'serious exercise in system integration, timing, and hardware limitations.',
  'summary_nl': 'Voor dit IoT-project bouwde mijn team een hardware-softwaredemo die een persoon detecteert, een '
                'waterpistool op hen richt en een rookeffect activeert wanneer iemand te dichtbij komt. Het was een '
                'leuk concept, maar ook een serieuze oefening in systeemintegratie, timing en hardwarebeperkingen.',
  'description_markdown': '## Concept\n'
                          '\n'
                          'This project brought together AI, electronics, and mechanical design in one system. A '
                          "camera feed was used to detect a person's head, stepper motors aimed the turret, and a "
                          'water gun handled the final action. If someone moved too close, a relay-controlled fog '
                          'machine added a second defensive effect.\n'
                          '\n'
                          '## My contribution\n'
                          '\n'
                          'I was responsible for the 3D modelling side of the project, including the design and '
                          'printing of the mounts for the water gun, camera, and motors. I also contributed to the '
                          'control logic that connected the detection step to motor movement, helping translate visual '
                          'input into a stable mechanical response.\n'
                          '\n'
                          '## Stack\n'
                          '\n'
                          '- Python and OpenCV for the detection pipeline\n'
                          '- Orange Pi as the main controller\n'
                          '- Stepper motors for movement\n'
                          '- Relay-controlled smoke output\n'
                          '- FreeCAD and 3D printing for the custom housing\n'
                          '\n'
                          '## Challenges\n'
                          '\n'
                          'The main technical challenge was keeping the system responsive without making the turret '
                          'shake or overshoot. We improved this by adding cooldown logic and by tuning the sensitivity '
                          'of the detection step. We also had to work around the limits of the Orange Pi, which meant '
                          'simplifying parts of the onboard AI pipeline so the system remained usable in real time.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'This project taught me a lot about the gap between a cool idea and a working system. It '
                          'also made me much more confident in combining software with physical design, especially '
                          'when there are real-world constraints like hardware performance, motion control, and '
                          'mounting stability.',
  'description_markdown_nl': '## Concept\n'
                             '\n'
                             'Dit project bracht AI, elektronica en mechanisch ontwerp samen in één systeem. Een '
                             'camerafeed werd gebruikt om iemands hoofd te detecteren, stappenmotoren richtten de '
                             'turret en een waterpistool zorgde voor de uiteindelijke actie. Als iemand te dichtbij '
                             'kwam, voegde een relaisgestuurde rookmachine een tweede verdedigend effect toe.\n'
                             '\n'
                             '## Mijn bijdrage\n'
                             '\n'
                             'Ik was verantwoordelijk voor het 3D-modelleringsgedeelte van het project, waaronder het '
                             'ontwerpen en printen van de houders voor het waterpistool, de camera en de motoren. '
                             'Daarnaast hielp ik ook aan de besturingslogica die de detectiestap koppelde aan de '
                             'motorbewegingen, zodat visuele input in een stabiele mechanische respons werd omgezet.\n'
                             '\n'
                             '## Stack\n'
                             '\n'
                             '- Python en OpenCV voor de detectiepijplijn\n'
                             '- Orange Pi als hoofdcontroller\n'
                             '- Stappenmotoren voor beweging\n'
                             '- Relaisgestuurde rookoutput\n'
                             '- FreeCAD en 3D-printing voor de behuizing op maat\n'
                             '\n'
                             '## Uitdagingen\n'
                             '\n'
                             'De grootste technische uitdaging was het systeem responsief houden zonder dat de turret '
                             'begon te trillen of doorschoot. Dat verbeterden we door cooldown-logica toe te voegen en '
                             'de gevoeligheid van de detectiestap af te stemmen. We moesten ook rekening houden met de '
                             'limieten van de Orange Pi, waardoor we delen van de AI-pijplijn op het toestel '
                             'vereenvoudigden zodat het systeem bruikbaar bleef in realtime.\n'
                             '\n'
                             '## Reflectie\n'
                             '\n'
                             'Dit project leerde me veel over het verschil tussen een cool idee en een werkend '
                             'systeem. Het maakte me ook veel zekerder in het combineren van software met fysiek '
                             'ontwerp, zeker wanneer er echte beperkingen zijn zoals hardwareprestaties, motion '
                             'control en montagestabiliteit.',
  'cover_image_file_id': '289fa361-f996-5266-a68e-6a7fe1802cb2',
  'github_url': None,
  'github_repo_owner': 'Alex-v-p',
  'github_repo_name': 'iot-security-system',
  'demo_url': None,
  'company_name': 'Thomas More',
  'started_on': '2024-05-01',
  'ended_on': '2024-07-31',
  'duration_label': '3 months',
  'duration_label_nl': '3 maanden',
  'status': 'Completed',
  'status_nl': 'Afgerond',
  'state': 'completed',
  'is_featured': True,
  'sort_order': 2,
  'published_at': '2024-08-10T09:00:00+00:00',
  'created_at': '2024-08-10T09:00:00+00:00',
  'updated_at': '2026-04-28T13:11:30.157880+00:00'},
 {'id': '94ccc9b4-57c3-4e81-ac68-4a873a727c10',
  'slug': 'angular-portfolio-website',
  'title': 'Angular Portfolio',
  'title_nl': 'Angular Portfolio',
  'teaser': 'The current self-hosted portfolio platform, rebuilt with Angular, FastAPI, a CMS, media backups, and a '
            'public assistant.',
  'teaser_nl': 'Het huidige zelfgehoste portfolioplatform, herbouwd met Angular, FastAPI, een CMS, mediaback-ups en '
               'een publieke assistent.',
  'summary': 'This is the portfolio you are looking at now: a full rebuild of my earlier Laravel portfolio into a more '
             'maintainable platform. The goal was not only to make the public site look better, but also to make the '
             'content easier to manage, back up, seed, translate, and rebuild whenever the project changes.',
  'summary_nl': 'Dit is het portfolio dat je nu bekijkt: een volledige herbouw van mijn eerdere Laravel-portfolio naar '
                'een beter onderhoudbaar platform. Het doel was niet alleen om de publieke site er beter uit te laten '
                'zien, maar ook om content makkelijker te beheren, back-uppen, seeden, vertalen en opnieuw op te '
                'bouwen wanneer het project verandert.',
  'description_markdown': '## Why I rebuilt it\n'
                          '\n'
                          'My older Laravel portfolio taught me a lot, but it also made one problem very clear: once '
                          'the content grows, managing it directly through code becomes annoying. For this version I '
                          'wanted a portfolio that felt more like a real platform than a static showcase.\n'
                          '\n'
                          'The project now combines a public portfolio, an admin CMS, media handling, backup/restore '
                          'flows, seeded content, multilingual fields, GitHub statistics, and a small assistant that '
                          'can answer questions based on indexed portfolio content.\n'
                          '\n'
                          '## Stack\n'
                          '\n'
                          '- Angular and TypeScript for the frontend\n'
                          '- Tailwind CSS for the UI\n'
                          '- FastAPI for the portfolio API and admin endpoints\n'
                          '- PostgreSQL with pgvector for structured data and retrieval support\n'
                          '- Redis for background jobs\n'
                          '- MinIO for uploaded media\n'
                          '- Docker Compose for local and server deployment\n'
                          '- Ollama-compatible AI services for local assistant and embedding workflows\n'
                          '\n'
                          '## What I focused on\n'
                          '\n'
                          'A big part of this project was turning the portfolio into something I can keep maintaining. '
                          'I added an admin area for editing projects, blog posts, skills, profile text, navigation, '
                          'media files, and assistant context. I also worked on backup exports and deterministic seed '
                          'data so I can rebuild the environment without losing the content I already wrote.\n'
                          '\n'
                          'The public side focuses on a cleaner browsing experience: project pages, blog pages, stats, '
                          'contact flows, language switching, and responsive layouts that work on smaller screens.\n'
                          '\n'
                          '## What I learned\n'
                          '\n'
                          'This project pushed me to think beyond a nice homepage. I had to connect frontend design, '
                          'backend APIs, database migrations, object storage, authentication, media URLs, background '
                          'workers, and deployment concerns into one system. It also helped me understand why stable '
                          'seed data and backup workflows matter so much when a project is still changing quickly.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'The main lesson is that a portfolio can also be a software project in itself. It gives me a '
                          'place to show my work, but it also keeps forcing me to improve how I structure real '
                          'applications.',
  'description_markdown_nl': '## Waarom ik het opnieuw bouwde\n'
                             '\n'
                             'Mijn oudere Laravel-portfolio heeft me veel geleerd, maar het maakte ook één probleem '
                             'duidelijk: zodra er meer content bijkomt, wordt het vervelend om alles rechtstreeks via '
                             'code te beheren. Voor deze versie wilde ik een portfolio dat meer aanvoelt als een echt '
                             'platform dan als een statische showcase.\n'
                             '\n'
                             'Het project combineert nu een publieke portfolio-site, een admin-CMS, mediabeheer, '
                             'backup- en restore-flows, seedbare content, meertalige velden, GitHub-statistieken en '
                             'een kleine assistent die vragen kan beantwoorden op basis van geïndexeerde '
                             'portfolio-inhoud.\n'
                             '\n'
                             '## Stack\n'
                             '\n'
                             '- Angular en TypeScript voor de frontend\n'
                             '- Tailwind CSS voor de UI\n'
                             '- FastAPI voor de portfolio-API en admin-endpoints\n'
                             '- PostgreSQL met pgvector voor gestructureerde data en retrieval-ondersteuning\n'
                             '- Redis voor achtergrondtaken\n'
                             '- MinIO voor geüploade media\n'
                             '- Docker Compose voor lokale en serverdeployment\n'
                             '- Ollama-compatibele AI-services voor lokale assistent- en embeddingflows\n'
                             '\n'
                             '## Waar ik op focuste\n'
                             '\n'
                             'Een groot deel van dit project draaide rond het onderhoudbaar maken van mijn portfolio. '
                             'Ik voegde een adminomgeving toe om projecten, blogposts, skills, profieltekst, '
                             'navigatie, media en assistant-context te beheren. Daarnaast werkte ik aan backup-exports '
                             'en deterministische seed data, zodat ik de omgeving opnieuw kan opbouwen zonder de '
                             'content te verliezen die ik al geschreven heb.\n'
                             '\n'
                             "De publieke kant focust op een duidelijke gebruikerservaring: projectpagina's, "
                             "blogpagina's, statistieken, contactflows, taalwissels en responsive layouts die ook op "
                             'kleinere schermen goed werken.\n'
                             '\n'
                             '## Wat ik geleerd heb\n'
                             '\n'
                             'Dit project dwong me om verder te denken dan een mooie homepage. Ik moest '
                             "frontenddesign, backend-API's, databasemigraties, object storage, authenticatie, "
                             "media-URL's, background workers en deployment in één systeem laten samenwerken. Het "
                             'heeft me ook laten zien waarom stabiele seed data en backup-workflows zo belangrijk zijn '
                             'wanneer een project nog snel verandert.\n'
                             '\n'
                             '## Reflectie\n'
                             '\n'
                             'De belangrijkste les is dat een portfolio ook zelf een softwareproject kan zijn. Het '
                             'geeft me een plek om mijn werk te tonen, maar het dwingt me tegelijk om beter te worden '
                             'in het structureren van echte applicaties.',
  'cover_image_file_id': '8ca95658-9e66-4c74-b5fa-d698770d3142',
  'github_url': 'https://github.com/Alex-v-p/personal-portfolio',
  'github_repo_owner': 'Alex-v-p',
  'github_repo_name': 'personal-portfolio',
  'demo_url': 'https://www.alex-vp.com',
  'company_name': 'Personal Project',
  'started_on': '2026-04-04',
  'ended_on': '2026-05-20',
  'duration_label': '2 Month',
  'duration_label_nl': '2 Maanden',
  'status': 'In progress',
  'status_nl': 'In uitvoering',
  'state': 'published',
  'is_featured': False,
  'sort_order': 0,
  'published_at': '2026-04-28T13:40:00+00:00',
  'created_at': '2026-04-28T13:40:41.921471+00:00',
  'updated_at': '2026-04-28T17:05:00+00:00'},
 {'id': '0e67658b-7811-4d72-9e9c-ac5250a46261',
  'slug': 'kraggleml-prediction',
  'title': 'Kraggle Placement Prediction Competition',
  'title_nl': 'Kraggle Plaatsingsvoorspelling Competitie',
  'teaser': 'A Kaggle-style school competition where I worked on predicting student placement outcomes from cleaned '
            'tabular data.',
  'teaser_nl': 'Een Kaggle-achtige schoolcompetitie waarin ik studentplaatsingen voorspelde op basis van opgeschoonde '
               'tabeldata.',
  'summary': 'This machine learning project focused on predicting whether a student would be placed or not placed '
             'based on educational and profile data. The work was mainly about careful preprocessing, comparing '
             'models, and learning how small data-cleaning decisions can influence a final prediction score.',
  'summary_nl': 'Dit machinelearningproject draaide om het voorspellen of een student wel of niet geplaatst zou worden '
                'op basis van onderwijs- en profieldata. Het werk bestond vooral uit zorgvuldige preprocessing, '
                'modellen vergelijken en leren hoe kleine keuzes in datacleaning de uiteindelijke predictiescore '
                'kunnen beïnvloeden.',
  'description_markdown': '## Project overview\n'
                          '\n'
                          'Kraggle was a school competition inspired by Kaggle. The goal was to build the best '
                          'possible placement prediction model using a dataset with student information such as '
                          'education percentages, work experience, specialisation, and MBA percentage.\n'
                          '\n'
                          'The dataset contained both placed and not placed students, which made the project a useful '
                          'exercise in binary classification and evaluation.\n'
                          '\n'
                          '## My approach\n'
                          '\n'
                          'I started by cleaning the data so the models could use it reliably. That included handling '
                          'missing values, encoding categorical variables, converting numeric columns to the right '
                          'data types, and checking the target distribution. From there I compared different machine '
                          'learning models and looked at how their results changed depending on the preprocessing '
                          'choices.\n'
                          '\n'
                          'The cover image for this project comes from that comparison step, where the goal was to '
                          'quickly see which model families were worth improving further.\n'
                          '\n'
                          '## Tools and techniques\n'
                          '\n'
                          '- Python\n'
                          '- Pandas\n'
                          '- Scikit-learn\n'
                          '- Data cleaning and preprocessing\n'
                          '- Classification models\n'
                          '- Model comparison and evaluation\n'
                          '\n'
                          '## What I learned\n'
                          '\n'
                          'The most useful lesson was that machine learning results depend heavily on the quality of '
                          'the preparation work. A stronger model does not help much if the input data is inconsistent '
                          'or if categorical values are handled poorly.\n'
                          '\n'
                          'This project also made the workflow around experiments feel more concrete: clean the data, '
                          'build a baseline, compare results, make one change at a time, and keep track of what '
                          'actually improved the prediction.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'Even though this was a competition, the biggest value for me was not only the score. It '
                          'helped me become more comfortable with the practical machine learning workflow and with '
                          'explaining why one model or preprocessing choice performs better than another.',
  'description_markdown_nl': '## Projectoverzicht\n'
                             '\n'
                             'Kraggle was een schoolcompetitie geïnspireerd door Kaggle. Het doel was om een zo goed '
                             'mogelijk model te bouwen dat studentplaatsingen voorspelt op basis van een dataset met '
                             'studentinformatie zoals opleidingspercentages, werkervaring, specialisatie en '
                             'MBA-percentage.\n'
                             '\n'
                             'De dataset bevatte zowel geplaatste als niet-geplaatste studenten, waardoor het project '
                             'een nuttige oefening was in binaire classificatie en evaluatie.\n'
                             '\n'
                             '## Mijn aanpak\n'
                             '\n'
                             'Ik begon met het opschonen van de data zodat de modellen ermee konden werken op een '
                             'betrouwbare manier. Dat betekende onder andere ontbrekende waarden behandelen, '
                             'categorische variabelen encoden, numerieke kolommen naar de juiste datatypes omzetten en '
                             'de verdeling van de target controleren. Daarna vergeleek ik verschillende '
                             'machinelearningmodellen en keek ik hoe hun resultaten veranderden afhankelijk van de '
                             'preprocessingkeuzes.\n'
                             '\n'
                             'De coverafbeelding van dit project komt uit die vergelijkingsstap, waar het doel was om '
                             'snel te zien welke modelfamilies de moeite waard waren om verder te verbeteren.\n'
                             '\n'
                             '## Tools en technieken\n'
                             '\n'
                             '- Python\n'
                             '- Pandas\n'
                             '- Scikit-learn\n'
                             '- Datacleaning en preprocessing\n'
                             '- Classificatiemodellen\n'
                             '- Modelvergelijking en evaluatie\n'
                             '\n'
                             '## Wat ik geleerd heb\n'
                             '\n'
                             'De belangrijkste les was dat machinelearningresultaten sterk afhangen van de kwaliteit '
                             'van de voorbereiding. Een sterker model helpt niet veel als de inputdata inconsistent is '
                             'of als categorische waarden slecht behandeld worden.\n'
                             '\n'
                             'Dit project maakte de experimentele workflow ook concreter voor mij: data opschonen, een '
                             'baseline bouwen, resultaten vergelijken, telkens één wijziging maken en bijhouden wat de '
                             'voorspelling echt verbetert.\n'
                             '\n'
                             '## Reflectie\n'
                             '\n'
                             'Hoewel dit een competitie was, zat de grootste waarde voor mij niet alleen in de score. '
                             'Het project hielp me om comfortabeler te worden met de praktische '
                             'machinelearningworkflow en met het uitleggen waarom een model of preprocessingkeuze '
                             'beter werkt dan een andere.',
  'cover_image_file_id': 'ad9396a4-3dc9-4c4b-bbd4-52527aee63ea',
  'github_url': 'https://github.com/tijskanters/Ai-ACS02-kraggle',
  'github_repo_owner': 'tijskanters',
  'github_repo_name': 'Ai-ACS02-kraggle',
  'demo_url': None,
  'company_name': 'Kraggle Machinelearning competition',
  'started_on': '2025-03-01',
  'ended_on': '2025-03-25',
  'duration_label': '1 Month',
  'duration_label_nl': '1 Maand',
  'status': 'Completed',
  'status_nl': 'Afgerond',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 0,
  'published_at': '2026-04-28T13:33:00+00:00',
  'created_at': '2026-04-28T13:33:37.483825+00:00',
  'updated_at': '2026-04-28T17:05:00+00:00'},
 {'id': '0543c00e-2e28-4310-9a2c-9f0be751c2d7',
  'slug': 'ceriq-assistant',
  'title': 'CerIQ Email Assistant',
  'title_nl': 'CerIQ Email Assistant',
  'teaser': 'An AI-assisted email and support tool built for CERcuits to help engineers draft grounded customer '
            'responses faster.',
  'teaser_nl': 'Een AI-ondersteunde email- en supporttool voor CERcuits, gebouwd om engineers sneller onderbouwde '
               'klantantwoorden te laten opstellen.',
  'summary': 'This team project delivered a proof of concept for CERcuits: an internal AI assistant that generates '
             'draft replies to customer emails using company documentation as context. The system kept humans in '
             'control while adding RAG, a chatbot, document management, user management, feedback, and '
             'security-focused deployment choices.',
  'summary_nl': 'Dit teamproject leverde een proof of concept op voor CERcuits: een interne AI-assistent die '
                'conceptantwoorden op klantmails genereert met bedrijfsdocumentatie als context. Het systeem liet de '
                'controle bij de gebruiker, maar voegde RAG, een chatbot, documentbeheer, gebruikersbeheer, feedback '
                'en securitygerichte deploymentkeuzes toe.',
  'description_markdown': '## Project context\n'
                          '\n'
                          'CERcuits wanted to reduce the manual workload around incoming customer emails and technical '
                          'support questions. Their engineers still needed to stay in control, but the first draft and '
                          'supporting context could be prepared by an AI system.\n'
                          '\n'
                          'As part of a team project, we built a proof of concept that helps generate context-aware '
                          'draft responses instead of sending anything automatically.\n'
                          '\n'
                          '## Main features\n'
                          '\n'
                          '- Email draft generation grounded in company documents\n'
                          '- Retrieval-Augmented Generation using an internal knowledge base\n'
                          '- A chatbot for follow-up questions and transparency around generated answers\n'
                          '- Document upload and ingestion flows for the knowledge base\n'
                          '- User management and role-based access control\n'
                          '- AI usage insights and feedback collection\n'
                          '- Security measures around authentication, rate limiting, scanning, and deployment\n'
                          '\n'
                          '## Technical approach\n'
                          '\n'
                          'The system was designed around a modular AI pipeline. Uploaded company documents are '
                          'processed into a searchable knowledge base, and the assistant retrieves relevant context '
                          'before generating an answer. This makes the output easier to review because users can '
                          'understand which information influenced the draft.\n'
                          '\n'
                          'The project also focused strongly on privacy and control. The assistant was intended for '
                          'internal use, with human review as a requirement, not as a replacement for the engineer.\n'
                          '\n'
                          '## What I learned\n'
                          '\n'
                          'This project made the difference between a simple chatbot demo and a usable business tool '
                          'very clear. The difficult part was not just calling an AI model; it was managing context, '
                          'access, security, feedback, and user trust.\n'
                          '\n'
                          'It also taught me how important it is to document architecture and handover decisions when '
                          'a project may be continued by someone else later.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'The most valuable part of CerIQ was working on AI in a setting where reliability matters. '
                          'The assistant had to be helpful, but also transparent, limited in scope, and safe enough '
                          'for real support workflows.',
  'description_markdown_nl': '## Projectcontext\n'
                             '\n'
                             'CERcuits wilde de manuele workload rond inkomende klantmails en technische supportvragen '
                             'verminderen. De engineers moesten zelf controle houden, maar de eerste versie van een '
                             'antwoord en de ondersteunende context konden voorbereid worden door een AI-systeem.\n'
                             '\n'
                             'Als deel van een teamproject bouwden we een proof of concept dat helpt om contextbewuste '
                             'conceptantwoorden te genereren, zonder automatisch mails te versturen.\n'
                             '\n'
                             '## Belangrijkste features\n'
                             '\n'
                             '- Conceptantwoorden op emails, onderbouwd met bedrijfsdocumentatie\n'
                             '- Retrieval-Augmented Generation op basis van een interne knowledge base\n'
                             '- Een chatbot voor vervolgvragen en transparantie rond gegenereerde antwoorden\n'
                             '- Documentupload en ingestion-flows voor de knowledge base\n'
                             '- Gebruikersbeheer en role-based access control\n'
                             '- AI-gebruiksinzichten en feedbackverzameling\n'
                             '- Securitymaatregelen rond authenticatie, rate limiting, scanning en deployment\n'
                             '\n'
                             '## Technische aanpak\n'
                             '\n'
                             'Het systeem werd ontworpen rond een modulaire AI-pipeline. Geüploade bedrijfsdocumenten '
                             'worden verwerkt tot een doorzoekbare knowledge base, waarna de assistent relevante '
                             'context ophaalt voordat hij een antwoord genereert. Daardoor is de output makkelijker te '
                             'controleren, omdat gebruikers beter begrijpen welke informatie het conceptantwoord heeft '
                             'beïnvloed.\n'
                             '\n'
                             'Het project focuste ook sterk op privacy en controle. De assistent was bedoeld voor '
                             'intern gebruik, met menselijke review als vereiste, niet als vervanging van de '
                             'engineer.\n'
                             '\n'
                             '## Wat ik geleerd heb\n'
                             '\n'
                             'Dit project maakte het verschil tussen een simpele chatbotdemo en een bruikbare '
                             'businesstool heel duidelijk. Het moeilijke deel was niet alleen een AI-model aanroepen, '
                             'maar ook context, toegang, security, feedback en gebruikersvertrouwen beheren.\n'
                             '\n'
                             'Het leerde me ook hoe belangrijk architectuurdocumentatie en duidelijke overdracht zijn '
                             'wanneer een project later door iemand anders verdergezet kan worden.\n'
                             '\n'
                             '## Reflectie\n'
                             '\n'
                             'Het meest waardevolle aan CerIQ was werken aan AI in een context waar betrouwbaarheid '
                             'belangrijk is. De assistent moest nuttig zijn, maar ook transparant, afgebakend en '
                             'veilig genoeg voor echte supportworkflows.',
  'cover_image_file_id': 'a6862186-5c12-4e35-a381-45c00bc2b80c',
  'github_url': None,
  'github_repo_owner': None,
  'github_repo_name': None,
  'demo_url': 'https://www.youtube.com/watch?v=GNbZ3ArOCOI',
  'company_name': 'CERcuits',
  'started_on': '2026-01-12',
  'ended_on': '2026-01-30',
  'duration_label': '3 Weeks',
  'duration_label_nl': '3 weken',
  'status': 'Completed',
  'status_nl': 'Afgerond',
  'state': 'completed',
  'is_featured': False,
  'sort_order': 0,
  'published_at': '2026-04-28T15:24:00+00:00',
  'created_at': '2026-04-28T15:24:26.190678+00:00',
  'updated_at': '2026-04-28T17:05:00+00:00'},
 {'id': '9362fec8-67df-4754-a820-c2c9429110df',
  'slug': 'appies-bricks',
  'title': 'Appies Legobib',
  'title_nl': 'Appies Legobib',
  'teaser': 'An online Lego library portal for hospitalized children, with ordering, inventory, returns, and '
            'sanitization flows.',
  'teaser_nl': 'Een online Legobib-portaal voor gehospitaliseerde kinderen, met bestellen, inventaris, retouren en '
               'ontsmettingsflows.',
  'summary': 'Appies Legobib was a team project for Bricks and More focused on making a small Lego library easier to '
             'operate in a hospital context. Children could request Lego sets, while the system supported the '
             'practical workflow behind inventory, delivery, return, and sanitization.',
  'summary_nl': 'Appies Legobib was een teamproject voor Bricks and More, gericht op het makkelijker beheren van een '
                'kleine Legobib in een ziekenhuiscontext. Kinderen konden Lego-sets aanvragen, terwijl het systeem de '
                'praktische workflow rond voorraad, levering, retour en ontsmetting ondersteunde.',
  'description_markdown': '## Project overview\n'
                          '\n'
                          'Appies Legobib was built around a simple idea: hospitalized children should be able to '
                          'request Lego sets in an accessible way, while volunteers or staff can still keep the '
                          'library organized behind the scenes.\n'
                          '\n'
                          'The application was not only about placing an order. It also needed to support what happens '
                          'after that: keeping track of sets, knowing which sets are available, following the return '
                          'flow, and making sure returned sets go through sanitization before being used again.\n'
                          '\n'
                          '## What the application supports\n'
                          '\n'
                          '- Browsing and requesting Lego sets\n'
                          '- Tracking which sets are available or in use\n'
                          '- Managing returns after a set comes back\n'
                          '- Supporting a sanitization step before a set is available again\n'
                          '- Giving the organization a clearer view of the library workflow\n'
                          '\n'
                          '## Stack and workflow\n'
                          '\n'
                          'The project used Angular and Tailwind CSS on the frontend, with a C#/.NET-style backend '
                          'approach and Azure-related deployment thinking. The work was done as a team project, so '
                          'communication, planning, and scope control were as important as the technical '
                          'implementation.\n'
                          '\n'
                          'The cover image shows our team pitching the project, which fits the project well because a '
                          'lot of the value came from explaining the concept clearly to others.\n'
                          '\n'
                          '## What I learned\n'
                          '\n'
                          'This project made me think more about software for a sensitive real-world environment. The '
                          'interface had to stay simple, but the process behind it still needed enough structure to '
                          'avoid confusion around inventory and hygiene.\n'
                          '\n'
                          'It also showed how important it is to turn a warm idea into a practical workflow. A good '
                          'concept only becomes useful when the boring operational steps are also handled properly.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'Appies Legobib was valuable because it combined technical work with a more human goal. It '
                          'reminded me that even a small web application can make a process feel easier for the people '
                          'using it.',
  'description_markdown_nl': '## Projectoverzicht\n'
                             '\n'
                             'Appies Legobib werd gebouwd rond een eenvoudig idee: gehospitaliseerde kinderen moeten '
                             'op een toegankelijke manier Lego-sets kunnen aanvragen, terwijl vrijwilligers of '
                             'medewerkers de bibliotheek achter de schermen georganiseerd kunnen houden.\n'
                             '\n'
                             'De applicatie ging niet alleen over een bestelling plaatsen. Ze moest ook ondersteunen '
                             'wat daarna gebeurt: sets opvolgen, weten welke sets beschikbaar zijn, de retourflow '
                             'beheren en zorgen dat teruggebrachte sets eerst ontsmet worden voordat ze opnieuw '
                             'beschikbaar zijn.\n'
                             '\n'
                             '## Wat de applicatie ondersteunt\n'
                             '\n'
                             '- Lego-sets bekijken en aanvragen\n'
                             '- Bijhouden welke sets beschikbaar of in gebruik zijn\n'
                             '- Retouren beheren wanneer een set terugkomt\n'
                             '- Een ontsmettingsstap ondersteunen voordat een set opnieuw beschikbaar is\n'
                             '- De organisatie een duidelijker beeld geven van de workflow rond de bibliotheek\n'
                             '\n'
                             '## Stack en werkwijze\n'
                             '\n'
                             'Het project gebruikte Angular en Tailwind CSS aan de frontend, met een C#/.NET-achtige '
                             'backendaanpak en Azure-gerichte deploymentkeuzes. Het werk gebeurde als teamproject, dus '
                             'communicatie, planning en scopecontrole waren even belangrijk als de technische '
                             'implementatie.\n'
                             '\n'
                             'De coverafbeelding toont onze teampitch, wat goed bij het project past omdat een groot '
                             'deel van de waarde ook zat in het helder uitleggen van het concept.\n'
                             '\n'
                             '## Wat ik geleerd heb\n'
                             '\n'
                             'Dit project liet me meer nadenken over software voor een gevoelige realistische '
                             'omgeving. De interface moest eenvoudig blijven, maar het proces erachter had genoeg '
                             'structuur nodig om verwarring rond voorraad en hygiëne te vermijden.\n'
                             '\n'
                             'Het toonde ook hoe belangrijk het is om een warm idee om te zetten naar een praktische '
                             'workflow. Een goed concept wordt pas echt bruikbaar wanneer ook de saaie operationele '
                             'stappen goed zijn uitgewerkt.\n'
                             '\n'
                             '## Reflectie\n'
                             '\n'
                             'Appies Legobib was waardevol omdat het technisch werk combineerde met een menselijker '
                             'doel. Het herinnerde me eraan dat zelfs een kleine webapplicatie een proces makkelijker '
                             'kan maken voor de mensen die ermee werken.',
  'cover_image_file_id': 'cc257aca-f1fc-402c-aae6-a12998c587dc',
  'github_url': None,
  'github_repo_owner': None,
  'github_repo_name': None,
  'demo_url': None,
  'company_name': 'Bricks and More',
  'started_on': '2025-10-01',
  'ended_on': '2025-12-11',
  'duration_label': '3 Months',
  'duration_label_nl': '3 Maanden',
  'status': 'Completed',
  'status_nl': 'Afgerond',
  'state': 'published',
  'is_featured': False,
  'sort_order': 0,
  'published_at': '2026-04-28T13:46:00+00:00',
  'created_at': '2026-04-28T13:46:35.922559+00:00',
  'updated_at': '2026-04-28T17:05:00+00:00'},
 {'id': '483f7898-9bf8-4899-9998-5b7407c73c72',
  'slug': 'mobicare-llmguidance',
  'title': 'Medical Cardiovascular LLM Guidance',
  'title_nl': 'Medische cardiovasculaire LLM-begeleiding',
  'teaser': 'A medical guidance prototype that uses guideline documents and a local LLM pipeline to support '
            'cardiovascular medication decisions.',
  'teaser_nl': 'Een medisch guidance-prototype dat richtlijndocumenten en een lokale LLM-pipeline gebruikt ter '
               'ondersteuning van cardiovasculaire medicatiebeslissingen.',
  'summary': 'This internship project focuses on an inference system for medical professionals working with '
             'cardiovascular medication guidance. The application is designed around a grounded, human-in-the-loop '
             'workflow: retrieve relevant guideline context, run the inference pipeline, and return structured support '
             'that can be reviewed by a professional.',
  'summary_nl': 'Dit stageproject focust op een inferentiesysteem voor medische professionals die werken met '
                'cardiovasculaire medicatiebegeleiding. De applicatie is opgebouwd rond een onderbouwde '
                'human-in-the-loop workflow: relevante richtlijncontext ophalen, de inferentiepipeline uitvoeren en '
                'gestructureerde ondersteuning teruggeven die door een professional gecontroleerd kan worden.',
  'description_markdown': '## Project context\n'
                          '\n'
                          'This project was developed during my internship with MobiLab & Care. The goal was to '
                          'explore how an LLM-based inference system could support medical professionals with '
                          'cardiovascular medication guidance while staying grounded in guideline documentation.\n'
                          '\n'
                          'Because the domain is medical, the system is not designed to make autonomous decisions. The '
                          'focus is on supporting professionals with structured, traceable output that can be '
                          'reviewed.\n'
                          '\n'
                          '## Architecture\n'
                          '\n'
                          'The architecture is built around a containerized inference system. A dashboard can call the '
                          'API, the API validates and routes requests, and a worker coordinates the retrieval and '
                          'inference flow.\n'
                          '\n'
                          'The supporting services include:\n'
                          '\n'
                          '- FastAPI and Pydantic for request handling and validation\n'
                          '- Qdrant for vector storage and similarity search\n'
                          '- MinIO for storing guideline documents and longer-running job artefacts\n'
                          '- Ollama for local LLM and embedding runtime\n'
                          '- Redis for asynchronous job handling\n'
                          '- Docker Compose as the base deployment setup\n'
                          '\n'
                          '## What I focused on\n'
                          '\n'
                          'The interesting part of this project is the boundary between AI output and reliable '
                          'software engineering. I worked with concepts such as document ingestion, vector search, API '
                          'boundaries, asynchronous jobs, and local inference infrastructure.\n'
                          '\n'
                          'A lot of attention also goes to making the system understandable. In a medical setting, it '
                          'is not enough for the model to produce an answer; the surrounding application has to make '
                          'the flow clear, limited, and reviewable.\n'
                          '\n'
                          '## What I learned\n'
                          '\n'
                          'This project helped me see why AI systems need more than a prompt and a model. The useful '
                          'work sits in the surrounding architecture: how documents are stored, how context is '
                          'retrieved, how requests are validated, how jobs are tracked, and how results are returned '
                          'safely.\n'
                          '\n'
                          'It also gave me more practical experience with containerized services, retrieval pipelines, '
                          'and the trade-offs between local control and system complexity.\n'
                          '\n'
                          '## Reflection\n'
                          '\n'
                          'The main takeaway is that AI in a professional domain has to be designed carefully. The '
                          'value is not in pretending the model is always right, but in building a workflow where the '
                          'model can support a human expert with relevant context and clear limitations.',
  'description_markdown_nl': '## Projectcontext\n'
                             '\n'
                             'Dit project werd ontwikkeld tijdens mijn stage bij MobiLab & Care. Het doel was om te '
                             'onderzoeken hoe een LLM-gebaseerd inferentiesysteem medische professionals kan '
                             'ondersteunen bij cardiovasculaire medicatiebegeleiding, terwijl de antwoorden gebaseerd '
                             'blijven op richtlijndocumentatie.\n'
                             '\n'
                             'Omdat het domein medisch is, is het systeem niet bedoeld om autonome beslissingen te '
                             'nemen. De focus ligt op het ondersteunen van professionals met gestructureerde en '
                             'traceerbare output die gecontroleerd kan worden.\n'
                             '\n'
                             '## Architectuur\n'
                             '\n'
                             'De architectuur is opgebouwd rond een gecontaineriseerd inferentiesysteem. Een dashboard '
                             'kan de API aanroepen, de API valideert en routeert requests, en een worker coördineert '
                             'de retrieval- en inferentieflow.\n'
                             '\n'
                             'De ondersteunende services zijn onder andere:\n'
                             '\n'
                             '- FastAPI en Pydantic voor request handling en validatie\n'
                             '- Qdrant voor vectoropslag en similarity search\n'
                             '- MinIO voor het bewaren van richtlijndocumenten en jobartefacten\n'
                             '- Ollama voor lokale LLM- en embeddingruntime\n'
                             '- Redis voor asynchrone jobverwerking\n'
                             '- Docker Compose als basis voor de deploymentsetup\n'
                             '\n'
                             '## Waar ik op focuste\n'
                             '\n'
                             'Het interessante aan dit project is de grens tussen AI-output en betrouwbare software '
                             'engineering. Ik werkte met concepten zoals document ingestion, vector search, '
                             'API-grenzen, asynchrone jobs en lokale inference-infrastructuur.\n'
                             '\n'
                             'Er gaat ook veel aandacht naar begrijpelijkheid. In een medische context is het niet '
                             'genoeg dat een model een antwoord produceert; de applicatie eromheen moet de flow '
                             'duidelijk, afgebakend en controleerbaar maken.\n'
                             '\n'
                             '## Wat ik geleerd heb\n'
                             '\n'
                             'Dit project liet me zien waarom AI-systemen meer nodig hebben dan alleen een prompt en '
                             'een model. Het nuttige werk zit in de omliggende architectuur: hoe documenten worden '
                             'opgeslagen, hoe context wordt opgehaald, hoe requests worden gevalideerd, hoe jobs '
                             'worden opgevolgd en hoe resultaten veilig worden teruggegeven.\n'
                             '\n'
                             'Het gaf me ook meer praktische ervaring met gecontaineriseerde services, '
                             'retrieval-pipelines en de afwegingen tussen lokale controle en systeemcomplexiteit.\n'
                             '\n'
                             '## Reflectie\n'
                             '\n'
                             'De belangrijkste les is dat AI in een professioneel domein voorzichtig ontworpen moet '
                             'worden. De waarde zit niet in doen alsof het model altijd gelijk heeft, maar in een '
                             'workflow bouwen waarin het model een menselijke expert ondersteunt met relevante context '
                             'en duidelijke beperkingen.',
  'cover_image_file_id': '0a9e43e7-24e3-5065-8d29-d0d20d1647dd',
  'github_url': 'https://github.com/Alex-v-p/mobicare-LLMGuidance',
  'github_repo_owner': 'Alex-v-p',
  'github_repo_name': 'mobicare-LLMGuidance',
  'demo_url': None,
  'company_name': 'Mobilab & Care',
  'started_on': '2026-02-23',
  'ended_on': None,
  'duration_label': '4 months',
  'duration_label_nl': '4 maanden',
  'status': 'In progress',
  'status_nl': 'In uitvoering',
  'state': 'published',
  'is_featured': False,
  'sort_order': 0,
  'published_at': '2026-04-28T13:19:00+00:00',
  'created_at': '2026-04-28T13:19:42.690019+00:00',
  'updated_at': '2026-04-28T17:05:00+00:00'}]

BLOG_POST_ROWS = [{'id': '155286fe-5710-53c7-be2d-6088b3bfa71c',
  'slug': 'my-homelab',
  'title': 'My Homelab',
  'title_nl': 'Mijn HomeLab',
  'excerpt': 'A look at the homelab setup I use to learn more about storage, hosting, networking, and running my own '
             'tools.',
  'excerpt_nl': 'Een blik in de wijksetup waar ik gebruik van heb om meer te leren over opslag, hosting, netwerken en '
                'eigen tools te runnen.',
  'content_markdown': '# My Homelab\n'
                      '\n'
                      '\n'
                      'At first my homelab consisted of only my trueNAS server. But since then its expanded '
                      'drastically. My current homelab has slowly grown from a few experiments into my own personal '
                      'small-scale infrastructure setup. It is not just one server running random containers anymore. '
                      'My infrastructure is clearly seperated based on responsilbity between containers and virtual '
                      'machines, public traffic is controlled, and network trafic is consistently monitored. Making it '
                      'easy to deploy project for my own personal and public use.\n'
                      '\n'
                      'The core idea behind its construction is simple: I wanted a place that felt like a small '
                      'personal datacenter. It should host my own applications, support experiments, run game servers, '
                      'provide storage, and give me a safe place to learn infrastructure, DevOps, networking, '
                      'monitoring, and AI deployment.\n'
                      '\n'
                      '![Diagram of the homelab setup](http://localhost:19000/portfolio/blog/my-homelab/cover.png)\n'
                      '\n'
                      '\n'
                      '## The Main Architecture\n'
                      '\n'
                      'The setup is built around a Proxmox server, which runs several virtual machines. Each VM has a '
                      'specific role instead of putting everything into one large system.\n'
                      '\n'
                      'At the edge of the network, my router forwards only the traffic that really needs to enter the '
                      'homelab. From there, traffic is split depending on the use case. Public web traffic goes '
                      'through an edge VM, game server traffic goes directly to the game server VM (due to latency '
                      'issues), and internal services communicate over the local network.\n'
                      '\n'
                      'A separate TrueNAS server handles storage. This keeps my storage layer separated from the '
                      'compute layer, which makes the setup cleaner and easier to reason about.\n'
                      '\n'
                      '### VM1: Edge\n'
                      '\n'
                      'The edge VM is the main entry point for most web-based services.\n'
                      '\n'
                      'It runs:\n'
                      '1. - Cloudflare Tunnel\n'
                      '2. - Nginx Proxy Manager\n'
                      '3. - WireGuard\n'
                      '\n'
                      'This VM is responsible for getting traffic from the outside world to the correct internal '
                      'service. Instead of exposing every application directly, I can route traffic through Cloudflare '
                      'and Nginx Proxy Manager.\n'
                      '\n'
                      'Cloudflare Tunnel is useful because it allows some services to be reachable without directly '
                      'opening a bunch of ports on my router. Nginx Proxy Manager then handles routing based on '
                      'domains and subdomains. For example, one subdomain can point to a personal app, while another '
                      'one can point to a project running on a different VM.\n'
                      '\n'
                      'WireGuard is also running here so I can securely connect back into my home network when I am '
                      'away. This is useful when I want to access internal dashboards, administration panels, or '
                      'services that should not be publicly available.\n'
                      '\n'
                      'In short, this VM is the controlled doorway into the homelab.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '### VM2: GitHub Runner\n'
                      '\n'
                      'The second VM is dedicated to deployments.\n'
                      '\n'
                      'This VM runs a GitHub Actions runner. The idea is that my projects can be built and deployed '
                      'automatically from GitHub into my internal app VM.\n'
                      '\n'
                      'This keeps the deployment process separate from the apps themselves. Instead of manually SSHing '
                      'into the app server every time I want to update a project, I can push changes to GitHub and let '
                      'the runner handle the deployment.\n'
                      '\n'
                      'The runner communicates with the app VM and performs the deployment steps there. This setup is '
                      'useful because it feels closer to how real-world CI/CD pipelines work.  \n'
                      '\n'
                      'Although there is one minor downside, which is that the runner is only available in my own '
                      'GitHub organization due to security reasons. So I still have to work with 2 separate repos for '
                      'deploy-able projects: 1 to develop in which is publicly viewable, and a second one which is '
                      'private and handled deployment.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '### VM3: Apps\n'
                      '\n'
                      'The apps VM is where my own hosted projects live.\n'
                      '\n'
                      'This includes projects such as:\n'
                      '- Portfolio platform\n'
                      '- Web applications\n'
                      '- APIs\n'
                      '- Databases related to those apps\n'
                      '- Supporting services like media storage connections\n'
                      '\n'
                      'This VM receives traffic from the edge VM. For example, when someone visits one of my public '
                      'project domains, Cloudflare and Nginx Proxy Manager route the request to the correct '
                      'application running here.\n'
                      '\n'
                      'Some of these apps can also communicate with the AI VM when they need LLM functionality. That '
                      'means the apps VM does not need to run the AI model itself. It can simply send a request to the '
                      'AI service and receive a response.\n'
                      '\n'
                      'This separation keeps the apps VM focused on application hosting, while the AI VM handles the '
                      'heavy GPU-related workload.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '### VM4: AI\n'
                      '\n'
                      'The AI VM is used for local AI workloads.\n'
                      '\n'
                      'It currently runs vLLM and ollama, which allows other services in the homelab to make requests '
                      'to a locally hosted language model. This makes it possible to experiment with AI features '
                      'without relying fully on external APIs.\n'
                      '\n'
                      'The apps VM and personal apps VM can both query the AI VM for AI-related use cases. For '
                      'example, a web application can send a prompt to the AI service and use the response inside the '
                      'app.\n'
                      '\n'
                      'Keeping AI workloads on a dedicated VM is important because they can be resource-heavy. This '
                      'also makes it easier to manage GPU passthrough, memory usage, and model serving separately from '
                      'the rest of the infrastructure.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '### VM5: Game Servers\n'
                      '\n'
                      'The game server VM is separate from the web application side of the homelab.\n'
                      '\n'
                      'This VM hosts game servers, such as terraria, minecraft, or other games.\n'
                      '\n'
                      'Unlike the web apps, these services often need direct port forwarding from the router. Game '
                      'servers usually depend on specific ports and protocols, so their traffic path is different from '
                      'the normal Cloudflare/Nginx web routing. And alongside this, the additional latency of '
                      'rerouting the connection to other services first can often be detrimental in games where '
                      'response time is critical.\n'
                      '\n'
                      'By keeping game servers on their own VM, they are isolated from the rest of the infrastructure. '
                      'If a game server uses too many resources or needs a restart, it does not affect my hosted apps, '
                      'monitoring stack, or AI services.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '### VM6: Ops and Monitoring\n'
                      '\n'
                      'The ops VM is where I keep the observability side of the homelab.\n'
                      '\n'
                      'It runs:\n'
                      '\n'
                      '- Prometheus\n'
                      '- Grafana\n'
                      '- Loki\n'
                      '- Alertmanager\n'
                      '- Uptime Kuma\n'
                      '\n'
                      'This VM helps me understand what is happening across the whole environment.\n'
                      '\n'
                      'Prometheus collects metrics. Grafana visualizes them in dashboards. Loki is used for logs. '
                      'Alertmanager can be used to send alerts when something goes wrong. Uptime Kuma gives a simple '
                      'overview of whether services are online or offline.\n'
                      '\n'
                      'This is one of the most useful parts of the setup because once multiple services are running, '
                      'it becomes difficult to manually check everything. Monitoring gives me a central place to see '
                      'the health of my infrastructure.\n'
                      '\n'
                      'For example, I can monitor whether containers are running, whether a VM is reachable, how much '
                      'RAM or CPU is being used, and whether public services are responding correctly.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '### VM7: Personal Apps\n'
                      '\n'
                      'The personal apps VM is for services that are more private or personal.\n'
                      '\n'
                      'This can include things like:\n'
                      '\n'
                      '- Homepage dashboards\n'
                      '- Nextcloud\n'
                      '- Personal tools\n'
                      '- Internal-only applications\n'
                      '\n'
                      'This VM also receives traffic from the edge VM when needed. Some services may be public, but '
                      'others are only intended to be accessed through WireGuard.\n'
                      '\n'
                      'Like the apps VM, personal apps can also query the AI VM if I want to add AI-powered features '
                      'to private tools.\n'
                      '\n'
                      'This VM gives me a place to run software that is useful for daily life without mixing it with '
                      'public project deployments.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '### TrueNAS Server\n'
                      '\n'
                      'Storage is handled by a separate TrueNAS server.\n'
                      '\n'
                      'The TrueNAS server provides storage through SMB for my windows machines, and NFS for my linux '
                      'laptop and machines.\n'
                      '\n'
                      'This is where larger persistent storage can live. Instead of storing everything directly inside '
                      'each VM, the VMs can use network storage when appropriate.\n'
                      '\n'
                      'The main benefit of this separation is that Proxmox handles compute, while TrueNAS handles '
                      'storage. This makes the infrastructure more modular. If I need to change or rebuild a VM, the '
                      'data does not necessarily have to live inside that VM.\n'
                      '\n'
                      'It also makes backups, shares, and storage management easier to centralize.\n',
  'content_markdown_nl': '# My Homelab\n'
                         '\n'
                         '\n'
                         'At first my homelab consisted of only my trueNAS server. But since then its expanded '
                         'drastically. My current homelab has slowly grown from a few experiments into my own personal '
                         'small-scale infrastructure setup. It is not just one server running random containers '
                         'anymore. My infrastructure is clearly seperated based on responsilbility between containers '
                         'and virtual machines, public traffic is controlled, and network trafic is consistently '
                         'monitored. Making it easy to deploy project for my own personal and public use.\n'
                         '\n'
                         'The core idea behind its construction is simple: I wanted a place that felt like a small '
                         'personal datacenter. It should host my own applications, support experiments, run game '
                         'servers, provide storage, and give me a safe place to learn infrastructure, DevOps, '
                         'networking, monitoring, and AI deployment.\n'
                         '\n'
                         '![Diagram of the homelab setup](http://localhost:19000/portfolio/blog/my-homelab/cover.png)\n'
                         '\n'
                         '\n'
                         '## The Main Architecture\n'
                         '\n'
                         'The setup is built around a Proxmox server, which runs several virtual machines. Each VM has '
                         'a specific role instead of putting everything into one large system.\n'
                         '\n'
                         'At the edge of the network, my router forwards only the traffic that really needs to enter '
                         'the homelab. From there, traffic is split depending on the use case. Public web traffic goes '
                         'through an edge VM, game server traffic goes directly to the game server VM (due to latency '
                         'issues), and internal services communicate over the local network.A aparte TrueNAS server '
                         'beheert de opslag. Dit houdt mijn opslaglaag gescheiden van de berekeningslaag, wat maakt '
                         'het setup schoon en eenvoudiger om te begrijpen.\n'
                         '\n'
                         '### VM1: Edge\n'
                         '\n'
                         'De edge VM is de hoofdingang voor de meeste web-basisdiensten.\n'
                         '\n'
                         'Ze draait:\n'
                         '1. - Cloudflare Tunnel\n'
                         '2. - Nginx Proxy Manager\n'
                         '3. - WireGuard\n'
                         '\n'
                         'Deze VM is verantwoordelijk voor het krijgen van traffiek van buiten de wereld naar de '
                         'juiste interne dienst. In plaats van elke applicatie direct te openen, kan ik traffiek via '
                         'Cloudflare en Nginx Proxy Manager worden gerouteerd.\n'
                         '\n'
                         'Cloudflare Tunnel is nuttig omdat het toegankelijk maakt sommige diensten zonder direct een '
                         'hoop poorten op mijn router te openen. Nginx Proxy Manager handelt vervolgens gerouteerd op '
                         'basis van domeinen en subdomeinen. Bijvoorbeeld, een subdomein kan naar een persoonlijke app '
                         'wijzen, terwijl een ander subdomein naar een project op een andere VM wijst.\n'
                         '\n'
                         'WireGuard draait ook hier, zodat ik veilig terug kan verbinding maken met mijn thuisnetwerk '
                         'wanneer ik weg ben. Dit is nuttig wanneer ik naar binnen wilt toegang krijgen tot interne '
                         'dashboards, beheeringspanels of diensten die niet publiekelijk toegankelijk moeten zijn.\n'
                         '\n'
                         'In kort, is deze VM de beheerde ingang naar de homelab.\n'
                         '\n'
                         '---\n'
                         '\n'
                         '### VM2: GitHub Runner\n'
                         '\n'
                         'De tweede VM is speciaal voor de uitvoeringen.\n'
                         '\n'
                         'Deze VM draait een GitHub Actions runner. Het idee is dat mijn projects kunnen worden '
                         'geïmplementeerd en uitgevoerd automatisch van GitHub naar mijn interne app VM.\n'
                         '\n'
                         'Dit houdt de uitvoeringssessie apart van de applicaties zelf. In plaats van manueel SSH te '
                         'gaan naar de app-server elke keer als ik een project wil bijwerken, kan ik changes naar '
                         'GitHub pushen en laten laten dat de runner de uitvoeringen uitvoert.### VM3: Apps\n'
                         '\n'
                         'De runner communiceert met de app VM en uitvoert de deploy-stappen daar. Dit setup is nuttig '
                         'omdat het zich bijna lijkt op hoe echte CI/CD-pipelijnen werken.\n'
                         '\n'
                         'Hoewel er één kleine onverzakbare kant is, die is dat de runner alleen beschikbaar is in '
                         'mijn eigen GitHub-organisatie vanwege veiligheidsredenen. Dus ik moet nog steeds met twee '
                         'aparte repositories werken voor de uitgebreide projecten: 1 voor het ontwikkelen, dat '
                         'openbaar is, en een tweede dat privé is en de deploy wordt afhandeld.\n'
                         '\n'
                         '---\n'
                         '\n'
                         '### VM3: Apps\n'
                         '\n'
                         'De apps VM is waar mijn eigen gehostte projecten op liggen.\n'
                         '\n'
                         'Dit omvat projecten zoals:\n'
                         '- Portfolio platform\n'
                         '- Web-apps\n'
                         '- APIs\n'
                         '- Databases die bij die apps horen\n'
                         '- Bijzondere diensten zoals mediaopslagverbindingen\n'
                         '\n'
                         'Deze VM ontvangt verzoeken van de edge VM. Bijvoorbeeld, als iemand een van mijn publieke '
                         'projectdomains bezoekt, routeert Cloudflare en Nginx Proxy Manager de verzoek naar de juiste '
                         'applicatie die hier wordt gehost.\n'
                         '\n'
                         'Een aantal van deze apps kan ook met de AI VM communiceren wanneer ze LLM-functies nodig '
                         'hebben. Dit betekent dat de apps VM niet zelf de AI-model moet draaien. Ze kan gewoon een '
                         'verzoek sturen naar de AI-service en ontvangt een antwoord.\n'
                         '\n'
                         'Dit gescheidenheid houdt de apps VM gericht op de applicatiehosting, terwijl de AI VM de '
                         'gewichtige GPU-bewerkingen afhandelt.\n'
                         '\n'
                         '---\n'
                         '\n'
                         '### VM4: AI\n'
                         '\n'
                         'De AI VM wordt gebruikt voor lokale AI-bewerkingen.\n'
                         '\n'
                         'Het draait momenteel vLLM en ollama, wat toelaat andere diensten in de homelab om lokale '
                         'beschikbare taalmodellen te verzoeken. Dit maakt het mogelijk om AI-features te '
                         'experimenteren zonder volledig afhankelijk te zijn van externe APIs.### VM5: Game Servers\n'
                         '\n'
                         'De game server VM is gescheiden van de web-applicatiekant van de homelab.\n'
                         '\n'
                         'Dit VM bevat game servers, zoals Terraria, Minecraft of andere spelserveren.\n'
                         '\n'
                         'In tegenstelling tot de web-apps, deze diensten hebben vaak directe poortransfert vanuit het '
                         'router. Spelserveren hebben vaak specifieke poortjes en protokollen nodig, zodat hun '
                         'verkeerspad verschillend is van de normale Cloudflare/Nginx web-route. En bij dit, de extra '
                         'latencie van het verkeer naar andere diensten eerst te routeren kan vaak negatief zijn in '
                         'spelletjes waar reactietijd cruciaal is.\n'
                         '\n'
                         'Door spelserveren op hun eigen VM te houden, worden ze gescheiden van de rest van de '
                         'infrastructuur. Als een spelserver te veel resources nodig heeft of een herstart vereist, '
                         'heeft dit geen invloed op mijn gehoste apps, monitortakken of AI-diensten.\n'
                         '\n'
                         '---\n'
                         '\n'
                         '### VM6: Ops en Monitoring\n'
                         '\n'
                         'De ops VM is waar ik de observabiliteitskant van de homelab hou.\n'
                         '\n'
                         'Het draait:\n'
                         '\n'
                         '- Prometheus\n'
                         '- Grafana\n'
                         '- Loki\n'
                         '- Alertmanager\n'
                         '- Uptime Kuma\n'
                         '\n'
                         'Dit VM helpt me in te schatten wat er gebeurt over de hele omgeving.Entity type: blog-post\n'
                         'Field key: contentMarkdownNl\n'
                         '---\n'
                         'Prometheus collectt metrics. Grafana visualiseert ze in dashboards. Loki wordt gebruikt voor '
                         'logs. Alertmanager kan worden gebruikt om alerts te versturen wanneer iets fout gaat. Uptime '
                         'Kuma geeft een eenvoudige overzicht van of diensten online of offline zijn.\n'
                         '\n'
                         'Dit is een van de meest nuttige delen van de setup omdat als meerdere diensten draaiën, het '
                         'moeilijker wordt om alles zelf te controleren. Monitoring geeft me een centrale plek om de '
                         'gezondheid van mijn infrastructuur te zien.\n'
                         '\n'
                         'Bijvoorbeeld, kan ik controleren of containers draaiën, of een VM bereikbaar is, of hoeveel '
                         'RAM of CPU wordt gebruikt, en of publieke diensten correct reageren.\n'
                         '\n'
                         '---\n'
                         '\n'
                         '### VM7: Persoonlijke Apps\n'
                         '\n'
                         'De persoonlijke apps VM is voor diensten die meer privé of persoonlijker zijn.\n'
                         '\n'
                         'Dit kan omvatten:\n'
                         '\n'
                         '1. 1. Homepage dashboards\n'
                         '1. 2. Nextcloud\n'
                         '1. 3. Persoonlijke tools\n'
                         '1. 4. Internale toepassingen\n'
                         '\n'
                         'Deze VM ontvangt ook traffiek van de edge VM wanneer nodig. Sommige diensten kunnen publiek '
                         'zijn, maar anderen zijn alleen bedoeld om te worden toegesteld via WireGuard.\n'
                         '\n'
                         'Net zoals de apps VM, kunnen persoonlijke apps ook de AI VM kunnen queryen als ik '
                         'AI-gestuurd features wil toevoegen aan persoonlijke toepassingen.\n'
                         '\n'
                         'Dit VM geeft me een plek om software te draaien die nuttig is voor dagelijks leven zonder '
                         'het te mogen met publieke projectdeployments vermengen.\n'
                         '\n'
                         '---\n'
                         '\n'
                         '### TrueNAS Server\n'
                         '\n'
                         'Besturingssysteemopslag wordt door een apart TrueNAS server beheerd.\n'
                         '\n'
                         'De TrueNAS server biedt opslag via SMB voor mijn Windows-machines en via NFS voor mijn '
                         'Linux-laptop en machines.\n'
                         '\n'
                         'Hier is waar grotere persistente opslag kan leven. In plaats van alles rechtstreeks binnen '
                         'elke VM te storen, kunnen de VMs netwerkopslag gebruiken wanneer dat nuttig is.\n'
                         '\n'
                         'De belangrijkste voord van deze scheiding is dat Proxmox rekening houdt van de bereking, '
                         'terwijl TrueNAS rekening houdt van de opslag. Dit maakt de infrastructuur meer modulaire. '
                         'Als ik een VM moet veranderen of opnieuw bouwen, hoeft de data niet automatisch binnen die '
                         'VM te leven.\n'
                         '\n'
                         'Het maakt ook backups, delen en opslagbeheerderij eenvoudiger te centraliseren.',
  'cover_image_file_id': '9c662c12-71ac-5ba7-9439-c472b943615c',
  'cover_image_alt': "Diagram of Alex van Poppel's homelab setup",
  'cover_image_alt_nl': 'Diagram van de setup van Alex van Poppel thuislab',
  'reading_time_minutes': 5,
  'status': 'published',
  'is_featured': True,
  'seo_title': 'My Homelab | Alex van Poppel',
  'seo_title_nl': 'Mijn Homelab | Alex van Poppel',
  'seo_description': 'A casual walkthrough of the homelab setup I use to learn self-hosting, storage, networking, and '
                     'deployment.',
  'seo_description_nl': 'Een gedetailleerde rondleiding van mijn thuislab setup, waarin ik leren doe over zelfhosting, '
                        'opslag, netwerken en implementatie.',
  'published_at': '2026-04-10T09:00:00+00:00',
  'created_at': '2026-04-10T09:00:00+00:00',
  'updated_at': '2026-04-28T16:16:17.496136+00:00'},
 {'id': '02518413-212e-5fdd-80e5-caea952b2a68',
  'slug': 'mobilab-internship',
  'title': 'MobiLab Internship',
  'title_nl': 'MobiLab-stage',
  'excerpt': 'A reflection on building a medical LLM inference system during my internship and why AI in professional '
             'domains needs clear boundaries.',
  'excerpt_nl': 'Een reflectie over het bouwen van een medisch LLM-inferentiesysteem tijdens mijn stage en waarom AI '
                'in professionele domeinen duidelijke grenzen nodig heeft.',
  'content_markdown': '# MobiLab Internship\n'
                      '\n'
                      'During my internship at MobiLab & Care, I worked on a medical guidance prototype around '
                      'cardiovascular medication. The project was not about making an AI system that replaces a '
                      'medical professional. The goal was much more careful: explore how an LLM-based inference system '
                      'can support a professional by retrieving relevant guideline context and returning structured '
                      'information that can still be reviewed.\n'
                      '\n'
                      'That difference matters a lot. In school projects it is easy to build a chatbot, connect it to '
                      'some documents, and call it finished. In a medical setting, the surrounding system becomes just '
                      'as important as the model itself. The application needs to be predictable, traceable, and '
                      'limited in what it promises.\n'
                      '\n'
                      '## The system I worked on\n'
                      '\n'
                      'The architecture was built as a small containerized inference platform. A dashboard can call an '
                      'API, the API validates the request, and an inference worker coordinates the retrieval and '
                      'generation flow. The system uses guideline documents as its main source of context, stores '
                      'vectors for similarity search, and runs the LLM workflow locally.\n'
                      '\n'
                      'The main components were:\n'
                      '\n'
                      '- **FastAPI and Pydantic** for request handling and validation\n'
                      '- **Qdrant** for vector storage and similarity search\n'
                      '- **MinIO** for storing guideline documents and longer-running job artefacts\n'
                      '- **Ollama** for local LLM and embedding runtime\n'
                      '- **Redis** for asynchronous job handling\n'
                      '- **Docker Compose** as the base deployment setup\n'
                      '\n'
                      'The container diagram I use as the cover image shows this split clearly: API boundaries, '
                      'storage services, retrieval logic, and inference workers all have their own responsibilities.\n'
                      '\n'
                      '## What made it interesting\n'
                      '\n'
                      'The most interesting part was not only getting an LLM to answer. It was everything around that '
                      'answer.\n'
                      '\n'
                      'A useful system has to know where its context comes from, how documents are stored, how a '
                      'request is validated, how long-running jobs are tracked, and how the final result is returned. '
                      'If one of those pieces is unclear, the whole application becomes harder to trust.\n'
                      '\n'
                      'That was a valuable lesson for me because it connected AI work with the kind of software '
                      'engineering I already enjoy: APIs, infrastructure, deployment, data flow, and system '
                      'boundaries.\n'
                      '\n'
                      '## Human-in-the-loop by design\n'
                      '\n'
                      'Because the project works with medical guidance, the application has to stay human-in-the-loop. '
                      'The system can support a professional, but it should not pretend to make a final decision on '
                      'its own.\n'
                      '\n'
                      'That mindset influenced how I thought about the project. The goal is not to make the model '
                      'sound confident. The goal is to make the workflow clear enough that a professional can '
                      'understand what the system is doing and where its limitations are.\n'
                      '\n'
                      '## What I learned\n'
                      '\n'
                      'This internship helped me understand that AI projects become more serious when they leave the '
                      'demo stage. A prompt is only one small part of the system. The rest is architecture: document '
                      'ingestion, retrieval, validation, background jobs, storage, deployment, and monitoring.\n'
                      '\n'
                      'It also made me more aware of the responsibility that comes with building tools for '
                      'professional environments. A feature can be technically impressive and still not be useful if '
                      'it is difficult to review or trust.\n'
                      '\n'
                      '## Reflection\n'
                      '\n'
                      'The biggest takeaway from this project is that careful boundaries make AI more useful, not '
                      'less. A well-designed assistant does not need to act like it knows everything. It needs to '
                      'support the user with the right context, at the right moment, in a way that is clear enough to '
                      'verify.',
  'content_markdown_nl': '# MobiLab-stage\n'
                         '\n'
                         'Tijdens mijn stage bij MobiLab & Care werkte ik aan een medisch guidance-prototype rond '
                         'cardiovasculaire medicatie. Het project ging niet over een AI-systeem dat een medische '
                         'professional vervangt. Het doel was veel voorzichtiger: onderzoeken hoe een LLM-gebaseerd '
                         'inferentiesysteem een professional kan ondersteunen door relevante richtlijncontext op te '
                         'halen en gestructureerde informatie terug te geven die nog steeds gecontroleerd kan worden.\n'
                         '\n'
                         'Dat verschil is belangrijk. In schoolprojecten is het makkelijk om een chatbot te bouwen, '
                         'die met documenten te verbinden en het project als klaar te beschouwen. In een medische '
                         'context wordt het systeem rond het model minstens even belangrijk als het model zelf. De '
                         'applicatie moet voorspelbaar, traceerbaar en duidelijk afgebakend zijn.\n'
                         '\n'
                         '## Het systeem waaraan ik werkte\n'
                         '\n'
                         'De architectuur werd opgebouwd als een klein gecontaineriseerd inferentieplatform. Een '
                         'dashboard kan een API aanroepen, de API valideert de request en een inference worker '
                         'coördineert de retrieval- en generatieflow. Het systeem gebruikt richtlijndocumenten als '
                         'belangrijkste bron van context, bewaart vectoren voor similarity search en voert de LLM-flow '
                         'lokaal uit.\n'
                         '\n'
                         'De belangrijkste componenten waren:\n'
                         '\n'
                         '- **FastAPI en Pydantic** voor request handling en validatie\n'
                         '- **Qdrant** voor vectoropslag en similarity search\n'
                         '- **MinIO** voor het bewaren van richtlijndocumenten en jobartefacten\n'
                         '- **Ollama** voor lokale LLM- en embeddingruntime\n'
                         '- **Redis** voor asynchrone jobverwerking\n'
                         '- **Docker Compose** als basis voor de deploymentsetup\n'
                         '\n'
                         'Het containerdiagram dat ik als coverafbeelding gebruik toont die opsplitsing duidelijk: '
                         'API-grenzen, opslagservices, retrieval-logica en inference workers hebben elk hun eigen '
                         'verantwoordelijkheid.\n'
                         '\n'
                         '## Wat het interessant maakte\n'
                         '\n'
                         'Het interessantste deel was niet alleen een LLM laten antwoorden. Het was alles rond dat '
                         'antwoord.\n'
                         '\n'
                         'Een bruikbaar systeem moet weten waar de context vandaan komt, hoe documenten worden '
                         'opgeslagen, hoe een request wordt gevalideerd, hoe langlopende jobs worden opgevolgd en hoe '
                         'het eindresultaat wordt teruggegeven. Als één van die onderdelen onduidelijk is, wordt de '
                         'hele applicatie moeilijker te vertrouwen.\n'
                         '\n'
                         'Dat was voor mij een waardevolle les omdat het AI-werk verbond met de software engineering '
                         "die ik sowieso interessant vind: API's, infrastructuur, deployment, dataflow en "
                         'systeemgrenzen.\n'
                         '\n'
                         '## Human-in-the-loop by design\n'
                         '\n'
                         'Omdat het project met medische guidance werkt, moet de applicatie human-in-the-loop blijven. '
                         'Het systeem kan een professional ondersteunen, maar mag niet doen alsof het zelfstandig een '
                         'eindbeslissing neemt.\n'
                         '\n'
                         'Die mindset beïnvloedde hoe ik naar het project keek. Het doel is niet om het model zo '
                         'zelfzeker mogelijk te laten klinken. Het doel is om de workflow duidelijk genoeg te maken '
                         'zodat een professional begrijpt wat het systeem doet en waar de beperkingen liggen.\n'
                         '\n'
                         '## Wat ik geleerd heb\n'
                         '\n'
                         'Deze stage liet me zien dat AI-projecten serieuzer worden zodra ze voorbij de demofase gaan. '
                         'Een prompt is maar een klein deel van het systeem. De rest is architectuur: document '
                         'ingestion, retrieval, validatie, background jobs, opslag, deployment en monitoring.\n'
                         '\n'
                         'Het maakte me ook bewuster van de verantwoordelijkheid die hoort bij tools voor '
                         'professionele omgevingen. Een feature kan technisch indrukwekkend zijn en toch niet '
                         'bruikbaar als ze moeilijk te controleren of te vertrouwen is.\n'
                         '\n'
                         '## Reflectie\n'
                         '\n'
                         'De grootste les uit dit project is dat duidelijke grenzen AI juist bruikbaarder maken. Een '
                         'goed ontworpen assistent hoeft niet te doen alsof hij alles weet. Hij moet de gebruiker '
                         'ondersteunen met de juiste context, op het juiste moment, op een manier die duidelijk genoeg '
                         'is om te verifiëren.',
  'cover_image_file_id': '0a9e43e7-24e3-5065-8d29-d0d20d1647dd',
  'cover_image_alt': 'Container diagram from the MobiLab internship project',
  'cover_image_alt_nl': 'Containerdiagram van het MobiLab-stageproject',
  'reading_time_minutes': 5,
  'status': 'published',
  'is_featured': False,
  'seo_title': 'MobiLab Internship | Alex van Poppel',
  'seo_title_nl': 'MobiLab Internship | Alex van Poppel',
  'seo_description': 'Reflections on building a grounded medical LLM inference system during an internship at MobiLab '
                     '& Care.',
  'seo_description_nl': 'Reflectie over het bouwen van een onderbouwd medisch LLM-inferentiesysteem tijdens een stage '
                        'bij MobiLab & Care.',
  'published_at': '2026-04-14T09:00:00+00:00',
  'created_at': '2026-04-14T09:00:00+00:00',
  'updated_at': '2026-04-28T17:05:00+00:00'}]

# Compatibility maps used by older tests/utilities. The active database seeder uses the
# explicit relationship rows from the CMS backup instead of deriving relationships by name.
PROJECT_SKILL_NAMES_BY_PROJECT_SLUG = {'internal-exchange-student-portal': ['Laravel',
                                      'Tailwind CSS',
                                      'Git',
                                      'Requirements Analysis',
                                      'Prototyping',
                                      'Team Leadership'],
 'iot-security-system': ['Python', 'Machine Learning', 'Git', 'Prototyping', 'FreeCAD'],
 'laravel-portfolio-website': ['Laravel', 'Tailwind CSS', 'Git', 'Docker', 'Networking Basics', 'SQL'],
 'mobicare-llmguidance': ['Python', 'Kubernetes', 'Machine Learning', 'FastAPI', 'Git', 'LLM'],
 'kraggleml-prediction': ['Python', 'Machine Learning'],
 'angular-portfolio-website': ['Angular',
                               'Proxmox',
                               'FastAPI',
                               'TypeScript',
                               'Git',
                               'Docker',
                               'Networking Basics',
                               'Tailwind CSS',
                               'LLM'],
 'appies-bricks': ['Angular', 'Git', 'Tailwind CSS', 'Azure', 'C#'],
 'ceriq-assistant': ['Python', 'Machine Learning', 'Docker', 'LLM']}
BLOG_TAG_NAMES_BY_POST_SLUG = {'mobilab-internship': ['AI', 'Kubernetes', 'Python'],
 'my-homelab': ['Homelabbing', 'Networking', 'Proxmox', 'TrueNAS']}
