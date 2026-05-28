export type AdminAsyncTaskState = 'queued' | 'running' | 'succeeded' | 'failed';
export type AdminAsyncTaskType = 'github-refresh' | 'assistant-knowledge-rebuild';

export interface AdminAsyncTaskAccepted {
  taskId: string;
  taskType: AdminAsyncTaskType;
  status: AdminAsyncTaskState;
  pollAfterMs: number;
}

export interface AdminAsyncTaskStatus {
  taskId: string;
  taskType: AdminAsyncTaskType;
  status: AdminAsyncTaskState;
  submittedAt: string;
  startedAt?: string | null;
  completedAt?: string | null;
  errorMessage?: string | null;
  result?: Record<string, unknown> | null;
}
