import { Routes } from '@angular/router';

import { AdminLoginPageComponent } from './features/admin/admin-login.page';
import { AdminPageComponent } from './features/admin/admin.page';
import { AssistantPageComponent } from './features/assistant/assistant.page';
import { BlogPostPageComponent } from './features/blog-post/blog-post.page';
import { BlogPageComponent } from './features/blog/blog.page';
import { ContactPageComponent } from './features/contact/contact.page';
import { HomePageComponent } from './features/home/home.page';
import { ProjectsPageComponent } from './features/projects/projects.page';
import { StatsPageComponent } from './features/stats/stats.page';
import { adminAuthGuard, adminGuestGuard } from './shared/guards/admin-auth.guard';

export const routes: Routes = [
  { path: 'admin/login', component: AdminLoginPageComponent, title: 'Admin Login', canActivate: [adminGuestGuard] },
  { path: 'admin', component: AdminPageComponent, title: 'Admin CMS', canActivate: [adminAuthGuard] },
  { path: '', component: HomePageComponent, title: 'Home' },
  { path: 'projects', component: ProjectsPageComponent, title: 'Projects' },
  { path: 'blog', component: BlogPageComponent, title: 'Blog' },
  { path: 'blog/:slug', component: BlogPostPageComponent, title: 'Blog Post' },
  { path: 'contact', component: ContactPageComponent, title: 'Contact' },
  { path: 'stats', component: StatsPageComponent, title: 'Stats' },
  { path: 'assistant', component: AssistantPageComponent, title: 'Assistant' },
  { path: '**', redirectTo: '' }
];
