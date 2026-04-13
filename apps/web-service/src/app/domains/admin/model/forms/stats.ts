import { AdminGithubSnapshot } from '@domains/admin/model/admin.model';

export interface AdminGithubSnapshotForm {
  id?: string | null;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount: number | null;
  followingCount: number | null;
  totalStars: number | null;
  totalCommits: number | null;
  rawPayloadText: string;
  contributionDaysText: string;
}

export function createEmptyGithubSnapshotForm(): AdminGithubSnapshotForm {
  return {
    snapshotDate: '',
    username: 'Alex-v-p',
    publicRepoCount: 0,
    followersCount: null,
    followingCount: null,
    totalStars: null,
    totalCommits: null,
    rawPayloadText: '',
    contributionDaysText: '[]'
  };
}

export function toGithubSnapshotForm(snapshot: AdminGithubSnapshot): AdminGithubSnapshotForm {
  return {
    id: snapshot.id,
    snapshotDate: snapshot.snapshotDate,
    username: snapshot.username,
    publicRepoCount: snapshot.publicRepoCount,
    followersCount: snapshot.followersCount ?? null,
    followingCount: snapshot.followingCount ?? null,
    totalStars: snapshot.totalStars ?? null,
    totalCommits: snapshot.totalCommits ?? null,
    rawPayloadText: snapshot.rawPayload ? JSON.stringify(snapshot.rawPayload, null, 2) : '',
    contributionDaysText: JSON.stringify(snapshot.contributionDays, null, 2),
  };
}
