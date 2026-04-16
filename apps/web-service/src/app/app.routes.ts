import { Routes } from '@angular/router';

import { adminAuthGuard, adminGuestGuard, adminMfaGuard } from './shared/guards/admin-auth.guard';

export const routes: Routes = [
  {
    path: 'admin/login',
    loadComponent: () => import('@domains/admin/auth/feature/admin-login.page').then((module) => module.AdminLoginPageComponent),
    title: 'CMS Login',
    canActivate: [adminGuestGuard],
    data: {
      seo: {
        description: 'Secure sign-in for the portfolio content management system.',
        keywords: ['portfolio CMS', 'admin login'],
        noIndex: true,
      },
    },
  },
  {
    path: 'admin/mfa',
    loadComponent: () => import('@domains/admin/auth/feature/admin-mfa.page').then((module) => module.AdminMfaPageComponent),
    title: 'CMS MFA',
    canActivate: [adminMfaGuard],
    data: {
      seo: {
        description: 'Two-factor authentication for the portfolio content management system.',
        keywords: ['portfolio CMS', 'admin MFA'],
        noIndex: true,
      },
    },
  },
  {
    path: 'admin',
    loadComponent: () => import('@domains/admin/shell/layout/admin-shell.layout').then((module) => module.AdminShellLayoutComponent),
    title: 'Portfolio CMS',
    canActivate: [adminAuthGuard],
    data: {
      seo: {
        description: 'Private content management workspace for the portfolio site.',
        keywords: ['portfolio CMS', 'admin'],
        noIndex: true,
      },
    },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'overview' },
      {
        path: 'overview',
        loadComponent: () => import('@domains/admin/overview/feature/admin-overview.page').then((module) => module.AdminOverviewPageComponent),
        title: 'Admin Overview',
      },
      {
        path: 'messages',
        loadComponent: () => import('@domains/admin/messages/feature/admin-messages.page').then((module) => module.AdminMessagesPageComponent),
        title: 'Admin Messages',
      },
      {
        path: 'projects',
        loadComponent: () => import('@domains/admin/shell/feature/admin-legacy-tab.page').then((module) => module.AdminLegacyTabPageComponent),
        title: 'Admin Projects',
        data: { legacyTab: 'projects' },
      },
      {
        path: 'blog',
        loadComponent: () => import('@domains/admin/blog/feature/admin-blog.page').then((module) => module.AdminBlogPageComponent),
        title: 'Admin Blog',
      },
      {
        path: 'media',
        loadComponent: () => import('@domains/admin/media/feature/admin-media.page').then((module) => module.AdminMediaPageComponent),
        title: 'Admin Media',
      },
      {
        path: 'taxonomy',
        loadComponent: () => import('@domains/admin/shell/feature/admin-legacy-tab.page').then((module) => module.AdminLegacyTabPageComponent),
        title: 'Admin Taxonomy',
        data: { legacyTab: 'taxonomy' },
      },
      {
        path: 'experience',
        loadComponent: () => import('@domains/admin/shell/feature/admin-legacy-tab.page').then((module) => module.AdminLegacyTabPageComponent),
        title: 'Admin Experience',
        data: { legacyTab: 'experience' },
      },
      {
        path: 'navigation',
        loadComponent: () => import('@domains/admin/shell/feature/admin-legacy-tab.page').then((module) => module.AdminLegacyTabPageComponent),
        title: 'Admin Navigation',
        data: { legacyTab: 'navigation' },
      },
      {
        path: 'profile',
        loadComponent: () => import('@domains/admin/profile/feature/admin-profile.page').then((module) => module.AdminProfilePageComponent),
        title: 'Admin Profile',
      },
      {
        path: 'stats',
        loadComponent: () => import('@domains/admin/stats/feature/admin-stats.page').then((module) => module.AdminStatsPageComponent),
        title: 'Admin GitHub / Stats',
      },
      {
        path: 'assistant',
        loadComponent: () => import('@domains/admin/assistant/feature/admin-assistant.page').then((module) => module.AdminAssistantPageComponent),
        title: 'Admin Assistant',
      },
      {
        path: 'activity',
        loadComponent: () => import('@domains/admin/activity/feature/admin-activity.page').then((module) => module.AdminActivityPageComponent),
        title: 'Admin Activity',
      },
      {
        path: 'admins',
        loadComponent: () => import('@domains/admin/shell/feature/admin-legacy-tab.page').then((module) => module.AdminLegacyTabPageComponent),
        title: 'Admin Users',
        data: { legacyTab: 'admins' },
      },
      {
        path: '**',
        redirectTo: '/',
      },
    ],
  },
  {
    path: '',
    loadComponent: () => import('@domains/home/feature/home.page').then((module) => module.HomePageComponent),
    title: 'Home',
    data: {
      seo: {
        description: 'Explore selected projects, experience, blog posts, and contact details from the portfolio of Alex van Poppel.',
        keywords: ['Alex van Poppel', 'portfolio home', 'featured projects', 'experience', 'blog'],
        type: 'profile',
      },
    },
  },
  {
    path: 'projects',
    loadComponent: () => import('@domains/projects/feature/projects.page').then((module) => module.ProjectsPageComponent),
    title: 'Projects',
    data: {
      seo: {
        description: 'Browse practical software, web, and data projects built by Alex van Poppel, with technology filters and featured work.',
        keywords: ['projects', 'portfolio projects', 'Angular', 'Laravel', 'Python', 'software projects'],
      },
    },
  },
  {
    path: 'blog',
    loadComponent: () => import('@domains/blog/feature/blog.page').then((module) => module.BlogPageComponent),
    title: 'Blog posts',
    data: {
      seo: {
        description: 'Read notes on portfolio building, architecture, client workshops, hardware, and software lessons from current and past projects.',
        keywords: ['blog', 'portfolio blog', 'architecture', 'analysis', 'hardware', 'software lessons'],
        type: 'website',
      },
    },
  },
  {
    path: 'blog/:slug',
    loadComponent: () => import('@domains/blog/feature/blog-post.page').then((module) => module.BlogPostPageComponent),
    title: 'Blog post',
    data: {
      seo: {
        description: 'Read an article from the portfolio blog of Alex van Poppel.',
        keywords: ['portfolio blog', 'article'],
        type: 'article',
      },
    },
  },
  {
    path: 'contact',
    loadComponent: () => import('@domains/contact/feature/contact.page').then((module) => module.ContactPageComponent),
    title: 'Contact',
    data: {
      seo: {
        description: 'Use the contact form or public links to get in touch about internships, freelance work, collaboration, or portfolio questions.',
        keywords: ['contact', 'internship', 'freelance', 'collaboration', 'email'],
      },
    },
  },
  {
    path: 'stats',
    loadComponent: () => import('@domains/stats/feature/stats.page').then((module) => module.StatsPageComponent),
    title: 'Stats',
    data: {
      seo: {
        description: 'View GitHub contribution activity, portfolio views, and engagement metrics from the public portfolio.',
        keywords: ['GitHub stats', 'portfolio views', 'engagement', 'contributions'],
      },
    },
  },
  {
    path: 'assistant',
    loadComponent: () => import('@domains/assistant/feature/assistant.page').then((module) => module.AssistantPageComponent),
    title: 'Portfolio Assistant',
    data: {
      seo: {
        description: 'Ask the portfolio assistant about projects, blog posts, experience, and the overall site.',
        keywords: ['assistant', 'portfolio assistant', 'projects', 'blog', 'experience'],
      },
    },
  },
  { path: '**', redirectTo: '' },
];
