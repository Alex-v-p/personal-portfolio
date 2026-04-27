import { Routes } from '@angular/router';

import { localeMatcher } from '@core/routing/locale.matcher';
import { adminAuthGuard, adminGuestGuard, adminMfaGuard } from './shared/guards/admin-auth.guard';

const publicRoutes: Routes = [
  {
    path: '',
    loadComponent: () => import('@domains/home/feature/home.page').then((module) => module.HomePageComponent),
    data: {
      titleKey: 'routes.home.title',
      seo: {
        titleKey: 'routes.home.title',
        descriptionKey: 'routes.home.description',
        keywordsKey: 'routes.home.keywords',
        type: 'profile',
      },
    },
  },
  {
    path: 'projects',
    loadComponent: () => import('@domains/projects/feature/projects.page').then((module) => module.ProjectsPageComponent),
    data: {
      titleKey: 'routes.projects.title',
      seo: {
        titleKey: 'routes.projects.title',
        descriptionKey: 'routes.projects.description',
        keywordsKey: 'routes.projects.keywords',
      },
    },
  },
  {
    path: 'blog',
    loadComponent: () => import('@domains/blog/feature/blog.page').then((module) => module.BlogPageComponent),
    data: {
      titleKey: 'routes.blog.title',
      seo: {
        titleKey: 'routes.blog.title',
        descriptionKey: 'routes.blog.description',
        keywordsKey: 'routes.blog.keywords',
        type: 'website',
      },
    },
  },
  {
    path: 'blog/:slug',
    loadComponent: () => import('@domains/blog/feature/blog-post.page').then((module) => module.BlogPostPageComponent),
    data: {
      titleKey: 'routes.blogPost.title',
      seo: {
        titleKey: 'routes.blogPost.title',
        descriptionKey: 'routes.blogPost.description',
        keywordsKey: 'routes.blogPost.keywords',
        type: 'article',
      },
    },
  },
  {
    path: 'contact',
    loadComponent: () => import('@domains/contact/feature/contact.page').then((module) => module.ContactPageComponent),
    data: {
      titleKey: 'routes.contact.title',
      seo: {
        titleKey: 'routes.contact.title',
        descriptionKey: 'routes.contact.description',
        keywordsKey: 'routes.contact.keywords',
      },
    },
  },
  {
    path: 'stats',
    loadComponent: () => import('@domains/stats/feature/stats.page').then((module) => module.StatsPageComponent),
    data: {
      titleKey: 'routes.stats.title',
      seo: {
        titleKey: 'routes.stats.title',
        descriptionKey: 'routes.stats.description',
        keywordsKey: 'routes.stats.keywords',
      },
    },
  },
  {
    path: 'assistant',
    loadComponent: () => import('@domains/assistant/feature/assistant.page').then((module) => module.AssistantPageComponent),
    data: {
      titleKey: 'routes.assistant.title',
      seo: {
        titleKey: 'routes.assistant.title',
        descriptionKey: 'routes.assistant.description',
        keywordsKey: 'routes.assistant.keywords',
      },
    },
  },
  { path: '**', redirectTo: '' },
];

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'en' },
  {
    path: 'admin/login',
    loadComponent: () => import('@domains/admin/auth/feature/admin-login.page').then((module) => module.AdminLoginPageComponent),
    title: 'CMS Login',
    canActivate: [adminGuestGuard],
    data: {
      seo: {
        title: 'CMS Login',
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
        title: 'CMS MFA',
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
        title: 'Portfolio CMS',
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
        path: 'backup',
        loadComponent: () => import('@domains/admin/backup/feature/admin-backup.page').then((module) => module.AdminBackupPageComponent),
        title: 'Admin Backup',
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
    matcher: localeMatcher,
    children: publicRoutes,
  },
  { path: '**', redirectTo: 'en' },
];
