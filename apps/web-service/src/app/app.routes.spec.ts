import { describe, expect, it } from 'vitest';

import { routes } from './app.routes';

describe('app routes', () => {
  it('redirects the bare root path to the default locale', () => {
    const rootRoute = routes.find((route) => route.path === '');

    expect(rootRoute?.redirectTo).toBe('en');
  });

  it('redirects unlocalized public blog detail URLs to the default locale instead of the homepage', () => {
    const blogDetailRedirect = routes.find((route) => route.path === 'blog/:slug');

    expect(blogDetailRedirect?.redirectTo).toBe('en/blog/:slug');
  });

  it('keeps stale project detail URLs on the projects page instead of falling back to the homepage', () => {
    const localeRoute = routes.find((route) => route.matcher);
    const projectDetailRedirect = localeRoute?.children?.find((route) => route.path === 'projects/:slug');

    expect(projectDetailRedirect?.redirectTo).toBe('projects');
  });

  it('redirects unknown admin child routes to the homepage', () => {
    const adminRoute = routes.find((route) => route.path === 'admin');
    const adminWildcardRoute = adminRoute?.children?.find((route) => route.path === '**');

    expect(adminWildcardRoute?.redirectTo).toBe('/');
  });
});
