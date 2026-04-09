import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [NgFor, UiButtonComponent, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './home.page.html'
})
export class HomePageComponent {
  protected readonly heroSkills = ['Angular', 'Tailwind', 'TypeScript'];

  protected readonly featuredBlog = {
    badge: 'Featured',
    date: 'July 29, 2025',
    readTime: '5 min read',
    title: 'Title of the Blog Post',
    excerpt: 'Excerpts about process, frontend architecture, and the lessons learned while building a personal portfolio.',
    tags: ['Angular', 'UI/UX', 'Career']
  };

  protected readonly featuredProject = {
    badge: 'Featured',
    company: 'Side project',
    duration: '3 months',
    status: 'Completed',
    title: 'Title of the Project',
    excerpt: 'A practical web project focused on clean component design, maintainable structure, and strong user experience.',
    tags: ['Tailwind', 'SSR', 'API', 'UI kit'],
    details: 'Key results, responsibilities, and impact can live here later without redesigning the card shape.'
  };

  protected readonly expertiseGroups = [
    { title: 'Front-End', tags: ['Angular', 'Tailwind', 'HTML'] },
    { title: 'Back-End', tags: ['Node.js', '.NET', 'REST APIs'] },
    { title: 'AI', tags: ['ML', 'Data Prep', 'Python'] },
    { title: 'Programming', tags: ['Java', 'C#', 'TypeScript'] },
    { title: 'Languages', tags: ['Dutch', 'English', 'French'] }
  ];

  protected readonly experienceItems = [
    { title: 'Internship', location: 'Geel, Belgium', period: 'Feb 2025 - Jun 2025', text: 'Worked on web interfaces, client communication, and delivery of maintainable features.' },
    { title: 'Thomas More', location: 'Geel, Belgium', period: '2022 - present', text: 'Applied Computer Science with a focus on AI, software engineering, and practical project work.' },
    { title: 'Personal Projects', location: 'Remote', period: '2023 - present', text: 'Built portfolio, API, and full-stack learning projects to sharpen real-world development skills.' }
  ];

  protected readonly connectCards = [
    { title: 'Email', value: 'your.email@example.com', action: 'Send Email' },
    { title: 'Phone', value: '+32 470 12 34 39', action: 'Call' },
    { title: 'GitHub', value: 'github.com/shuzu', action: 'Connect +' },
    { title: 'LinkedIn', value: 'linkedin.com/in/your-name', action: 'Connect +' }
  ];
}
