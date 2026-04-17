import { ApplicationConfig } from '@angular/core';
import { provideRouter, TitleStrategy } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { routes } from './app.routes';
import { AppTitleStrategy } from './core/routing/app-title.strategy';
import { adminAuthInterceptor } from './shared/interceptors/admin-auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([adminAuthInterceptor])),
    {
      provide: TitleStrategy,
      useClass: AppTitleStrategy,
    },
  ],
};