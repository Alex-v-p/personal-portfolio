import { Routes } from '@angular/router';

import { adminAuthGuard, adminGuestGuard } from './shared/guards/admin-auth.guard';

export const routes: Routes = [
  {
    path: 'admin/login',
    loadComponent: () => import('@domains/admin/auth/feature/admin-login.page').then((module) => module.AdminLoginPageComponent),
    title: 'Admin Login',
    canActivate: [adminGuestGuard],
  },
  {
    path: 'admin',
    loadComponent: () => import('@domains/admin/shell/layout/admin-shell.layout').then((module) => module.AdminShellLayoutComponent),
    title: 'Admin CMS',
    canActivate: [adminAuthGuard],
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
    ],
  },
  {
    path: '',
    loadComponent: () => import('@domains/home/feature/home.page').then((module) => module.HomePageComponent),
    title: 'Home',
  },
  {
    path: 'projects',
    loadComponent: () => import('@domains/projects/feature/projects.page').then((module) => module.ProjectsPageComponent),
    title: 'Projects',
  },
  {
    path: 'blog',
    loadComponent: () => import('@domains/blog/feature/blog.page').then((module) => module.BlogPageComponent),
    title: 'Blog',
  },
  {
    path: 'blog/:slug',
    loadComponent: () => import('@domains/blog/feature/blog-post.page').then((module) => module.BlogPostPageComponent),
    title: 'Blog Post',
  },
  {
    path: 'contact',
    loadComponent: () => import('@domains/contact/feature/contact.page').then((module) => module.ContactPageComponent),
    title: 'Contact',
  },
  {
    path: 'stats',
    loadComponent: () => import('@domains/stats/feature/stats.page').then((module) => module.StatsPageComponent),
    title: 'Stats',
  },
  {
    path: 'assistant',
    loadComponent: () => import('@domains/assistant/feature/assistant.page').then((module) => module.AssistantPageComponent),
    title: 'Assistant',
  },
  { path: '**', redirectTo: '' },
];
