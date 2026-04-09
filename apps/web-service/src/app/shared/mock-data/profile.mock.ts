import { Experience } from '../models/experience.model';
import { Profile } from '../models/profile.model';
import { MEDIA_FILES } from './media-files.mock';
import { SKILL_CATEGORIES, SKILLS } from './skills.mock';
import { buildExperienceViews, buildProfileView, ExperienceRecord, ProfileRecord } from './content.selectors';

export const PROFILE_RECORD: ProfileRecord = {
  id: 'profile-alex-van-poppel',
  firstName: 'Alex',
  lastName: 'van Poppel',
  headline: 'Software Engineer',
  shortIntro:
    'With a strong foundation in web development and UX design, I enjoy building user-centred experiences that are practical, clear, and pleasant to use.',
  longBio:
    'I build portfolio sites, data-heavy student projects, and full-stack applications with a focus on maintainable architecture, thoughtful UI, and future-friendly structure.',
  location: 'Lommel, Belgium',
  email: 'hello@shuzu.dev',
  phone: '+32 470 31 34 39',
  avatarFileId: 'file-avatar-alex',
  heroImageFileId: 'file-hero-portrait',
  resumeFileId: 'file-resume',
  ctaPrimaryLabel: 'Download CV',
  ctaPrimaryUrl: '/assets/mock-resume.pdf',
  ctaSecondaryLabel: 'Contact me',
  ctaSecondaryUrl: '/contact',
  createdAt: '2025-09-28T10:00:00Z',
  updatedAt: '2025-10-01T12:00:00Z'
};

export const EXPERIENCE_RECORDS: ExperienceRecord[] = [
  {
    id: 'experience-internship-client-work',
    organizationName: 'Client delivery team',
    roleTitle: 'Internship',
    location: 'Geel, Belgium',
    experienceType: 'internship',
    startDate: '2025-02-01',
    endDate: '2025-06-30',
    isCurrent: false,
    summary:
      'Worked on maintainable web interfaces, internal tooling, and clear communication with clients while shipping practical features in a team setting.',
    descriptionMarkdown:
      'Collaborated in a client-facing team on practical web features, internal tools, and documentation.',
    sortOrder: 1
  },
  {
    id: 'experience-thomas-more',
    organizationName: 'Thomas More',
    roleTitle: 'Applied Computer Science',
    location: 'Geel, Belgium',
    experienceType: 'education',
    startDate: '2022-09-01',
    endDate: null,
    isCurrent: true,
    summary:
      'Built projects across AI, software engineering, and web development, with a strong focus on hands-on delivery and iterative improvement.',
    descriptionMarkdown:
      'Worked on AI, web, and software engineering assignments with practical delivery and reflection.',
    sortOrder: 2
  },
  {
    id: 'experience-personal-projects',
    organizationName: 'Independent work',
    roleTitle: 'Personal Projects',
    location: 'Remote',
    experienceType: 'personal',
    startDate: '2023-01-01',
    endDate: null,
    isCurrent: true,
    summary:
      'Created portfolio, API, machine learning, and full-stack projects to sharpen real-world architecture, deployment, and UI skills.',
    descriptionMarkdown:
      'Used personal projects to practice architecture, deployment, and maintainable front-end work.',
    sortOrder: 3
  }
];

export const PROFILE: Profile = buildProfileView(PROFILE_RECORD, MEDIA_FILES, SKILL_CATEGORIES, SKILLS);
export const EXPERIENCES: Experience[] = buildExperienceViews(EXPERIENCE_RECORDS, MEDIA_FILES);
