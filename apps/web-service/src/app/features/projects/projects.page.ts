import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';

@Component({
  selector: 'app-projects-page',
  standalone: true,
  imports: [NgFor, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './projects.page.html'
})
export class ProjectsPageComponent {
  protected readonly filters = ['Frontend', 'Backend', 'AI'];
  protected readonly pagerDots = [1, 2, 3];

  protected readonly featuredProject = {
    badge: 'Featured',
    source: 'CEV/ux',
    duration: '3 months',
    status: 'Completed',
    title: 'Title of the Project',
    excerpt: 'A highlighted project card that already includes all the content fields from the wireframe.',
    tags: ['Skill', 'Skill', 'Skill', 'Skill'],
    details: 'Describe the implementation, your role, and the measurable result here. This lets you swap to mock data later without redesigning the layout.',
    linkText: 'Goes to github read me'
  };

  protected readonly projects = [
    {
      company: 'Thomas More',
      duration: '6 months',
      title: 'Title of the Project',
      excerpt: 'Example project summary that explains the challenge and outcome in a concise way.',
      tags: ['Skill', 'Skill'],
      slug: '/projects'
    },
    {
      company: 'Thomas More',
      duration: '6 months',
      title: 'Title of the Project',
      excerpt: 'Example project summary that explains the challenge and outcome in a concise way.',
      tags: ['Skill', 'Skill'],
      slug: '/projects'
    },
    {
      company: 'Thomas More',
      duration: '6 months',
      title: 'Title of the Project',
      excerpt: 'Example project summary that explains the challenge and outcome in a concise way.',
      tags: ['Skill', 'Skill'],
      slug: '/projects'
    }
  ];
}
