import { BlogPost } from '../models/blog-post.model';
import { ContactMethod } from '../models/contact-method.model';
import { Experience } from '../models/experience.model';
import { Project } from '../models/project.model';
import { Skill } from '../models/skill.model';
import { FEATURED_BLOG_POSTS } from './blog-posts.mock';
import { CONTACT_METHODS } from './contact-links.mock';
import { EXPERIENCES, PROFILE } from './profile.mock';
import { FEATURED_PROJECT, PROJECTS } from './projects.mock';
import { EXPERIENCE_SKILLS, SKILLS } from './skills.mock';

export interface HomeExperiencePreview extends Experience {
  skillNames: string[];
}

const skillNameMap = new Map<string, Skill>(SKILLS.map((skill) => [skill.id, skill]));

const resolveExperienceSkills = (experienceId: string): string[] => EXPERIENCE_SKILLS
  .filter((relation) => relation.experienceId === experienceId)
  .map((relation) => skillNameMap.get(relation.skillId)?.name)
  .filter((name): name is string => Boolean(name));

const featuredBlogPost: BlogPost = FEATURED_BLOG_POSTS[0];
const highlightedProjectIds = new Set([FEATURED_PROJECT.id]);
const supportingProjects: Project[] = PROJECTS
  .filter((project) => !highlightedProjectIds.has(project.id))
  .slice(0, 2);

export const HOME_HERO_PROFILE = PROFILE;
export const HOME_FEATURED_BLOG_POST = featuredBlogPost;
export const HOME_PRIMARY_FEATURED_PROJECT = FEATURED_PROJECT;
export const HOME_SECONDARY_FEATURED_PROJECTS = supportingProjects;
export const HOME_EXPERTISE_GROUPS = PROFILE.expertiseGroups;
export const HOME_EXPERIENCE_PREVIEW: HomeExperiencePreview[] = EXPERIENCES
  .slice(0, 3)
  .map((experience) => ({
    ...experience,
    skillNames: resolveExperienceSkills(experience.id)
  }));

export const HOME_CONTACT_PREVIEW_METHODS: ContactMethod[] = CONTACT_METHODS
  .filter((method) => ['email', 'phone', 'github', 'linkedin'].includes(method.platform))
  .slice(0, 4);
