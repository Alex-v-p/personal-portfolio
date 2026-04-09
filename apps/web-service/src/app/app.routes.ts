import { Routes } from '@angular/router';

import { AssistantPageComponent } from './features/assistant/assistant.page';
import { BlogPostPageComponent } from './features/blog-post/blog-post.page';
import { BlogPageComponent } from './features/blog/blog.page';
import { ContactPageComponent } from './features/contact/contact.page';
import { HomePageComponent } from './features/home/home.page';
import { ProjectsPageComponent } from './features/projects/projects.page';
import { StatsPageComponent } from './features/stats/stats.page';

export const routes: Routes = [
  { path: '', component: HomePageComponent, title: 'Home' },
  { path: 'projects', component: ProjectsPageComponent, title: 'Projects' },
  { path: 'blog', component: BlogPageComponent, title: 'Blog' },
  { path: 'blog/:slug', component: BlogPostPageComponent, title: 'Blog Post' },
  { path: 'contact', component: ContactPageComponent, title: 'Contact' },
  { path: 'stats', component: StatsPageComponent, title: 'Stats' },
  { path: 'assistant', component: AssistantPageComponent, title: 'Assistant' },
  { path: '**', redirectTo: '' }
];
