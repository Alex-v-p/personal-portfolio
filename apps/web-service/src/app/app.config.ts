import { APP_INITIALIZER, ApplicationConfig } from '@angular/core';
import { provideRouter, TitleStrategy } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { routes } from './app.routes';
import { AppTitleStrategy } from './core/routing/app-title.strategy';
import { I18nService } from './core/i18n/i18n.service';
import { adminAuthInterceptor } from './shared/interceptors/admin-auth.interceptor';

function initializeI18n(i18n: I18nService): () => Promise<void> {
  return () => i18n.initialize();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([adminAuthInterceptor])),
    {
      provide: APP_INITIALIZER,
      multi: true,
      deps: [I18nService],
      useFactory: initializeI18n,
    },
    {
      provide: TitleStrategy,
      useClass: AppTitleStrategy,
    },
  ],
};
