import { NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { distinctUntilChanged } from 'rxjs/operators';
import { finalize, take } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { ContactMessageDraft } from '@domains/contact/model/contact-message.model';
import { ContactMethod } from '@domains/profile/model/contact-method.model';
import { Profile } from '@domains/profile/model/profile.model';
import { PublicContactApiService } from '@domains/contact/data/contact-api.service';
import { PublicProfileApiService } from '@domains/profile/data/profile-api.service';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';
import { createEmptyProfile } from '@domains/profile/lib/profile-view.util';

type SubmissionState = 'idle' | 'submitting' | 'success' | 'error';

@Component({
  selector: 'app-contact-page',
  standalone: true,
  imports: [NgFor, NgIf, ReactiveFormsModule, TranslatePipe, UiButtonComponent, UiCardComponent, UiChipComponent, UiEmptyStateComponent, UiSkeletonComponent],
  templateUrl: './contact.page.html'
})
export class ContactPageComponent implements OnInit {
  private readonly formBuilder = inject(NonNullableFormBuilder);
  private readonly contactApi = inject(PublicContactApiService);
  private readonly profileApi = inject(PublicProfileApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly siteTracking = inject(SiteTrackingService);
  private readonly i18n = inject(I18nService);
  private readonly destroyRef = inject(DestroyRef);

  protected profile: Profile = createEmptyProfile();
  protected contactMethods: ContactMethod[] = [];

  protected readonly contactForm = this.formBuilder.group({
    name: ['', [Validators.required, Validators.minLength(2)]],
    email: ['', [Validators.required, Validators.email]],
    subject: ['', [Validators.required, Validators.minLength(4)]],
    message: ['', [Validators.required, Validators.minLength(20), Validators.maxLength(1200)]],
    website: ['']
  });

  protected hasAttemptedSubmit = false;
  protected submissionState: SubmissionState = 'idle';
  protected errorMessage = '';
  protected profileErrorMessage = '';
  protected lastSubmittedMessage: ContactMessageDraft | null = null;
  protected isLoadingProfile = true;

  ngOnInit(): void {
    this.i18n.localeChanges$.pipe(distinctUntilChanged(), takeUntilDestroyed(this.destroyRef)).subscribe(() => {
      this.loadProfile();
    });
  }

  protected submit(): void {
    this.hasAttemptedSubmit = true;
    this.contactForm.markAllAsTouched();

    if (this.contactForm.invalid || this.submissionState === 'submitting') {
      return;
    }

    this.submissionState = 'submitting';
    this.errorMessage = '';

    const payload = this.buildDraft();

    this.contactApi
      .submitContactMessage(payload)
      .pipe(
        take(1),
        finalize(() => this.changeDetectorRef.detectChanges())
      )
      .subscribe({
        next: (response) => {
          this.submissionState = 'success';
          this.lastSubmittedMessage = {
            name: response.item.name,
            email: response.item.email,
            subject: response.item.subject,
            message: response.item.message,
            sourcePage: response.item.sourcePage
          };
          this.contactForm.reset();
          this.contactForm.markAsPristine();
          this.contactForm.markAsUntouched();
          this.hasAttemptedSubmit = false;
        },
        error: (error) => {
          this.submissionState = 'error';
          this.errorMessage = error?.error?.detail || this.i18n.translate('pages.contact.errors.submit');
        }
      });
  }

  protected resetForm(): void {
    this.contactForm.reset();
    this.contactForm.markAsPristine();
    this.contactForm.markAsUntouched();
    this.hasAttemptedSubmit = false;
    this.submissionState = 'idle';
    this.errorMessage = '';
  }

  protected startAnotherMessage(): void {
    this.lastSubmittedMessage = null;
    this.submissionState = 'idle';
    this.errorMessage = '';
    this.hasAttemptedSubmit = false;
  }

  protected get messageLength(): number {
    return this.contactForm.controls.message.value.length;
  }

  protected get contactIntroText(): string {
    return this.i18n.translate('pages.contact.intro');
  }

  protected get hasContactDetails(): boolean {
    return Boolean(this.contactMethods.length || this.profile.availability.length || this.profile.location);
  }

  protected get primaryContactMethods(): ContactMethod[] {
    const preferredPlatforms = new Set(['email', 'phone']);
    const preferredMethods = this.contactMethods.filter((method) => preferredPlatforms.has(method.platform));

    return (preferredMethods.length ? preferredMethods : this.contactMethods).slice(0, 2);
  }

  protected get secondaryContactMethods(): ContactMethod[] {
    const primaryIds = new Set(this.primaryContactMethods.map((method) => method.id));
    return this.contactMethods.filter((method) => !primaryIds.has(method.id));
  }

  protected get hasSupplementaryContactMethods(): boolean {
    return this.secondaryContactMethods.length > 0;
  }

  protected isExternalContactMethod(method: ContactMethod): boolean {
    return !(method.href.startsWith('mailto:') || method.href.startsWith('tel:'));
  }

  protected contactMethodMonogram(method: ContactMethod): string {
    const lookup: Record<string, string> = {
      email: 'EM',
      phone: 'PH',
      github: 'GH',
      linkedin: 'LI',
      location: 'LO',
    };

    return lookup[method.platform] ?? method.label.slice(0, 2).toUpperCase();
  }

  protected showError(controlName: 'name' | 'email' | 'subject' | 'message'): boolean {
    const control = this.contactForm.controls[controlName];
    return control.invalid && (control.touched || this.hasAttemptedSubmit);
  }

  protected errorText(controlName: 'name' | 'email' | 'subject' | 'message'): string {
    const control = this.contactForm.controls[controlName];

    if (control.hasError('required')) {
      const labels = {
        name: 'pages.contact.validation.nameRequired',
        email: 'pages.contact.validation.emailRequired',
        subject: 'pages.contact.validation.subjectRequired',
        message: 'pages.contact.validation.messageRequired'
      } as const;

      return this.i18n.translate(labels[controlName]);
    }

    if (control.hasError('email')) {
      return this.i18n.translate('pages.contact.validation.emailInvalid');
    }

    if (control.hasError('minlength')) {
      const labels = {
        name: 'pages.contact.validation.nameMinLength',
        email: 'pages.contact.validation.emailInvalid',
        subject: 'pages.contact.validation.subjectMinLength',
        message: 'pages.contact.validation.messageMinLength'
      } as const;

      return this.i18n.translate(labels[controlName]);
    }

    if (control.hasError('maxlength')) {
      return this.i18n.translate('pages.contact.validation.messageMaxLength');
    }

    return '';
  }

  protected get isSubmitDisabled(): boolean {
    return this.submissionState === 'submitting';
  }

  protected loadProfile(): void {
    this.isLoadingProfile = true;
    this.profileErrorMessage = '';
    this.profile = createEmptyProfile();
    this.contactMethods = [];

    forkJoin({
      profile: this.profileApi.getProfile().pipe(take(1)),
      shell: this.profileApi.getSiteShell().pipe(take(1)),
    })
      .pipe(
        finalize(() => {
          this.isLoadingProfile = false;
          this.changeDetectorRef.detectChanges();
        })
      )
      .subscribe({
        next: ({ profile, shell }) => {
          this.profile = profile;
          this.contactMethods = shell.contactMethods;
        },
        error: () => {
          this.profile = createEmptyProfile();
          this.contactMethods = [];
          this.profileErrorMessage = this.i18n.translate('pages.contact.errors.profileLoad');
        }
      });
  }

  private buildDraft(): ContactMessageDraft {
    const value = this.contactForm.getRawValue();

    return {
      name: value.name.trim(),
      email: value.email.trim(),
      subject: value.subject.trim(),
      message: value.message.trim(),
      sourcePage: '/contact',
      visitorId: this.siteTracking.visitorId,
      sessionId: this.siteTracking.sessionId,
      website: value.website?.trim() || ''
    };
  }
}
