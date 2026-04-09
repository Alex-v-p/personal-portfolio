import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="min-h-screen grid grid-rows-[auto_1fr_auto] text-stone-900">
      <header class="sticky top-0 z-20 pt-4 backdrop-blur supports-[backdrop-filter]:bg-transparent">
        <div class="mx-auto flex w-[min(72rem,calc(100vw-2rem))] flex-col gap-4 rounded-[1.75rem] border border-stone-200/80 bg-white/85 p-4 shadow-[0_18px_40px_rgba(40,31,20,0.08)] lg:flex-row lg:items-center lg:justify-between lg:rounded-full lg:px-4 lg:py-3">
          <a class="inline-flex min-w-0 items-center gap-3.5" routerLink="/" aria-label="Go to home page">
            <span class="h-10 w-10 shrink-0 rounded-full border border-stone-300 bg-gradient-to-br from-stone-200 to-stone-300" aria-hidden="true"></span>
            <span class="min-w-0">
              <strong class="block text-sm font-semibold tracking-tight text-stone-900 sm:text-base">Alex van Poppel</strong>
              <small class="block text-xs text-stone-500 sm:text-sm">Software engineer portfolio</small>
            </span>
          </a>

          <nav class="flex flex-wrap gap-2" aria-label="Primary">
            <a
              class="rounded-full border border-transparent px-4 py-3 text-sm font-semibold text-stone-500 transition hover:-translate-y-0.5 hover:border-stone-300 hover:bg-white hover:text-stone-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400"
              routerLink="/"
              routerLinkActive="border-stone-300 bg-stone-100 text-stone-900 shadow-sm"
              [routerLinkActiveOptions]="{ exact: true }"
            >
              Home
            </a>
            <a
              class="rounded-full border border-transparent px-4 py-3 text-sm font-semibold text-stone-500 transition hover:-translate-y-0.5 hover:border-stone-300 hover:bg-white hover:text-stone-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400"
              routerLink="/projects"
              routerLinkActive="border-stone-300 bg-stone-100 text-stone-900 shadow-sm"
            >
              Projects
            </a>
            <a
              class="rounded-full border border-transparent px-4 py-3 text-sm font-semibold text-stone-500 transition hover:-translate-y-0.5 hover:border-stone-300 hover:bg-white hover:text-stone-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400"
              routerLink="/blog"
              routerLinkActive="border-stone-300 bg-stone-100 text-stone-900 shadow-sm"
            >
              Blog
            </a>
            <a
              class="rounded-full border border-transparent px-4 py-3 text-sm font-semibold text-stone-500 transition hover:-translate-y-0.5 hover:border-stone-300 hover:bg-white hover:text-stone-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400"
              routerLink="/contact"
              routerLinkActive="border-stone-300 bg-stone-100 text-stone-900 shadow-sm"
            >
              Contact
            </a>
            <a
              class="rounded-full border border-transparent px-4 py-3 text-sm font-semibold text-stone-500 transition hover:-translate-y-0.5 hover:border-stone-300 hover:bg-white hover:text-stone-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400"
              routerLink="/stats"
              routerLinkActive="border-stone-300 bg-stone-100 text-stone-900 shadow-sm"
            >
              Stats
            </a>
          </nav>
        </div>
      </header>

      <main class="py-12 md:py-14 lg:py-16">
        <div class="mx-auto w-[min(72rem,calc(100vw-2rem))]">
          <router-outlet></router-outlet>
        </div>
      </main>

      <footer class="border-t border-stone-200/80 bg-stone-200/35 py-10">
        <div class="mx-auto grid w-[min(72rem,calc(100vw-2rem))] gap-6 md:grid-cols-3">
          <section class="space-y-3">
            <p class="text-sm font-semibold text-stone-900">Alex van Poppel</p>
            <p class="max-w-[32ch] text-sm leading-7 text-stone-600">
              Portfolio shell aligned to the low-fi wireframes, ready for page content in the next stages.
            </p>
          </section>

          <section class="space-y-3">
            <p class="text-sm font-semibold text-stone-900">Quick links</p>
            <div class="grid gap-2 text-sm text-stone-600">
              <a class="transition hover:text-stone-900 focus-visible:outline-none focus-visible:text-stone-900" routerLink="/">Home</a>
              <a class="transition hover:text-stone-900 focus-visible:outline-none focus-visible:text-stone-900" routerLink="/projects">Projects</a>
              <a class="transition hover:text-stone-900 focus-visible:outline-none focus-visible:text-stone-900" routerLink="/blog">Blog</a>
              <a class="transition hover:text-stone-900 focus-visible:outline-none focus-visible:text-stone-900" routerLink="/contact">Contact</a>
              <a class="transition hover:text-stone-900 focus-visible:outline-none focus-visible:text-stone-900" routerLink="/stats">Stats</a>
            </div>
          </section>

          <section class="space-y-3">
            <p class="text-sm font-semibold text-stone-900">Stage 1 status</p>
            <p class="max-w-[32ch] text-sm leading-7 text-stone-600">
              Global layout, shared UI primitives, and route placeholders are now in place.
            </p>
          </section>
        </div>
      </footer>
    </div>
  `
})
export class AppShellComponent {}
