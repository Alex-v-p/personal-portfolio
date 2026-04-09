import { SocialLink } from '../models/social-link.model';

export const SOCIAL_LINKS: SocialLink[] = [
  {
    id: 'social-github',
    profileId: 'profile-alex-van-poppel',
    platform: 'github',
    label: 'GitHub',
    url: 'https://github.com/shuzu',
    iconKey: 'github',
    sortOrder: 1,
    isVisible: true
  },
  {
    id: 'social-linkedin',
    profileId: 'profile-alex-van-poppel',
    platform: 'linkedin',
    label: 'LinkedIn',
    url: 'https://linkedin.com/in/alex-van-poppel',
    iconKey: 'linkedin',
    sortOrder: 2,
    isVisible: true
  },
  {
    id: 'social-email',
    profileId: 'profile-alex-van-poppel',
    platform: 'email',
    label: 'Email',
    url: 'mailto:hello@shuzu.dev',
    iconKey: 'mail',
    sortOrder: 3,
    isVisible: true
  }
].sort((a, b) => a.sortOrder - b.sortOrder);
