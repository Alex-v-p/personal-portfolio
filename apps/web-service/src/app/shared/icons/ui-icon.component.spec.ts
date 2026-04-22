import { TestBed } from '@angular/core/testing';
import { describe, expect, it } from 'vitest';

import { UiIconComponent } from './ui-icon.component';

describe('UiIconComponent', () => {
  it('renders an svg for known icon keys', async () => {
    await TestBed.configureTestingModule({
      imports: [UiIconComponent],
    }).compileComponents();

    const fixture = TestBed.createComponent(UiIconComponent);
    fixture.componentInstance.name = 'github';
    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('svg')).not.toBeNull();
    expect(element.textContent?.trim()).toBe('');
  });

  it('falls back to initials for unknown icon keys', async () => {
    await TestBed.configureTestingModule({
      imports: [UiIconComponent],
    }).compileComponents();

    const fixture = TestBed.createComponent(UiIconComponent);
    fixture.componentInstance.name = 'unknown channel';
    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('svg')).toBeNull();
    expect(element.textContent?.trim()).toBe('UN');
  });
});
