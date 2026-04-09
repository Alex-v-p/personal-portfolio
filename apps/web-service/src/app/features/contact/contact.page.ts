import { NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { CONTACT_METHODS } from '../../shared/mock-data/contact-links.mock';
import { PROFILE } from '../../shared/mock-data/profile.mock';
import { ContactMessageDraft } from '../../shared/models/contact-message.model';

interface ContactTopic {
  label: string;
  hint: string;
}

type SubmissionState = 'idle' | 'submitting' | 'success' | 'error';

@Component({
  selector: 'app-contact-page',
  standalone: true,
  imports: [NgFor, NgIf, ReactiveFormsModule, UiButtonComponent, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './contact.page.html'
})
export class ContactPageComponent {
  private readonly formBuilder = inject(NonNullableFormBuilder);

  protected readonly profile = PROFILE;
  protected readonly contactMethods = CONTACT_METHODS;
  protected readonly preferredTopics: ContactTopic[] = [
    { label: 'Internships', hint: 'Questions about availability, timing, and current study status.' },
    { label: 'Freelance work', hint: 'Small product sites, portfolio builds, or front-end feature work.' },
    { label: 'Collaboration', hint: 'Student projects, hackathons, or longer-term side projects.' },
    { label: 'Speaking or demos', hint: 'School events, portfolio walkthroughs, or project presentations.' }
  ];

  protected readonly contactForm = this.formBuilder.group({
    name: ['', [Validators.required, Validators.minLength(2)]],
    email: ['', [Validators.required, Validators.email]],
    subject: ['', [Validators.required, Validators.minLength(4)]],
    message: ['', [Validators.required, Validators.minLength(20), Validators.maxLength(1200)]]
  });

  protected hasAttemptedSubmit = false;
  protected submissionState: SubmissionState = 'idle';
  protected errorMessage = '';
  protected lastSubmittedMessage: ContactMessageDraft | null = null;

  protected submit(previewError = false): void {
    this.hasAttemptedSubmit = true;
    this.contactForm.markAllAsTouched();

    if (this.contactForm.invalid || this.submissionState === 'submitting') {
      return;
    }

    this.submissionState = 'submitting';
    this.errorMessage = '';

    const payload = this.buildDraft();

    window.setTimeout(() => {
      if (previewError) {
        this.submissionState = 'error';
        this.errorMessage = 'The mock submission failed on purpose so the error-state UI can be reviewed before the backend exists.';
        return;
      }

      this.submissionState = 'success';
      this.lastSubmittedMessage = payload;
      this.contactForm.reset();
      this.contactForm.markAsPristine();
      this.contactForm.markAsUntouched();
      this.hasAttemptedSubmit = false;
    }, 850);
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

  protected useTopic(label: string): void {
    const subjectControl = this.contactForm.controls.subject;

    if (!subjectControl.value.trim()) {
      subjectControl.setValue(label);
    }

    subjectControl.markAsDirty();
    subjectControl.markAsTouched();
  }

  protected get messageLength(): number {
    return this.contactForm.controls.message.value.length;
  }

  protected showError(controlName: 'name' | 'email' | 'subject' | 'message'): boolean {
    const control = this.contactForm.controls[controlName];
    return control.invalid && (control.touched || this.hasAttemptedSubmit);
  }

  protected errorText(controlName: 'name' | 'email' | 'subject' | 'message'): string {
    const control = this.contactForm.controls[controlName];

    if (control.hasError('required')) {
      const labels = {
        name: 'Please share your name.',
        email: 'Please share your email address.',
        subject: 'Please add a subject.',
        message: 'Please describe what you would like to discuss.'
      } as const;

      return labels[controlName];
    }

    if (control.hasError('email')) {
      return 'Please enter a valid email address.';
    }

    if (control.hasError('minlength')) {
      const labels = {
        name: 'Name should be at least 2 characters.',
        email: 'Please enter a valid email address.',
        subject: 'Subject should be at least 4 characters.',
        message: 'Message should be at least 20 characters so there is enough context.'
      } as const;

      return labels[controlName];
    }

    if (control.hasError('maxlength')) {
      return 'Message should stay under 1200 characters.';
    }

    return '';
  }

  protected get isSubmitDisabled(): boolean {
    return this.submissionState === 'submitting';
  }

  private buildDraft(): ContactMessageDraft {
    const value = this.contactForm.getRawValue();

    return {
      name: value.name.trim(),
      email: value.email.trim(),
      subject: value.subject.trim(),
      message: value.message.trim(),
      sourcePage: '/contact'
    };
  }
}
