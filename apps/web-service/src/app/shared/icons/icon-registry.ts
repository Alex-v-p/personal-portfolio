import { ICON_ALIASES, ICON_GROUPS, type IconDefinition, type IconGroupKey, type IconKey, type IconOption } from './icon.types';

const strokeIcon = (body: string, viewBox = '0 0 24 24'): string => `
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox}" width="100%" height="100%" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
    ${body}
  </svg>
`;

const filledIcon = (body: string, viewBox = '0 0 24 24'): string => `
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox}" width="100%" height="100%" fill="currentColor" aria-hidden="true" focusable="false">
    ${body}
  </svg>
`;

export const ICON_REGISTRY: Readonly<Record<IconKey, IconDefinition>> = {
  github: {
    key: 'github',
    label: 'GitHub',
    group: 'social',
    keywords: ['social', 'code', 'repository'],
    svg: strokeIcon(`
      <path d="M8 8.2 9.4 5.8 12 7.1 14.6 5.8 16 8.2" />
      <path d="M8.3 16.8c-1.9-1.3-3.1-3.4-3.1-5.8 0-3.8 3.1-6.9 6.8-6.9s6.8 3.1 6.8 6.9c0 2.4-1.2 4.6-3.1 5.8" />
      <circle cx="9.5" cy="10.6" r="0.6" fill="currentColor" stroke="none" />
      <circle cx="14.5" cy="10.6" r="0.6" fill="currentColor" stroke="none" />
      <path d="M9.5 13.6c0.9 0.7 1.7 1 2.5 1s1.6-0.3 2.5-1" />
      <path d="M10.2 17v2" />
      <path d="M13.8 17v2" />
    `),
  },
  linkedin: {
    key: 'linkedin',
    label: 'LinkedIn',
    group: 'social',
    keywords: ['social', 'professional', 'network'],
    svg: strokeIcon(`
      <rect x="4.5" y="4.5" width="15" height="15" rx="3" />
      <circle cx="8.1" cy="9" r="0.75" fill="currentColor" stroke="none" />
      <path d="M8.1 11.1v4.2" />
      <path d="M11.4 15.3v-4.2" />
      <path d="M11.4 12.3c0.6-0.8 1.3-1.2 2.3-1.2 1.7 0 2.8 1.1 2.8 3v3.2" />
    `),
  },
  twitter: {
    key: 'twitter',
    label: 'X / Twitter',
    group: 'social',
    keywords: ['social', 'x', 'microblog'],
    svg: strokeIcon(`
      <path d="M6.5 5.5 17.5 18.5" />
      <path d="M17.5 5.5 6.5 18.5" />
    `),
  },
  instagram: {
    key: 'instagram',
    label: 'Instagram',
    group: 'social',
    keywords: ['social', 'photos', 'media'],
    svg: strokeIcon(`
      <rect x="4.5" y="4.5" width="15" height="15" rx="4" />
      <circle cx="12" cy="12" r="3.25" />
      <circle cx="16.2" cy="7.8" r="0.75" fill="currentColor" stroke="none" />
    `),
  },
  mail: {
    key: 'mail',
    label: 'Email',
    group: 'contact',
    keywords: ['contact', 'email', 'message'],
    svg: strokeIcon(`
      <rect x="3.5" y="6.5" width="17" height="11" rx="2.5" />
      <path d="m5.4 8.2 6.6 5.1 6.6-5.1" />
    `),
  },
  phone: {
    key: 'phone',
    label: 'Phone',
    group: 'contact',
    keywords: ['contact', 'call', 'telephone'],
    svg: strokeIcon(`
      <path d="M8.6 5.6c0.5-0.5 1.4-0.5 1.9 0l1.4 1.4c0.5 0.5 0.5 1.2 0.1 1.8l-1.1 1.5c1 1.9 2.5 3.4 4.4 4.4l1.5-1.1c0.6-0.4 1.4-0.4 1.8 0.1l1.4 1.4c0.5 0.5 0.5 1.4 0 1.9l-1.2 1.2c-0.9 0.9-2.2 1.3-3.4 1-5.2-1.3-9.3-5.4-10.6-10.6-0.3-1.2 0.1-2.5 1-3.4L8.6 5.6Z" />
    `),
  },
  'map-pin': {
    key: 'map-pin',
    label: 'Location',
    group: 'contact',
    keywords: ['contact', 'location', 'map'],
    svg: strokeIcon(`
      <path d="M12 20c3.6-4.1 5.4-7.1 5.4-9.4a5.4 5.4 0 1 0-10.8 0C6.6 12.9 8.4 15.9 12 20Z" />
      <circle cx="12" cy="10.6" r="1.8" />
    `),
  },
  globe: {
    key: 'globe',
    label: 'Globe',
    group: 'contact',
    keywords: ['contact', 'website', 'world'],
    svg: strokeIcon(`
      <circle cx="12" cy="12" r="8" />
      <path d="M4.5 12h15" />
      <path d="M12 4c2.2 2.2 3.5 5 3.5 8s-1.3 5.8-3.5 8c-2.2-2.2-3.5-5-3.5-8s1.3-5.8 3.5-8Z" />
    `),
  },
  code: {
    key: 'code',
    label: 'Code',
    group: 'expertise',
    keywords: ['frontend', 'development', 'programming'],
    svg: strokeIcon(`
      <path d="m8.5 8.5-4 3.5 4 3.5" />
      <path d="m15.5 8.5 4 3.5-4 3.5" />
      <path d="M13.5 6 10.5 18" />
    `),
  },
  server: {
    key: 'server',
    label: 'Server',
    group: 'expertise',
    keywords: ['backend', 'infrastructure', 'api'],
    svg: strokeIcon(`
      <rect x="4" y="5" width="16" height="5" rx="1.8" />
      <rect x="4" y="14" width="16" height="5" rx="1.8" />
      <circle cx="7.5" cy="7.5" r="0.6" fill="currentColor" stroke="none" />
      <circle cx="10" cy="7.5" r="0.6" fill="currentColor" stroke="none" />
      <circle cx="7.5" cy="16.5" r="0.6" fill="currentColor" stroke="none" />
      <circle cx="10" cy="16.5" r="0.6" fill="currentColor" stroke="none" />
      <path d="M13 7.5h4" />
      <path d="M13 16.5h4" />
    `),
  },
  brain: {
    key: 'brain',
    label: 'Brain',
    group: 'expertise',
    keywords: ['ai', 'ml', 'thinking', 'data'],
    svg: strokeIcon(`
      <path d="M9.4 7.5a2.4 2.4 0 1 1 4.8 0c1.6 0 2.9 1.3 2.9 2.9 1.3 0.4 2.2 1.7 2.2 3.1 0 1.8-1.5 3.3-3.3 3.3H9.2a3.2 3.2 0 0 1-3.2-3.2c0-1.2 0.7-2.3 1.7-2.8a3 3 0 0 1 1.7-3.3Z" />
      <path d="M12 5.8v12" />
      <path d="M9.8 9.2c0.9 0.3 1.6 1 2.2 1.9" />
      <path d="M14.2 9.2c-0.9 0.3-1.6 1-2.2 1.9" />
      <path d="M9.6 14.2c0.9-0.1 1.7 0.2 2.4 0.9" />
      <path d="M14.4 14.2c-0.9-0.1-1.7 0.2-2.4 0.9" />
    `),
  },
  database: {
    key: 'database',
    label: 'Database',
    group: 'expertise',
    keywords: ['data', 'storage', 'sql'],
    svg: strokeIcon(`
      <ellipse cx="12" cy="6.5" rx="6.5" ry="2.5" />
      <path d="M5.5 6.5v9c0 1.4 2.9 2.5 6.5 2.5s6.5-1.1 6.5-2.5v-9" />
      <path d="M5.5 11c0 1.4 2.9 2.5 6.5 2.5s6.5-1.1 6.5-2.5" />
    `),
  },
  workflow: {
    key: 'workflow',
    label: 'Workflow',
    group: 'expertise',
    keywords: ['analysis', 'collaboration', 'process'],
    svg: strokeIcon(`
      <circle cx="6.5" cy="7" r="2.5" />
      <circle cx="17.5" cy="12" r="2.5" />
      <circle cx="6.5" cy="17" r="2.5" />
      <path d="M9 7h2.8c1.1 0 2 .9 2 2v0.5" />
      <path d="M9 17h2.8c1.1 0 2-.9 2-2v-0.5" />
      <path d="M15 12h-1.4" />
    `),
  },
  languages: {
    key: 'languages',
    label: 'Languages',
    group: 'expertise',
    keywords: ['language', 'communication', 'locales'],
    svg: strokeIcon(`
      <path d="M6 6.5h7a2.5 2.5 0 0 1 2.5 2.5v3A2.5 2.5 0 0 1 13 14.5H9l-3 3v-3H6A2.5 2.5 0 0 1 3.5 12V9A2.5 2.5 0 0 1 6 6.5Z" />
      <path d="M14.5 9.5h3.5a2.5 2.5 0 0 1 2.5 2.5v2.5A2.5 2.5 0 0 1 18 17h-0.5V20l-3-3H14" />
      <path d="M7.2 11.7h4.6" />
      <path d="M8.3 9.5c0.5 1.4 1.4 2.6 2.7 3.6" />
      <path d="M9.5 9.4v2.2" />
    `),
  },
  angular: {
    key: 'angular',
    label: 'Angular',
    group: 'tech',
    keywords: ['framework', 'frontend'],
    svg: filledIcon(`
      <path d="M12 2.8 5.4 5.1l1 10.2L12 21.2l5.6-5.9 1-10.2L12 2.8Z" />
      <path fill="white" d="M12 6.9 8.6 15.6h1.9l0.7-2h1.6l0.7 2h1.9L12 6.9Zm-0.4 5.1 0.4-1.1 0.4 1.1h-0.8Z" />
    `),
  },
  laravel: {
    key: 'laravel',
    label: 'Laravel',
    group: 'tech',
    keywords: ['framework', 'backend', 'php'],
    svg: strokeIcon(`
      <path d="m6 8 4-2.3 4 2.3v4.5L10 14.8 6 12.5Z" />
      <path d="m14 8 4-2.3v4.5l-4 2.3" />
      <path d="M10 14.8v3.5l4-2.3v-3.5" />
      <path d="m10 5.7 4 2.3 4-2.3" />
    `),
  },
  python: {
    key: 'python',
    label: 'Python',
    group: 'tech',
    keywords: ['language', 'backend', 'data'],
    svg: strokeIcon(`
      <path d="M9 4.8h3.3c1.6 0 2.7 1.1 2.7 2.7v2.1H9.5c-1.4 0-2.5 1.1-2.5 2.5v1.1H5.8c-1.3 0-2.3-1-2.3-2.3V8.1c0-1.8 1.5-3.3 3.3-3.3H9Z" />
      <circle cx="11.7" cy="7.3" r="0.55" fill="currentColor" stroke="none" />
      <path d="M15 19.2h-3.3c-1.6 0-2.7-1.1-2.7-2.7v-2.1h5.5c1.4 0 2.5-1.1 2.5-2.5v-1.1h1.2c1.3 0 2.3 1 2.3 2.3v2.8c0 1.8-1.5 3.3-3.3 3.3H15Z" />
      <circle cx="12.3" cy="16.7" r="0.55" fill="currentColor" stroke="none" />
    `),
  },
  docker: {
    key: 'docker',
    label: 'Docker',
    group: 'tech',
    keywords: ['containers', 'infrastructure', 'ops'],
    svg: strokeIcon(`
      <rect x="5" y="9" width="3" height="3" />
      <rect x="8.5" y="9" width="3" height="3" />
      <rect x="12" y="9" width="3" height="3" />
      <rect x="8.5" y="5.5" width="3" height="3" />
      <rect x="12" y="5.5" width="3" height="3" />
      <path d="M4 14.5h11.2c1.7 0 3.1-1.4 3.1-3.1 0 0-0.9 0.9-2.6 0.9H4.8" />
      <path d="M6.2 17.4c0.9 0.8 2.4 1.3 3.8 1.3 2.1 0 4-0.9 5.1-2.3" />
    `),
  },
  git: {
    key: 'git',
    label: 'Git',
    group: 'tech',
    keywords: ['version control', 'repository'],
    svg: strokeIcon(`
      <circle cx="7" cy="7" r="2.1" />
      <circle cx="17" cy="12" r="2.1" />
      <circle cx="7" cy="17" r="2.1" />
      <path d="M9.1 7h3.2a2.7 2.7 0 0 1 2.7 2.7V12" />
      <path d="M9.1 17h3.2a2.7 2.7 0 0 0 2.7-2.7V12" />
    `),
  },
  typescript: {
    key: 'typescript',
    label: 'TypeScript',
    group: 'tech',
    keywords: ['language', 'ts', 'frontend'],
    svg: strokeIcon(`
      <rect x="4.5" y="4.5" width="15" height="15" rx="2.2" />
      <path d="M8.3 9h5.4" />
      <path d="M11 9v6" />
      <path d="M16.8 10.4c-0.5-0.9-2.3-0.8-2.8 0-0.4 0.7 0.1 1.4 1 1.6l0.9 0.2c0.9 0.2 1.4 0.9 1 1.6-0.5 0.9-2.3 1-3 0.1" />
    `),
  },
  tailwindcss: {
    key: 'tailwindcss',
    label: 'Tailwind CSS',
    group: 'tech',
    keywords: ['css', 'utility', 'frontend'],
    svg: strokeIcon(`
      <path d="M6 10.2c1.3-2.4 3.1-3.6 5.5-3.6 1.5 0 2.7 0.6 3.6 1.7 0.7 0.8 1.4 1.2 2.4 1.2 1 0 1.9-0.5 2.5-1.4-1.2 2.4-3.1 3.6-5.5 3.6-1.5 0-2.7-0.6-3.6-1.7-0.7-0.8-1.4-1.2-2.4-1.2-1 0-1.9 0.5-2.5 1.4Z" />
      <path d="M4 15.5c1.3-2.4 3.1-3.6 5.5-3.6 1.5 0 2.7 0.6 3.6 1.7 0.7 0.8 1.4 1.2 2.4 1.2 1 0 1.9-0.5 2.5-1.4-1.2 2.4-3.1 3.6-5.5 3.6-1.5 0-2.7-0.6-3.6-1.7-0.7-0.8-1.4-1.2-2.4-1.2-1 0-1.9 0.5-2.5 1.4Z" />
    `),
  },
  sql: {
    key: 'sql',
    label: 'SQL',
    group: 'tech',
    keywords: ['database', 'query', 'data'],
    svg: strokeIcon(`
      <ellipse cx="9" cy="7" rx="4.5" ry="2" />
      <path d="M4.5 7v5c0 1.1 2 2 4.5 2s4.5-0.9 4.5-2V7" />
      <path d="M4.5 9.5c0 1.1 2 2 4.5 2s4.5-0.9 4.5-2" />
      <path d="M15.2 9.3h4.3" />
      <path d="M15.2 12h3.3" />
      <path d="M15.2 14.7h4.3" />
    `),
  },
  kubernetes: {
    key: 'kubernetes',
    label: 'Kubernetes',
    group: 'tech',
    keywords: ['containers', 'orchestration', 'ops'],
    svg: strokeIcon(`
      <path d="M12 4.2 17.3 7.2 17.3 13.2 12 16.2 6.7 13.2 6.7 7.2Z" />
      <circle cx="12" cy="10.2" r="1.9" />
      <path d="M12 3.2v2.8" />
      <path d="m18.1 6.7-2.4 1.4" />
      <path d="m18.1 13.7-2.4-1.4" />
      <path d="M12 17.2v-2.8" />
      <path d="m5.9 13.7 2.4-1.4" />
      <path d="m5.9 6.7 2.4 1.4" />
    `),
  },
};

export const ICON_OPTIONS: readonly IconOption[] = Object.values(ICON_REGISTRY)
  .map(({ key, label, group, keywords }) => ({ key, label, group, keywords }))
  .sort((left, right) => left.label.localeCompare(right.label));

export const getIconOptionsForGroup = (group: IconGroupKey): IconOption[] =>
  ICON_OPTIONS.filter((option) => option.group === group);

export const getOrderedIconOptions = (): Record<IconGroupKey, IconOption[]> => ({
  social: getIconOptionsForGroup('social'),
  contact: getIconOptionsForGroup('contact'),
  expertise: getIconOptionsForGroup('expertise'),
  tech: getIconOptionsForGroup('tech'),
});

export const normalizeIconKey = (value: string | null | undefined): string =>
  (value ?? '')
    .trim()
    .toLowerCase()
    .replace(/[\s_]+/g, '-')
    .replace(/[^a-z0-9-]/g, '');

export const resolveIconKey = (value: string | null | undefined): IconKey | null => {
  const normalizedValue = normalizeIconKey(value);

  if (!normalizedValue) {
    return null;
  }

  if (normalizedValue in ICON_REGISTRY) {
    return normalizedValue as IconKey;
  }

  return ICON_ALIASES[normalizedValue] ?? null;
};

export const getIconDefinition = (value: string | null | undefined): IconDefinition | null => {
  const resolvedKey = resolveIconKey(value);
  return resolvedKey ? ICON_REGISTRY[resolvedKey] : null;
};

export const getIconLabel = (value: string | null | undefined): string | null => getIconDefinition(value)?.label ?? null;

export const getDefaultIconKeyForGroup = (group: IconGroupKey): IconKey => ICON_GROUPS[group][0];
