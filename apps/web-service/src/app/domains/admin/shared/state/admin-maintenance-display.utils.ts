import { AdminGithubAutoRefreshStatus } from '@domains/admin/model/admin.model';

const MINUTE_IN_SECONDS = 60;
const HOUR_IN_SECONDS = 60 * MINUTE_IN_SECONDS;
const DAY_IN_SECONDS = 24 * HOUR_IN_SECONDS;

export function formatCountdown(targetIso: string | null | undefined, nowMs: number, fallback = '—'): string {
  if (!targetIso) {
    return fallback;
  }

  const targetMs = Date.parse(targetIso);
  if (Number.isNaN(targetMs)) {
    return fallback;
  }

  const totalSeconds = Math.max(Math.ceil((targetMs - nowMs) / 1000), 0);
  if (totalSeconds === 0) {
    return 'now';
  }

  if (totalSeconds >= DAY_IN_SECONDS) {
    const days = Math.floor(totalSeconds / DAY_IN_SECONDS);
    const hours = Math.floor((totalSeconds % DAY_IN_SECONDS) / HOUR_IN_SECONDS);
    return hours > 0 ? `${days}d ${hours}h` : `${days}d`;
  }

  if (totalSeconds >= HOUR_IN_SECONDS) {
    const hours = Math.floor(totalSeconds / HOUR_IN_SECONDS);
    const minutes = Math.floor((totalSeconds % HOUR_IN_SECONDS) / MINUTE_IN_SECONDS);
    return minutes > 0 ? `${hours}h ${minutes}m` : `${hours}h`;
  }

  const minutes = Math.max(Math.ceil(totalSeconds / MINUTE_IN_SECONDS), 1);
  return `${minutes}m`;
}

export function retentionCountdownLabel(targetIso: string | null | undefined, nowMs: number): string {
  const countdown = formatCountdown(targetIso, nowMs);
  return countdown === 'now' ? 'Expires now' : `Expires in ${countdown}`;
}

export function retentionCountdownTone(targetIso: string | null | undefined, nowMs: number): string {
  if (!targetIso) {
    return 'border-stone-200 bg-white text-stone-700';
  }

  const targetMs = Date.parse(targetIso);
  if (Number.isNaN(targetMs)) {
    return 'border-stone-200 bg-white text-stone-700';
  }

  const totalSeconds = Math.max(Math.ceil((targetMs - nowMs) / 1000), 0);
  if (totalSeconds === 0) {
    return 'border-rose-200 bg-rose-50 text-rose-700';
  }
  if (totalSeconds <= DAY_IN_SECONDS) {
    return 'border-amber-200 bg-amber-50 text-amber-800';
  }
  return 'border-stone-200 bg-white text-stone-700';
}

export function githubRefreshLabel(status: AdminGithubAutoRefreshStatus, targetIso: string | null | undefined, nowMs: number): string {
  switch (status) {
    case 'manual_only':
      return 'Manual only';
    case 'disabled':
      return 'Auto refresh disabled';
    case 'retry_scheduled': {
      const countdown = formatCountdown(targetIso, nowMs, 'soon');
      return countdown === 'now' ? 'Retry due now' : `Retry in ${countdown}`;
    }
    case 'due':
      return 'Refresh due now';
    case 'scheduled': {
      const countdown = formatCountdown(targetIso, nowMs, 'soon');
      return countdown === 'now' ? 'Refresh due now' : `Refresh in ${countdown}`;
    }
    default:
      return 'Manual only';
  }
}

export function githubRefreshTone(status: AdminGithubAutoRefreshStatus, targetIso: string | null | undefined, nowMs: number): string {
  if (status === 'manual_only' || status === 'disabled') {
    return 'border-stone-200 bg-white text-stone-700';
  }
  if (status === 'retry_scheduled' || status === 'due') {
    return 'border-amber-200 bg-amber-50 text-amber-800';
  }

  return retentionCountdownTone(targetIso, nowMs);
}
