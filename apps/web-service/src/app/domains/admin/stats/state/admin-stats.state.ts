import { AdminGithubContributionDay, AdminGithubSnapshot } from '@domains/admin/model/admin.model';

export function contributionPreview(snapshot: AdminGithubSnapshot): string {
  return `${snapshot.contributionDays.length} day entries`;
}

export function parseGithubRawPayload(raw: string): Record<string, unknown> | null {
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
