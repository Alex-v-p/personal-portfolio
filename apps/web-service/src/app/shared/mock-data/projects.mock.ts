import { Project } from '../models/project.model';
import { MEDIA_FILES } from './media-files.mock';
import { PROJECT_SKILLS, SKILL_CATEGORIES, SKILLS } from './skills.mock';
import { buildProjectViews, ProjectRecord } from './content.selectors';

export const PROJECT_RECORDS: ProjectRecord[] = [
  {
    id: 'project-personal-portfolio',
    slug: 'personal-portfolio',
    title: 'Personal Portfolio Platform',
    teaser:
      'A portfolio platform with a strong component system, room for CMS features, and a structure that can grow into full API-backed content.',
    summary:
      'Designed and built a portfolio foundation around Angular, Tailwind, and modular page sections so content can move from mock data to real APIs without a redesign.',
    descriptionMarkdown:
      'Designed the shell, mock-data layer, and reusable layout pieces for a future CMS-backed portfolio.',
    coverImageFileId: 'file-project-portfolio-cover',
    githubUrl: 'https://github.com/shuzu',
    githubRepoName: 'personal-portfolio',
    startedOn: '2025-07-01',
    endedOn: null,
    durationLabel: '3 months',
    isFeatured: true,
    sortOrder: 1,
    publishedAt: '2025-10-01',
    state: 'published',
    organizationName: 'Personal project',
    highlight:
      'Focused on reusable layout pieces, scalable data shapes, and a front-end structure that supports future admin and assistant features.'
  },
  {
    id: 'project-plant-care-app',
    slug: 'plant-care-app',
    title: 'Plant Care App',
    teaser:
      'A web application that helps users take care of plants with schedules, instructions, and a community-oriented concept.',
    summary:
      'Worked through the product and architecture side of a plant care app, focusing on useful flows, clear information presentation, and a structure that supports growth over time.',
    descriptionMarkdown:
      'Focused on product thinking, schedules, and useful screens for plant care guidance.',
    coverImageFileId: 'file-project-plant-cover',
    startedOn: '2024-09-01',
    endedOn: '2025-02-28',
    durationLabel: '6 months',
    isFeatured: false,
    sortOrder: 2,
    publishedAt: '2025-03-01',
    state: 'completed',
    organizationName: 'Thomas More',
    highlight:
      'Emphasis on practical value, usable screens, and a clean business-to-product connection.'
  },
  {
    id: 'project-motogp-ticketing',
    slug: 'motogp-ticketing',
    title: 'MotoGP Ticket Reservation System',
    teaser:
      'A reservation flow with order screens, confirmation logic, and ticket-management interactions for event bookings.',
    summary:
      'Built React-based ticket ordering and management flows with clean state handling, user-friendly confirmation screens, and backend integration patterns.',
    descriptionMarkdown:
      'Built an event-booking flow with React components, order forms, and confirmation logic.',
    coverImageFileId: 'file-project-motogp-cover',
    demoUrl: 'https://example.com/motogp-demo',
    startedOn: '2024-09-01',
    endedOn: '2025-02-28',
    durationLabel: '6 months',
    isFeatured: false,
    sortOrder: 3,
    publishedAt: '2025-03-12',
    state: 'completed',
    organizationName: 'Thomas More',
    highlight:
      'Balanced interactive UI needs with maintainable implementation details and clear user feedback.'
  },
  {
    id: 'project-dino-classifier',
    slug: 'dino-classifier',
    title: 'Dinosaur Image Classifier',
    teaser:
      'A machine learning project using image datasets and EfficientNet to classify dinosaur species.',
    summary:
      'Cleaned datasets, set up augmentation, and trained a TensorFlow/Keras model while documenting the pipeline clearly enough to iterate on results later.',
    descriptionMarkdown:
      'Worked on data preparation, augmentation, training structure, and reproducible experimentation.',
    coverImageFileId: 'file-project-dino-cover',
    githubUrl: 'https://github.com/shuzu',
    githubRepoName: 'dinosaur-image-classifier',
    startedOn: '2025-04-01',
    endedOn: '2025-05-31',
    durationLabel: '4 months',
    isFeatured: false,
    sortOrder: 4,
    publishedAt: '2025-06-01',
    state: 'completed',
    organizationName: 'Thomas More',
    highlight:
      'Strong practice in data preparation, reproducible training structure, and model iteration.'
  },
  {
    id: 'project-auction-house-api',
    slug: 'auction-house-api',
    title: 'Auction House REST API',
    teaser:
      'A Spring Boot API project that implements Singleton and Observer patterns in a practical auction domain.',
    summary:
      'Designed endpoints for bidding workflows and observer registration while keeping the architecture focused on testable patterns and clear responsibilities.',
    descriptionMarkdown:
      'Implemented REST endpoints and pattern-focused services in a Spring Boot project.',
    coverImageFileId: 'file-project-auction-cover',
    githubUrl: 'https://github.com/shuzu',
    githubRepoName: 'auction-house',
    startedOn: '2025-06-01',
    endedOn: '2025-06-30',
    durationLabel: '3 months',
    isFeatured: false,
    sortOrder: 5,
    publishedAt: '2025-07-01',
    state: 'completed',
    organizationName: 'Thomas More',
    highlight:
      'Good example of combining backend fundamentals with pattern-driven design decisions.'
  }
];

export const PROJECTS: Project[] = buildProjectViews(PROJECT_RECORDS, MEDIA_FILES, SKILLS, SKILL_CATEGORIES, PROJECT_SKILLS);
export const FEATURED_PROJECT = PROJECTS.find((project) => project.isFeatured) ?? PROJECTS[0];
