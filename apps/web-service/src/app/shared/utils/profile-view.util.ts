import { ContactMethod } from '../models/contact-method.model';
import { Profile } from '../models/profile.model';

export const createEmptyProfile = (): Profile => ({
  id: '',
  firstName: '',
  lastName: '',
  name: '',
  headline: '',
  role: '',
  greeting: '',
  location: '',
  email: '',
  phone: '',
  shortIntro: '',
  longBio: '',
  heroTitle: '',
  summary: '',
  shortBio: '',
  footerDescription: '',
  avatarFileId: null,
  heroImageFileId: null,
  resumeFileId: null,
  avatarUrl: '',
  heroImageUrl: '',
  resumeUrl: '',
  skills: [],
  expertiseGroups: [],
  introParagraphs: [],
  availability: [],
  heroActions: [],
  socialLinks: [],
  createdAt: '',
  updatedAt: ''
});

const sanitizePhoneHref = (phone: string): string => `tel:${phone.replace(/\s+/g, '')}`;

export const buildContactMethodsFromProfile = (profile: Profile): ContactMethod[] => {
  const methods: ContactMethod[] = [];

  if (profile.email) {
    methods.push({
      id: 'contact-email',
      platform: 'email',
      label: 'Email',
      value: profile.email,
      href: `mailto:${profile.email}`,
      actionLabel: 'Send Email',
      iconKey: 'mail',
      description: 'Best for project enquiries, internships, and collaboration.',
      sortOrder: 1,
      isVisible: true,
    });
  }

  if (profile.phone) {
    methods.push({
      id: 'contact-phone',
      platform: 'phone',
      label: 'Phone',
      value: profile.phone,
      href: sanitizePhoneHref(profile.phone),
      actionLabel: 'Call',
      iconKey: 'phone',
      description: 'Useful for quick coordination or planning a meeting.',
      sortOrder: 2,
      isVisible: true,
    });
  }

  for (const link of profile.socialLinks ?? []) {
    methods.push({
      id: `contact-${link.platform}`,
      platform: link.platform,
      label: link.label,
      value: link.url.replace(/^https?:\/\//, ''),
      href: link.url,
      actionLabel: ['github', 'linkedin'].includes(link.platform) ? 'Connect +' : 'Open',
      iconKey: link.iconKey,
      description:
        link.platform === 'github'
          ? 'Code samples, experiments, and longer-form project work.'
          : link.platform === 'linkedin'
            ? 'Professional background, study path, and experience.'
            : 'Direct line for portfolio contact.',
      sortOrder: (link.sortOrder ?? 0) + 10,
      isVisible: link.isVisible,
    });
  }

  if (profile.location) {
    methods.push({
      id: 'contact-location',
      platform: 'location',
      label: 'Location',
      value: profile.location,
      href: `https://maps.google.com/?q=${encodeURIComponent(profile.location)}`,
      actionLabel: 'View Map',
      iconKey: 'map-pin',
      description: 'Available for on-site, hybrid, or remote collaboration.',
      sortOrder: 99,
      isVisible: true,
    });
  }

  return methods
    .filter((method) => method.isVisible)
    .sort((left, right) => left.sortOrder - right.sortOrder);
};
