import { Component } from '@angular/core';

@Component({
  selector: 'app-experience-page',
  standalone: true,
  template: `
    <section class="page-card">
      <p class="eyebrow">Experience</p>
      <h1>Experience page</h1>
      <p>Use this section for work experience, education, and skill timeline views.</p>
    </section>
  `,
  styles: [`
    .page-card {
      padding: 2rem;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 1rem;
      background: rgba(255,255,255,0.03);
    }

    .eyebrow {
      margin: 0 0 0.5rem;
      color: #8ab4ff;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 0.8rem;
    }

    h1 {
      margin-top: 0;
    }
  `]
})
export class ExperiencePageComponent {}
