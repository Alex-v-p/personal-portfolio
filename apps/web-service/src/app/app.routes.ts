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
    loadComponent: () => import('@domains/admin/shell/feature/admin.page').then((module) => module.AdminPageComponent),
    title: 'Admin CMS',
    canActivate: [adminAuthGuard],
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
  { path: '**', redirectTo: '' }
];
