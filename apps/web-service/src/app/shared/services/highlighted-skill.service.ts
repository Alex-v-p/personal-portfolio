import { Injectable, computed, inject, signal } from '@angular/core';
import { take } from 'rxjs/operators';

import { PublicProfileApiService } from '@domains/profile/data/profile-api.service';

@Injectable({ providedIn: 'root' })
export class HighlightedSkillService {
  private readonly profileApi = inject(PublicProfileApiService);
  private readonly highlightedNames = signal<Set<string>>(new Set());
  private readonly loaded = signal(false);

  constructor() {
    this.ensureLoaded();
  }

  readonly names = computed(() => this.highlightedNames());

  isHighlighted(name: string | null | undefined): boolean {
    if (!name) {
      return false;
    }

    return this.names().has(this.normalize(name));
  }

  private ensureLoaded(): void {
    if (this.loaded()) {
      return;
    }

    this.loaded.set(true);
    this.profileApi
      .getProfile()
      .pipe(take(1))
      .subscribe({
        next: (profile) => {
          const names = new Set(
            (profile.skills ?? [])
              .map((item) => this.normalize(item))
              .filter(Boolean)
          );

          this.highlightedNames.set(names);
        },
        error: () => {
          this.highlightedNames.set(new Set());
        }
      });
  }

  private normalize(value: string): string {
    return value.trim().toLowerCase();
  }
}
