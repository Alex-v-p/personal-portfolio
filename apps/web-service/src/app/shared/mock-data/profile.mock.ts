import { Experience } from '../models/experience.model';
import { Profile } from '../models/profile.model';

export const PROFILE: Profile = {
  name: 'Alex van Poppel',
  role: 'Software Engineer',
  greeting: "Hi, I'm Alex",
  location: 'Lommel, Belgium',
  heroTitle: "I’m a Software Engineer",
  summary:
    'With a strong foundation in web development and UX design, I enjoy building user-centred experiences that are practical, clear, and pleasant to use.',
  shortBio:
    'I build portfolio sites, data-heavy student projects, and full-stack applications with a focus on maintainable architecture, thoughtful UI, and future-friendly structure.',
  footerDescription:
    'Applied Computer Science student focused on AI, web development, and building practical digital products that are easy to maintain.',
  skills: ['Angular', 'Tailwind', 'TypeScript', 'Laravel', '.NET', 'Python'],
  expertiseGroups: [
    { title: 'Front-End', tags: ['Angular', 'Tailwind', 'TypeScript'] },
    { title: 'Back-End', tags: ['Laravel', '.NET', 'REST APIs'] },
    { title: 'AI', tags: ['Python', 'TensorFlow', 'Data Prep'] },
    { title: 'Programming', tags: ['Java', 'C#', 'TypeScript'] },
    { title: 'Languages', tags: ['Dutch', 'English', 'French'] }
  ],
  introParagraphs: [
    'I like building systems that feel simple on the surface and are well-structured underneath. That includes thoughtful UI, clean component design, and backend work that supports growth later.',
    'This mock portfolio content is intentionally realistic and reusable, so later stages can swap in API data without changing the overall page shapes.'
  ],
  availability: ['Open to internships', 'Open to freelance', 'Based in Belgium'],
  heroActions: [
    {
      label: 'Download CV',
      appearance: 'secondary',
      href: '/assets/mock-resume.pdf'
    },
    {
      label: 'Contact me',
      appearance: 'primary',
      routerLink: '/contact'
    }
  ]
};

export const EXPERIENCES: Experience[] = [
  {
    id: 'internship-client-work',
    title: 'Internship',
    organization: 'Client delivery team',
    location: 'Geel, Belgium',
    period: 'Feb 2025 - Jun 2025',
    summary:
      'Worked on maintainable web interfaces, internal tooling, and clear communication with clients while shipping practical features in a team setting.'
  },
  {
    id: 'thomas-more',
    title: 'Thomas More',
    organization: 'Applied Computer Science',
    location: 'Geel, Belgium',
    period: '2022 - present',
    summary:
      'Built projects across AI, software engineering, and web development, with a strong focus on hands-on delivery and iterative improvement.'
  },
  {
    id: 'personal-projects',
    title: 'Personal Projects',
    organization: 'Independent work',
    location: 'Remote',
    period: '2023 - present',
    summary:
      'Created portfolio, API, machine learning, and full-stack projects to sharpen real-world architecture, deployment, and UI skills.'
  }
];
