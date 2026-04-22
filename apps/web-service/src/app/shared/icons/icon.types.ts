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
  call: 'phone',
  location: 'map-pin',
  'map-pin': 'map-pin',
  map: 'map-pin',
  marker: 'map-pin',
  pin: 'map-pin',
  world: 'globe',
  website: 'globe',
  web: 'globe',
  portfolio: 'globe',
  frontend: 'code',
  'front-end': 'code',
  backend: 'server',
  'back-end': 'server',
  api: 'server',
  fastapi: 'server',
  proxmox: 'server',
  data: 'database',
  pandas: 'database',
  'data-ai': 'brain',
  ai: 'brain',
  'machine-learning': 'brain',
  collaboration: 'workflow',
  'analysis-collaboration': 'workflow',
  'analysis-and-collaboration': 'workflow',
  'requirements-analysis': 'workflow',
  'clipboard-search': 'workflow',
  'layout-template': 'workflow',
  users: 'workflow',
  prototyping: 'workflow',
  'team-leadership': 'workflow',
  language: 'languages',
  languages: 'languages',
  tailwind: 'tailwindcss',
  'tailwind-css': 'tailwindcss',
  ts: 'typescript',
  x: 'twitter',
  'linked-in': 'linkedin',
  network: 'globe',
  networking: 'globe',
  'networking-basics': 'globe',
  csharp: 'code',
  'c-sharp': 'code',
} as const;
