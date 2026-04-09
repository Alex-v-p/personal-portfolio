import { BlogTag } from '../models/blog-tag.model';
import { ExperienceSkill } from '../models/experience-skill.model';
import { ProjectSkill } from '../models/project-skill.model';
import { SkillCategory } from '../models/skill-category.model';
import { Skill } from '../models/skill.model';

export const SKILL_CATEGORIES: SkillCategory[] = [
  { id: 'cat-frontend', name: 'Front-End', description: 'UI and client-side technologies', sortOrder: 1 },
  { id: 'cat-backend', name: 'Back-End', description: 'API and server-side development', sortOrder: 2 },
  { id: 'cat-ai', name: 'AI', description: 'Machine learning and data tooling', sortOrder: 3 },
  { id: 'cat-programming', name: 'Programming', description: 'General languages and fundamentals', sortOrder: 4 },
  { id: 'cat-languages', name: 'Languages', description: 'Spoken languages', sortOrder: 5 }
].sort((a, b) => a.sortOrder - b.sortOrder);

export const SKILLS: Skill[] = [
  { id: 'skill-angular', categoryId: 'cat-frontend', name: 'Angular', yearsOfExperience: 2, iconKey: 'angular', sortOrder: 1, isHighlighted: true },
  { id: 'skill-tailwind', categoryId: 'cat-frontend', name: 'Tailwind', yearsOfExperience: 1, iconKey: 'tailwind', sortOrder: 2, isHighlighted: true },
  { id: 'skill-typescript', categoryId: 'cat-frontend', name: 'TypeScript', yearsOfExperience: 2, iconKey: 'typescript', sortOrder: 3, isHighlighted: true },
  { id: 'skill-react', categoryId: 'cat-frontend', name: 'React', yearsOfExperience: 1, iconKey: 'react', sortOrder: 4, isHighlighted: false },
  { id: 'skill-laravel', categoryId: 'cat-backend', name: 'Laravel', yearsOfExperience: 2, iconKey: 'laravel', sortOrder: 1, isHighlighted: true },
  { id: 'skill-dotnet', categoryId: 'cat-backend', name: '.NET', yearsOfExperience: 1, iconKey: 'dotnet', sortOrder: 2, isHighlighted: true },
  { id: 'skill-rest', categoryId: 'cat-backend', name: 'REST APIs', yearsOfExperience: 2, iconKey: 'api', sortOrder: 3, isHighlighted: false },
  { id: 'skill-java', categoryId: 'cat-programming', name: 'Java', yearsOfExperience: 2, iconKey: 'java', sortOrder: 1, isHighlighted: false },
  { id: 'skill-csharp', categoryId: 'cat-programming', name: 'C#', yearsOfExperience: 1, iconKey: 'csharp', sortOrder: 2, isHighlighted: false },
  { id: 'skill-python', categoryId: 'cat-ai', name: 'Python', yearsOfExperience: 2, iconKey: 'python', sortOrder: 1, isHighlighted: true },
  { id: 'skill-tensorflow', categoryId: 'cat-ai', name: 'TensorFlow', yearsOfExperience: 1, iconKey: 'tensorflow', sortOrder: 2, isHighlighted: false },
  { id: 'skill-data-prep', categoryId: 'cat-ai', name: 'Data Prep', yearsOfExperience: 1, iconKey: 'dataset', sortOrder: 3, isHighlighted: false },
  { id: 'skill-dutch', categoryId: 'cat-languages', name: 'Dutch', sortOrder: 1, isHighlighted: false },
  { id: 'skill-english', categoryId: 'cat-languages', name: 'English', sortOrder: 2, isHighlighted: false },
  { id: 'skill-french', categoryId: 'cat-languages', name: 'French', sortOrder: 3, isHighlighted: false },
  { id: 'skill-ux', categoryId: 'cat-frontend', name: 'UX', yearsOfExperience: 1, iconKey: 'layout', sortOrder: 5, isHighlighted: false },
  { id: 'skill-efficientnet', categoryId: 'cat-ai', name: 'EfficientNet', yearsOfExperience: 1, iconKey: 'model', sortOrder: 4, isHighlighted: false },
  { id: 'skill-state-management', categoryId: 'cat-frontend', name: 'State Management', yearsOfExperience: 1, iconKey: 'state', sortOrder: 6, isHighlighted: false },
  { id: 'skill-design-patterns', categoryId: 'cat-programming', name: 'Design Patterns', yearsOfExperience: 1, iconKey: 'patterns', sortOrder: 4, isHighlighted: false },
  { id: 'skill-livewire', categoryId: 'cat-backend', name: 'Livewire', yearsOfExperience: 1, iconKey: 'livewire', sortOrder: 4, isHighlighted: false },
  { id: 'skill-nx', categoryId: 'cat-frontend', name: 'Nx', yearsOfExperience: 1, iconKey: 'nx', sortOrder: 7, isHighlighted: false },
  { id: 'skill-spring-boot', categoryId: 'cat-backend', name: 'Spring Boot', yearsOfExperience: 1, iconKey: 'spring', sortOrder: 5, isHighlighted: false },
  { id: 'skill-ml', categoryId: 'cat-ai', name: 'ML', yearsOfExperience: 1, iconKey: 'ml', sortOrder: 5, isHighlighted: false }
].sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name));

export const PROJECT_SKILLS: ProjectSkill[] = [
  { projectId: 'project-personal-portfolio', skillId: 'skill-angular' },
  { projectId: 'project-personal-portfolio', skillId: 'skill-tailwind' },
  { projectId: 'project-personal-portfolio', skillId: 'skill-typescript' },
  { projectId: 'project-personal-portfolio', skillId: 'skill-nx' },
  { projectId: 'project-plant-care-app', skillId: 'skill-laravel' },
  { projectId: 'project-plant-care-app', skillId: 'skill-livewire' },
  { projectId: 'project-plant-care-app', skillId: 'skill-tailwind' },
  { projectId: 'project-plant-care-app', skillId: 'skill-ux' },
  { projectId: 'project-motogp-ticketing', skillId: 'skill-react' },
  { projectId: 'project-motogp-ticketing', skillId: 'skill-rest' },
  { projectId: 'project-motogp-ticketing', skillId: 'skill-state-management' },
  { projectId: 'project-dino-classifier', skillId: 'skill-python' },
  { projectId: 'project-dino-classifier', skillId: 'skill-tensorflow' },
  { projectId: 'project-dino-classifier', skillId: 'skill-efficientnet' },
  { projectId: 'project-dino-classifier', skillId: 'skill-ml' },
  { projectId: 'project-auction-house-api', skillId: 'skill-java' },
  { projectId: 'project-auction-house-api', skillId: 'skill-spring-boot' },
  { projectId: 'project-auction-house-api', skillId: 'skill-rest' },
  { projectId: 'project-auction-house-api', skillId: 'skill-design-patterns' }
];

export const EXPERIENCE_SKILLS: ExperienceSkill[] = [
  { experienceId: 'experience-internship-client-work', skillId: 'skill-angular' },
  { experienceId: 'experience-internship-client-work', skillId: 'skill-rest' },
  { experienceId: 'experience-internship-client-work', skillId: 'skill-typescript' },
  { experienceId: 'experience-thomas-more', skillId: 'skill-python' },
  { experienceId: 'experience-thomas-more', skillId: 'skill-laravel' },
  { experienceId: 'experience-thomas-more', skillId: 'skill-dotnet' },
  { experienceId: 'experience-personal-projects', skillId: 'skill-angular' },
  { experienceId: 'experience-personal-projects', skillId: 'skill-tailwind' },
  { experienceId: 'experience-personal-projects', skillId: 'skill-design-patterns' }
];

export const BLOG_TAGS: BlogTag[] = [
  { id: 'tag-angular', name: 'Angular', slug: 'angular' },
  { id: 'tag-architecture', name: 'Architecture', slug: 'architecture' },
  { id: 'tag-ui', name: 'UI', slug: 'ui' },
  { id: 'tag-mock-data', name: 'Mock Data', slug: 'mock-data' },
  { id: 'tag-planning', name: 'Planning', slug: 'planning' },
  { id: 'tag-typescript', name: 'TypeScript', slug: 'typescript' },
  { id: 'tag-career', name: 'Career', slug: 'career' },
  { id: 'tag-projects', name: 'Projects', slug: 'projects' },
  { id: 'tag-writing', name: 'Writing', slug: 'writing' },
  { id: 'tag-components', name: 'Components', slug: 'components' },
  { id: 'tag-tailwind', name: 'Tailwind', slug: 'tailwind' },
  { id: 'tag-design-systems', name: 'Design Systems', slug: 'design-systems' }
];
