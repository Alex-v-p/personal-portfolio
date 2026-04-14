import { describe, expect, it } from 'vitest';

import { routes } from './app.routes';

describe('app routes', () => {
  it('redirects unknown top-level routes to the homepage', () => {
    const wildcardRoute = routes.find((route) => route.path === '**');

    expect(wildcardRoute?.redirectTo).toBe('');
  });

  it('redirects unknown admin child routes to the homepage', () => {
    const adminRoute = routes.find((route) => route.path === 'admin');
    const adminWildcardRoute = adminRoute?.children?.find((route) => route.path === '**');

    expect(adminWildcardRoute?.redirectTo).toBe('/');
  });
});
