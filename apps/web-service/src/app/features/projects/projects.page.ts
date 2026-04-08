import { Component } from '@angular/core';

@Component({
  selector: 'app-projects-page',
  standalone: true,
  template: `
    <section class="page-card">
      <p class="eyebrow">Projects</p>
      <h1>Projects page</h1>
      <p>Hook this page up to the portfolio API projects endpoints when you are ready.</p>
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
export class ProjectsPageComponent {}
