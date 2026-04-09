import { Component } from '@angular/core';

import { AppShellComponent } from './core/layout/app-shell.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AppShellComponent],
  templateUrl: './app.component.html'
})
export class AppComponent {}
