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
    svg: filledIcon(`
      <path d="M12 3.25A8.75 8.75 0 0 0 3.25 12c0 3.94 2.6 7.28 6.17 8.46.45.08.61-.2.61-.45v-1.57c-2.5.54-3.03-1.06-3.03-1.06-.4-1.03-1-1.3-1-1.3-.82-.56.07-.55.07-.55.9.06 1.37.92 1.37.92.8 1.37 2.1.97 2.61.75.08-.58.31-.97.56-1.2-2-.23-4.1-1-4.1-4.45 0-.98.35-1.78.92-2.4-.09-.23-.4-1.14.09-2.38 0 0 .76-.24 2.48.92a8.4 8.4 0 0 1 4.52 0c1.72-1.16 2.48-.92 2.48-.92.49 1.24.18 2.15.09 2.38.57.62.92 1.42.92 2.4 0 3.46-2.11 4.21-4.12 4.44.32.28.61.84.61 1.7v2.53c0 .25.16.53.62.45A8.76 8.76 0 0 0 20.75 12 8.75 8.75 0 0 0 12 3.25Z" />
    `),
  },
  linkedin: {
    key: 'linkedin',
    label: 'LinkedIn',
    group: 'social',
    keywords: ['social', 'professional', 'network'],
    svg: filledIcon(`
      <circle cx="6.8" cy="6.4" r="1.55" />
      <path d="M5.35 9.35h2.9v9.15h-2.9V9.35Z" />
      <path d="M10.2 9.35h2.78v1.25h0.04c0.38-0.72 1.33-1.48 2.75-1.48 2.95 0 3.49 1.94 3.49 4.46v4.92h-2.9v-4.36c0-1.04-0.02-2.38-1.45-2.38-1.45 0-1.68 1.14-1.68 2.31v4.43h-2.9V9.35Z" />
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
  youtube: {
    key: 'youtube',
    label: 'YouTube',
    group: 'social',
    keywords: ['social', 'video', 'media'],
    svg: filledIcon(`
      <path d="M19.7 8.34a2.5 2.5 0 0 0-1.76-1.77C16.36 6.12 12 6.12 12 6.12s-4.36 0-5.94.45A2.5 2.5 0 0 0 4.3 8.34 26.3 26.3 0 0 0 3.88 12c0 1.22.14 2.44.42 3.66a2.5 2.5 0 0 0 1.76 1.77c1.58.45 5.94.45 5.94.45s4.36 0 5.94-.45a2.5 2.5 0 0 0 1.76-1.77c.28-1.22.42-2.44.42-3.66 0-1.22-.14-2.44-.42-3.66ZM10.38 14.88V9.12L15.3 12l-4.92 2.88Z" />
    `),
  },
  facebook: {
    key: 'facebook',
    label: 'Facebook',
    group: 'social',
    keywords: ['social', 'meta', 'community'],
    svg: filledIcon(`
      <path d="M13.53 20.5v-7.02h2.36l.35-2.74h-2.71V9c0-.8.22-1.34 1.36-1.34h1.46V5.2c-.25-.03-1.12-.1-2.14-.1-2.12 0-3.57 1.3-3.57 3.68v2.06H8.25v2.74h2.39v7.02h2.89Z" />
    `),
  },
  discord: {
    key: 'discord',
    label: 'Discord',
    group: 'social',
    keywords: ['social', 'chat', 'community'],
    svg: filledIcon(`
      <path d="M17.46 7.2A13.2 13.2 0 0 0 14.2 6.2l-.16.32a12.2 12.2 0 0 1 2.94 1.13 9.78 9.78 0 0 0-4.98-1.29 9.8 9.8 0 0 0-4.98 1.3 12.2 12.2 0 0 1 2.95-1.14l-.16-.32c-1.13.18-2.23.52-3.27 1.01C4.46 10.28 4 13.29 4.23 16.26a13.28 13.28 0 0 0 4 2.03l.5-.82c-.74-.28-1.44-.64-2.08-1.08l.18-.14c1.5.7 3.13 1.05 4.77 1.05 1.64 0 3.27-.36 4.78-1.06l.17.14c-.64.44-1.34.8-2.08 1.08l.5.82a13.25 13.25 0 0 0 4-2.03c.3-3.43-.5-6.41-2.51-9.06ZM9.82 14.34c-.77 0-1.4-.72-1.4-1.6 0-.89.62-1.6 1.4-1.6.78 0 1.41.71 1.4 1.6 0 .88-.62 1.6-1.4 1.6Zm4.36 0c-.77 0-1.4-.72-1.4-1.6 0-.89.62-1.6 1.4-1.6.78 0 1.41.71 1.4 1.6 0 .88-.62 1.6-1.4 1.6Z" />
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
  link: {
    key: 'link',
    label: 'Link',
    group: 'contact',
    keywords: ['contact', 'url', 'website'],
    svg: strokeIcon(`
      <path d="M10.2 13.8 8.3 15.7a3 3 0 1 1-4.2-4.2L6 9.6" />
      <path d="m13.8 10.2 1.9-1.9a3 3 0 1 1 4.2 4.2L18 14.4" />
      <path d="m8.8 15.2 6.4-6.4" />
    `),
  },
  'external-link': {
    key: 'external-link',
    label: 'External link',
    group: 'contact',
    keywords: ['contact', 'url', 'external'],
    svg: strokeIcon(`
      <path d="M13 5.5h5.5V11" />
      <path d="m18.5 5.5-7.6 7.6" />
      <rect x="5" y="8.5" width="10.5" height="10.5" rx="2" />
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
  shield: {
    key: 'shield',
    label: 'Shield',
    group: 'expertise',
    keywords: ['security', 'protection', 'iot'],
    svg: strokeIcon(`
      <path d="M12 3.8 18 6v4.5c0 3.4-2.3 6.5-6 7.7-3.7-1.2-6-4.3-6-7.7V6l6-2.2Z" />
      <path d="m9.6 11.8 1.6 1.6 3.2-3.5" />
    `),
  },
  cpu: {
    key: 'cpu',
    label: 'CPU',
    group: 'expertise',
    keywords: ['hardware', 'embedded', 'chip'],
    svg: strokeIcon(`
      <rect x="7" y="7" width="10" height="10" rx="2" />
      <rect x="10" y="10" width="4" height="4" rx="0.8" />
      <path d="M9.5 3.8v2.4M14.5 3.8v2.4M9.5 17.8v2.4M14.5 17.8v2.4M3.8 9.5h2.4M3.8 14.5h2.4M17.8 9.5h2.4M17.8 14.5h2.4" />
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
  fastapi: {
    key: 'fastapi',
    label: 'FastAPI',
    group: 'tech',
    keywords: ['python', 'api', 'backend'],
    svg: strokeIcon(`
      <path d="M13.8 4.5 7.5 12h4.1L10.2 19.5 16.5 12h-4.1l1.4-7.5Z" />
    `),
  },
  csharp: {
    key: 'csharp',
    label: 'C#',
    group: 'tech',
    keywords: ['dotnet', '.net', 'language'],
    svg: strokeIcon(`
      <path d="M14.2 7.2a5.1 5.1 0 1 0 0 9.6" />
      <path d="M16.4 9.2v5.6M18.2 9.2v5.6M15.2 11h4.2M15.2 13h4.2" />
    `),
  },
  pandas: {
    key: 'pandas',
    label: 'Pandas',
    group: 'tech',
    keywords: ['python', 'dataframe', 'data'],
    svg: strokeIcon(`
      <rect x="6.5" y="5" width="3" height="6" rx="0.8" />
      <rect x="6.5" y="13" width="3" height="6" rx="0.8" />
      <rect x="11.5" y="8" width="3" height="11" rx="0.8" />
      <rect x="14.5" y="5" width="3" height="6" rx="0.8" />
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
    .replace(/[^a-z0-9-]/g, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');

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
