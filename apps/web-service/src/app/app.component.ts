import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="shell">
      <header class="topbar">
        <a class="brand" routerLink="/">Personal Portfolio</a>
        <nav>
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">Home</a>
          <a routerLink="/projects" routerLinkActive="active">Projects</a>
          <a routerLink="/experience" routerLinkActive="active">Experience</a>
          <a routerLink="/blog" routerLinkActive="active">Blog</a>
          <a routerLink="/contact" routerLinkActive="active">Contact</a>
          <a routerLink="/assistant" routerLinkActive="active">Assistant</a>
        </nav>
      </header>

      <main class="content">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 1rem 2rem;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      background: rgba(8, 14, 28, 0.8);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
    }

    nav {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .brand {
      font-weight: 700;
      letter-spacing: 0.02em;
    }

    .active {
      color: #8ab4ff;
    }

    .content {
      width: min(1100px, calc(100vw - 2rem));
      margin: 0 auto;
      padding: 2rem 0 4rem;
    }
  `]
})
export class AppComponent {}
