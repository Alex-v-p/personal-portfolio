import { Routes } from '@angular/router';

import { AssistantPageComponent } from './features/assistant/assistant.page';
import { BlogPageComponent } from './features/blog/blog.page';
import { ContactPageComponent } from './features/contact/contact.page';
import { ExperiencePageComponent } from './features/experience/experience.page';
import { HomePageComponent } from './features/home/home.page';
import { ProjectsPageComponent } from './features/projects/projects.page';

export const routes: Routes = [
  { path: '', component: HomePageComponent, title: 'Home' },
  { path: 'projects', component: ProjectsPageComponent, title: 'Projects' },
  { path: 'experience', component: ExperiencePageComponent, title: 'Experience' },
  { path: 'blog', component: BlogPageComponent, title: 'Blog' },
  { path: 'contact', component: ContactPageComponent, title: 'Contact' },
  { path: 'assistant', component: AssistantPageComponent, title: 'Assistant' },
  { path: '**', redirectTo: '' }
];
