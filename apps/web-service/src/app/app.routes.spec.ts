import { describe, expect, it } from 'vitest';

import { routes } from './app.routes';

describe('app routes', () => {
  it('redirects the bare root path to the default locale', () => {
    const rootRoute = routes.find((route) => route.path === '');

    expect(rootRoute?.redirectTo).toBe('en');
  });

  it('redirects unknown admin child routes to the homepage', () => {
    const adminRoute = routes.find((route) => route.path === 'admin');
    const adminWildcardRoute = adminRoute?.children?.find((route) => route.path === '**');

    expect(adminWildcardRoute?.redirectTo).toBe('/');
  });
});
