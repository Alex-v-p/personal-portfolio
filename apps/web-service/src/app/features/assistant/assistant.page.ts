import { Component } from '@angular/core';

import { AssistantPanelComponent } from '../../shared/components/assistant-panel/assistant-panel.component';

@Component({
  selector: 'app-assistant-page',
  standalone: true,
  imports: [AssistantPanelComponent],
  templateUrl: './assistant.page.html'
})
export class AssistantPageComponent {}
