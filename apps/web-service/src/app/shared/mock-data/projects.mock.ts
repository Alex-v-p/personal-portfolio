import { Project } from '../models/project.model';

export const PROJECTS: Project[] = [
  {
    id: 'personal-portfolio',
    slug: 'personal-portfolio',
    title: 'Personal Portfolio Platform',
    shortDescription:
      'A portfolio platform with a strong component system, room for CMS features, and a structure that can grow into full API-backed content.',
    summary:
      'Designed and built a portfolio foundation around Angular, Tailwind, and modular page sections so content can move from mock data to real APIs without a redesign.',
    organization: 'Personal project',
    duration: '3 months',
    status: 'In progress',
    category: 'Frontend',
    tags: ['Angular', 'Tailwind', 'TypeScript', 'Nx'],
    featured: true,
    imageAlt: 'Wireframe-inspired portfolio layout mock-up',
    highlight:
      'Focused on reusable layout pieces, scalable data shapes, and a front-end structure that supports future admin and assistant features.',
    links: [
      { label: 'Read More', routerLink: ['/projects'] },
      { label: 'GitHub README', href: 'https://github.com/shuzu' }
    ]
  },
  {
    id: 'plant-care-app',
    slug: 'plant-care-app',
    title: 'Plant Care App',
    shortDescription:
      'A web application that helps users take care of plants with schedules, instructions, and a community-oriented concept.',
    summary:
      'Worked through the product and architecture side of a plant care app, focusing on useful flows, clear information presentation, and a structure that supports growth over time.',
    organization: 'Thomas More',
    duration: '6 months',
    status: 'Completed',
    category: 'Full stack',
    tags: ['Laravel', 'Livewire', 'Tailwind', 'UX'],
    featured: false,
    imageAlt: 'Plant care dashboard concept',
    highlight:
      'Emphasis on practical value, usable screens, and a clean business-to-product connection.',
    links: [{ label: 'View Details', routerLink: ['/projects'] }]
  },
  {
    id: 'motogp-ticketing',
    slug: 'motogp-ticketing',
    title: 'MotoGP Ticket Reservation System',
    shortDescription:
      'A reservation flow with order screens, confirmation logic, and ticket-management interactions for event bookings.',
    summary:
      'Built React-based ticket ordering and management flows with clean state handling, user-friendly confirmation screens, and backend integration patterns.',
    organization: 'Thomas More',
    duration: '6 months',
    status: 'Completed',
    category: 'Frontend',
    tags: ['React', 'REST API', 'State Management'],
    featured: false,
    imageAlt: 'MotoGP booking interface mock-up',
    highlight:
      'Balanced interactive UI needs with maintainable implementation details and clear user feedback.',
    links: [{ label: 'View Details', routerLink: ['/projects'] }]
  },
  {
    id: 'dino-classifier',
    slug: 'dino-classifier',
    title: 'Dinosaur Image Classifier',
    shortDescription:
      'A machine learning project using image datasets and EfficientNet to classify dinosaur species.',
    summary:
      'Cleaned datasets, set up augmentation, and trained a TensorFlow/Keras model while documenting the pipeline clearly enough to iterate on results later.',
    organization: 'Thomas More',
    duration: '4 months',
    status: 'Completed',
    category: 'AI',
    tags: ['Python', 'TensorFlow', 'EfficientNet', 'ML'],
    featured: false,
    imageAlt: 'Dataset and model-training workflow diagram',
    highlight:
      'Strong practice in data preparation, reproducible training structure, and model iteration.',
    links: [{ label: 'View Details', routerLink: ['/projects'] }]
  },
  {
    id: 'auction-house-api',
    slug: 'auction-house-api',
    title: 'Auction House REST API',
    shortDescription:
      'A Spring Boot API project that implements Singleton and Observer patterns in a practical auction domain.',
    summary:
      'Designed endpoints for bidding workflows and observer registration while keeping the architecture focused on testable patterns and clear responsibilities.',
    organization: 'Thomas More',
    duration: '3 months',
    status: 'Completed',
    category: 'Backend',
    tags: ['Java', 'Spring Boot', 'REST API', 'Design Patterns'],
    featured: false,
    imageAlt: 'Auction workflow and service architecture sketch',
    highlight:
      'Good example of combining backend fundamentals with pattern-driven design decisions.',
    links: [{ label: 'View Details', routerLink: ['/projects'] }]
  }
];

export const FEATURED_PROJECT = PROJECTS.find((project) => project.featured) ?? PROJECTS[0];
