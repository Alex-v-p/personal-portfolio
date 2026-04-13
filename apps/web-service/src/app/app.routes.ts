import { Routes } from '@angular/router';

import { adminAuthGuard, adminGuestGuard } from './shared/guards/admin-auth.guard';

export const routes: Routes = [
  {
    path: 'admin/login',
    loadComponent: () => import('./features/admin/admin-login.page').then((module) => module.AdminLoginPageComponent),
    title: 'Admin Login',
    canActivate: [adminGuestGuard],
  },
  {
    path: 'admin',
    loadComponent: () => import('./features/admin/admin.page').then((module) => module.AdminPageComponent),
    title: 'Admin CMS',
    canActivate: [adminAuthGuard],
  },
  {
    path: '',
    loadComponent: () => import('./features/home/home.page').then((module) => module.HomePageComponent),
    title: 'Home',
  },
  {
    path: 'projects',
    loadComponent: () => import('./features/projects/projects.page').then((module) => module.ProjectsPageComponent),
    title: 'Projects',
  },
  {
    path: 'blog',
    loadComponent: () => import('./features/blog/blog.page').then((module) => module.BlogPageComponent),
    title: 'Blog',
  },
  {
    path: 'blog/:slug',
    loadComponent: () => import('./features/blog-post/blog-post.page').then((module) => module.BlogPostPageComponent),
    title: 'Blog Post',
  },
  {
    path: 'contact',
    loadComponent: () => import('./features/contact/contact.page').then((module) => module.ContactPageComponent),
    title: 'Contact',
  },
  {
    path: 'stats',
    loadComponent: () => import('./features/stats/stats.page').then((module) => module.StatsPageComponent),
    title: 'Stats',
  },
  {
    path: 'assistant',
    loadComponent: () => import('./features/assistant/assistant.page').then((module) => module.AssistantPageComponent),
    title: 'Assistant',
  },
  { path: '**', redirectTo: '' }
];
