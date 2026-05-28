import { AdminGithubContributionDay } from '@domains/admin/model/admin.model';

const slugCleanupPattern = /[^a-z0-9]+/g;

export function matchesSearch(values: Array<string | null | undefined>, needle: string): boolean {
  const searchNeedle = needle.trim().toLowerCase();
  if (!searchNeedle) {
    return true;
  }

  return values.some((value) => value?.toLowerCase().includes(searchNeedle));
}

export function toggleSelection(items: string[], value: string): string[] {
  return items.includes(value) ? items.filter((item) => item !== value) : [...items, value];
}

export function resolveSelection<T extends { id: string }>(currentId: string | null, items: T[]): string | null {
  if (!items.length) {
    return null;
  }

  return items.some((item) => item.id === currentId) ? currentId : items[0].id;
}

export function slugify(value: string): string {
  const cleaned = value.trim().toLowerCase().replace(slugCleanupPattern, '-').replace(/^-+|-+$/g, '');
  return cleaned || 'item';
}

export function parseJsonObject(raw: string): Record<string, unknown> | null {
  if (!raw.trim()) {
    return null;
  }

  const parsed = JSON.parse(raw) as unknown;
  if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') {
    throw new Error('GitHub raw payload must be a JSON object.');
  }

  return parsed as Record<string, unknown>;
}

export function parseContributionDays(raw: string): AdminGithubContributionDay[] {
  const parsed = JSON.parse(raw) as unknown;
  if (!Array.isArray(parsed)) {
    throw new Error('Contribution days must be a JSON array.');
  }

  return parsed.map((item) => ({
    date: String((item as { date?: unknown })?.date ?? ''),
    count: Number((item as { count?: unknown })?.count ?? 0),
    level: Number((item as { level?: unknown })?.level ?? 0),
  }));
}
