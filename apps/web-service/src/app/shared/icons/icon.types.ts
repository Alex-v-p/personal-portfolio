export const ICON_GROUPS = {
  social: ['github', 'linkedin', 'twitter', 'instagram'],
  contact: ['mail', 'phone', 'map-pin', 'globe'],
  expertise: ['code', 'server', 'brain', 'database', 'workflow', 'languages'],
  tech: ['angular', 'laravel', 'python', 'docker', 'git', 'typescript', 'tailwindcss', 'sql', 'kubernetes'],
} as const;

export type IconGroupKey = keyof typeof ICON_GROUPS;

export const ICON_KEYS = [
  ...ICON_GROUPS.social,
  ...ICON_GROUPS.contact,
  ...ICON_GROUPS.expertise,
  ...ICON_GROUPS.tech,
] as const;

export type IconKey = (typeof ICON_KEYS)[number];

export type IconSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | number;

export interface IconDefinition {
  key: IconKey;
  label: string;
  group: IconGroupKey;
  svg: string;
  keywords?: readonly string[];
}

export interface IconOption {
  key: IconKey;
  label: string;
  group: IconGroupKey;
  keywords?: readonly string[];
}

export const ICON_ALIASES: Readonly<Record<string, IconKey>> = {
  email: 'mail',
  'e-mail': 'mail',
  mailto: 'mail',
  phonecall: 'phone',
  telephone: 'phone',
  location: 'map-pin',
  'map-pin': 'map-pin',
  map: 'map-pin',
  marker: 'map-pin',
  world: 'globe',
  frontend: 'code',
  'front-end': 'code',
  backend: 'server',
  'back-end': 'server',
  data: 'database',
  ai: 'brain',
  collaboration: 'workflow',
  language: 'languages',
  tailwind: 'tailwindcss',
  'tailwind-css': 'tailwindcss',
  ts: 'typescript',
  x: 'twitter',
  'linked-in': 'linkedin',
} as const;
