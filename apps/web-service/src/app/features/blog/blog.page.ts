import { Component } from '@angular/core';

@Component({
  selector: 'app-blog-page',
  standalone: true,
  template: `
    <section class="page-card">
      <p class="eyebrow">Blog</p>
      <h1>Blog page</h1>
      <p>Connect this page to blog listing and blog detail routes later.</p>
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
export class BlogPageComponent {}
