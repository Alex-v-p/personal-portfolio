import { TestBed } from '@angular/core/testing';
import { from, of, throwError } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ContactPageComponent } from './contact.page';
import { PublicProfileApiService } from '@domains/profile/data/profile-api.service';
import { PublicContactApiService } from '@domains/contact/data/contact-api.service';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';
import { Profile } from '@domains/profile/model/profile.model';

const profileFixture: Profile = {
  id: 'profile-1',
  firstName: 'Alex',
  lastName: 'van Poppel',
  name: 'Alex van Poppel',
  headline: 'Software Engineer',
  role: 'Software Engineer',
  greeting: "Hi, I'm Alex",
  location: 'Belgium',
  email: 'hello@example.com',
  phone: '+32 000 000',
  shortIntro: 'Builder',
  longBio: 'Long bio',
  heroTitle: 'I’m Software Engineer',
  summary: 'Builder',
  shortBio: 'Long bio',
  footerDescription: 'Footer',
  avatarFileId: null,
  heroImageFileId: null,
  resumeFileId: null,
  avatarUrl: '',
  heroImageUrl: '',
  resumeUrl: '',
  skills: ['Angular', 'FastAPI'],
  expertiseGroups: [{ title: 'Core stack', tags: ['Angular', 'FastAPI'], skills: [{ name: 'Angular', yearsOfExperience: 1 }, { name: 'FastAPI', yearsOfExperience: 3 }] }],
  introParagraphs: ['Builder'],
  availability: ['Open to internships'],
  heroActions: [],
  socialLinks: [],
  createdAt: '2026-04-13T10:00:00Z',
  updatedAt: '2026-04-13T10:00:00Z',
};

describe('ContactPageComponent', () => {
  beforeEach(() => {
    TestBed.resetTestingModule();
  });

  it('loads profile contact methods on init and submits a contact message successfully', async () => {
    const submitContactMessage = vi.fn().mockReturnValue(
      of({
        message: 'Contact message created.',
        item: {
          id: 'message-1',
          name: 'Alex',
          email: 'alex@example.com',
          subject: 'Internship',
          message: 'I would like to discuss an internship opportunity with you.',
          sourcePage: '/contact',
          isRead: false,
          createdAt: '2026-04-13T10:00:00Z',
          updatedAt: '2026-04-13T10:00:00Z',
        },
      })
    );

    TestBed.configureTestingModule({
      imports: [ContactPageComponent],
      providers: [
        {
          provide: PublicProfileApiService,
          useValue: {
            getProfile: () => from(Promise.resolve(profileFixture)),
          },
        },
        {
          provide: PublicContactApiService,
          useValue: { submitContactMessage },
        },
        {
          provide: SiteTrackingService,
          useValue: {
            visitorId: 'visitor-1',
            sessionId: 'session-1',
          },
        },
      ],
    });

    const fixture = TestBed.createComponent(ContactPageComponent);
    const component = fixture.componentInstance as any;
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();

    expect(component.contactMethods.some((item: { platform: string }) => item.platform === 'email')).toBe(true);

    component.contactForm.setValue({
      name: 'Alex',
      email: 'alex@example.com',
      subject: 'Internship',
      message: 'I would like to discuss an internship opportunity with you.',
      website: '',
    });

    component.submit();

    expect(submitContactMessage).toHaveBeenCalledWith({
      name: 'Alex',
      email: 'alex@example.com',
      subject: 'Internship',
      message: 'I would like to discuss an internship opportunity with you.',
      sourcePage: '/contact',
      visitorId: 'visitor-1',
      sessionId: 'session-1',
      website: '',
    });
    expect(component.submissionState).toBe('success');
    expect(component.lastSubmittedMessage?.subject).toBe('Internship');
    expect(component.contactForm.pristine).toBe(true);
  });


  it('keeps the contact form available when profile details fail to load', async () => {
    TestBed.configureTestingModule({
      imports: [ContactPageComponent],
      providers: [
        {
          provide: PublicProfileApiService,
          useValue: {
            getProfile: () => throwError(() => ({ error: { detail: 'Profile unavailable' } })),
          },
        },
        {
          provide: PublicContactApiService,
          useValue: {
            submitContactMessage: () => of({
              message: 'Contact message created.',
              item: {
                id: 'message-2',
                name: 'Alex',
                email: 'alex@example.com',
                subject: 'Collaboration',
                message: 'I would like to collaborate on a project with you soon.',
                sourcePage: '/contact',
                isRead: false,
                createdAt: '2026-04-13T10:00:00Z',
                updatedAt: '2026-04-13T10:00:00Z',
              },
            }),
          },
        },
        {
          provide: SiteTrackingService,
          useValue: {
            visitorId: 'visitor-1',
            sessionId: 'session-1',
          },
        },
      ],
    });

    const fixture = TestBed.createComponent(ContactPageComponent);
    const component = fixture.componentInstance as any;
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();

    expect(component.profileErrorMessage).toContain('Contact details could not be loaded');
    expect(component.isLoadingProfile).toBe(false);

    component.contactForm.setValue({
      name: 'Alex',
      email: 'alex@example.com',
      subject: 'Collaboration',
      message: 'I would like to collaborate on a project with you soon.',
      website: '',
    });

    component.submit();

    expect(component.submissionState).toBe('success');
  });

  it('shows the API error detail when the submission fails', async () => {
    TestBed.configureTestingModule({
      imports: [ContactPageComponent],
      providers: [
        {
          provide: PublicProfileApiService,
          useValue: {
            getProfile: () => from(Promise.resolve(profileFixture)),
          },
        },
        {
          provide: PublicContactApiService,
          useValue: {
            submitContactMessage: () => throwError(() => ({ error: { detail: 'Too many messages were sent from this page recently.' } })),
          },
        },
        {
          provide: SiteTrackingService,
          useValue: {
            visitorId: 'visitor-1',
            sessionId: 'session-1',
          },
        },
      ],
    });

    const fixture = TestBed.createComponent(ContactPageComponent);
    const component = fixture.componentInstance as any;
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();

    component.contactForm.setValue({
      name: 'Alex',
      email: 'alex@example.com',
      subject: 'Internship',
      message: 'I would like to discuss an internship opportunity with you.',
      website: '',
    });

    component.submit();

    expect(component.submissionState).toBe('error');
    expect(component.errorMessage).toContain('Too many messages');
  });
});
