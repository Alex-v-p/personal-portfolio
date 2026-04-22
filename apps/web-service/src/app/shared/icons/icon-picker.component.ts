import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { getIconDefinition, getOrderedIconOptions } from './icon-registry';
import type { IconGroupKey, IconOption } from './icon.types';
import { UiIconComponent } from './ui-icon.component';

interface IconOptionGroupView {
  key: IconGroupKey;
  label: string;
  options: IconOption[];
}

@Component({
  selector: 'app-icon-picker',
  standalone: true,
  imports: [CommonModule, FormsModule, UiIconComponent],
  template: `
    <div class="space-y-3">
      <div class="flex flex-wrap items-start gap-3 rounded-[1.25rem] border border-stone-300 bg-white p-3">
        <div class="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-stone-200 bg-stone-50 text-stone-700">
          <app-ui-icon [name]="value" [fallbackText]="fallbackText || placeholder" size="md"></app-ui-icon>
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-sm font-semibold text-stone-900">{{ selectedLabel || 'No icon selected' }}</p>
          <p class="mt-1 text-xs leading-5 text-stone-500">
            {{ selectedKeyText || placeholder }}
          </p>
        </div>
        <button
          *ngIf="value"
          type="button"
          (click)="clearSelection()"
          class="inline-flex min-h-10 items-center rounded-full border border-stone-300 px-4 text-sm font-semibold text-stone-700 transition hover:bg-stone-50"
        >
          Clear
        </button>
      </div>

      <label class="block space-y-2">
        <span class="text-sm font-semibold text-stone-800">Search icons</span>
        <input
          [(ngModel)]="searchTerm"
          type="search"
          [placeholder]="searchPlaceholder"
          class="w-full rounded-2xl border border-stone-300 bg-white px-4 py-3 text-sm"
        />
      </label>

      <div class="max-h-72 space-y-3 overflow-y-auto rounded-[1.25rem] border border-stone-300 bg-white p-3">
        <ng-container *ngIf="filteredGroups.length; else noMatches">
          <section *ngFor="let group of filteredGroups" class="space-y-2">
            <div class="flex items-center justify-between gap-3 px-1">
              <p class="text-xs font-semibold uppercase tracking-[0.16em] text-stone-500">{{ group.label }}</p>
              <span class="text-[11px] text-stone-400">{{ group.options.length }} option{{ group.options.length === 1 ? '' : 's' }}</span>
            </div>
            <div class="grid gap-2 sm:grid-cols-2">
              <button
                *ngFor="let option of group.options"
                type="button"
                (click)="selectOption(option.key)"
                [ngClass]="option.key === normalizedValue ? 'border-stone-900 bg-stone-100 text-stone-950' : 'border-stone-200 bg-stone-50 text-stone-700 hover:bg-stone-100'"
                class="flex min-h-12 items-center gap-3 rounded-2xl border px-3 py-3 text-left transition"
              >
                <span class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-current/10 bg-white/80">
                  <app-ui-icon [name]="option.key" [fallbackText]="option.label" size="sm"></app-ui-icon>
                </span>
                <span class="min-w-0">
                  <span class="block truncate text-sm font-semibold">{{ option.label }}</span>
                  <span class="block truncate text-xs text-stone-500">{{ option.key }}</span>
                </span>
              </button>
            </div>
          </section>
        </ng-container>
      </div>

      <ng-template #noMatches>
        <div class="rounded-2xl border border-dashed border-stone-300 bg-stone-50 px-4 py-5 text-sm text-stone-500">
          No icons matched your search.
        </div>
      </ng-template>
    </div>
  `,
})
export class IconPickerComponent {
  private readonly orderedOptions = getOrderedIconOptions();

  @Input() value: string | null | undefined = null;
  @Output() readonly valueChange = new EventEmitter<string>();

  @Input() groups: readonly IconGroupKey[] | null = null;
  @Input() placeholder = 'Choose an icon key for this item.';
  @Input() fallbackText: string | null = null;
  @Input() searchPlaceholder = 'Search by label, key, or keyword';

  protected searchTerm = '';

  protected readonly groupLabels: Record<IconGroupKey, string> = {
    social: 'Social',
    contact: 'Contact',
    expertise: 'Expertise & generic',
    tech: 'Technology',
  };

  protected get normalizedValue(): string {
    return (this.value ?? '').trim().toLowerCase();
  }

  protected get selectedLabel(): string | null {
    return getIconDefinition(this.value)?.label ?? null;
  }

  protected get selectedKeyText(): string | null {
    return this.value?.trim() || null;
  }

  protected get filteredGroups(): IconOptionGroupView[] {
    const normalizedSearch = this.searchTerm.trim().toLowerCase();
    const activeGroups = this.groups?.length ? [...this.groups] : (Object.keys(this.groupLabels) as IconGroupKey[]);

    return activeGroups
      .map((groupKey) => {
        const options = this.orderedOptions[groupKey].filter((option) => this.matchesSearch(option, normalizedSearch));
        return {
          key: groupKey,
          label: this.groupLabels[groupKey],
          options,
        } satisfies IconOptionGroupView;
      })
      .filter((group) => group.options.length > 0);
  }

  protected selectOption(iconKey: string): void {
    this.valueChange.emit(iconKey);
  }

  protected clearSelection(): void {
    this.valueChange.emit('');
  }

  private matchesSearch(option: IconOption, normalizedSearch: string): boolean {
    if (!normalizedSearch) {
      return true;
    }

    const haystacks = [
      option.label,
      option.key,
      this.groupLabels[option.group],
      ...(option.keywords ?? []),
    ];

    return haystacks.some((entry) => entry.toLowerCase().includes(normalizedSearch));
  }
}
